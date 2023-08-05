# This file is part of GridCal.
#
# GridCal is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GridCal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GridCal.  If not, see <http://www.gnu.org/licenses/>.

import pandas as pd
from numpy import complex, double, sqrt, zeros, ones, nan_to_num, exp, conj, ndarray, vstack, power, delete, where, \
    r_, Inf, linalg, maximum, array, nan, shape, arange, sort, interp, iscomplexobj, c_, argwhere, floor
from scipy.sparse.linalg import inv
from matplotlib import pyplot as plt
from PyQt5.QtCore import QThread, QRunnable, pyqtSignal

from GridCal.Engine.Numerical.SC import short_circuit_3p
from GridCal.Engine.CalculationEngine import LINEWIDTH, Circuit, MultiCircuit
from GridCal.Engine.PowerFlowDriver import PowerFlowResults


########################################################################################################################
# Short circuit classes
########################################################################################################################


class ShortCircuitOptions:

    def __init__(self, bus_index, verbose=False):
        """

        Args:
            bus_index: indices of the short circuited buses
            zf: fault impedance
        """
        self.bus_index = bus_index

        self.verbose = verbose


class ShortCircuitResults(PowerFlowResults):

    def __init__(self, Sbus=None, voltage=None, Sbranch=None, Ibranch=None, loading=None, losses=None, SCpower=None,
                 error=None, converged=None, Qpv=None):

        """

        Args:
            Sbus:
            voltage:
            Sbranch:
            Ibranch:
            loading:
            losses:
            SCpower:
            error:
            converged:
            Qpv:
        """
        PowerFlowResults.__init__(self, Sbus=Sbus, voltage=voltage, Sbranch=Sbranch, Ibranch=Ibranch,
                                  loading=loading, losses=losses, error=error, converged=converged, Qpv=Qpv)

        self.short_circuit_power = SCpower

        self.available_results = ['Bus voltage', 'Branch power', 'Branch current', 'Branch_loading', 'Branch losses',
                                  'Bus short circuit power']

    def copy(self):
        """
        Return a copy of this
        @return:
        """
        return ShortCircuitResults(Sbus=self.Sbus, voltage=self.voltage, Sbranch=self.Sbranch,
                                   Ibranch=self.Ibranch, loading=self.loading,
                                   losses=self.losses, SCpower=self.short_circuit_power, error=self.error,
                                   converged=self.converged, Qpv=self.Qpv)

    def initialize(self, n, m):
        """
        Initialize the arrays
        @param n: number of buses
        @param m: number of branches
        @return:
        """
        self.Sbus = zeros(n, dtype=complex)

        self.voltage = zeros(n, dtype=complex)

        self.short_circuit_power = zeros(n, dtype=complex)

        self.overvoltage = zeros(n, dtype=complex)

        self.undervoltage = zeros(n, dtype=complex)

        self.Sbranch = zeros(m, dtype=complex)

        self.Ibranch = zeros(m, dtype=complex)

        self.loading = zeros(m, dtype=complex)

        self.losses = zeros(m, dtype=complex)

        self.overloads = zeros(m, dtype=complex)

        self.error = 0

        self.converged = True

        self.buses_useful_for_storage = list()

    def apply_from_island(self, results, b_idx, br_idx):
        """
        Apply results from another island circuit to the circuit results represented here
        @param results: PowerFlowResults
        @param b_idx: bus original indices
        @param br_idx: branch original indices
        @return:
        """
        self.Sbus[b_idx] = results.Sbus

        self.voltage[b_idx] = results.voltage

        self.short_circuit_power[b_idx] = results.short_circuit_power

        self.overvoltage[b_idx] = results.overvoltage

        self.undervoltage[b_idx] = results.undervoltage

        self.Sbranch[br_idx] = results.Sbranch

        self.Ibranch[br_idx] = results.Ibranch

        self.loading[br_idx] = results.loading

        self.losses[br_idx] = results.losses

        self.overloads[br_idx] = results.overloads

        if results.error > self.error:
            self.error = results.error

        self.converged = self.converged and results.converged

        if results.buses_useful_for_storage is not None:
            self.buses_useful_for_storage = b_idx[results.buses_useful_for_storage]

    def plot(self, result_type, ax=None, indices=None, names=None):
        """
        Plot the results
        Args:
            result_type:
            ax:
            indices:
            names:

        Returns:

        """

        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)

        if indices is None:
            indices = array(range(len(names)))

        if len(indices) > 0:
            labels = names[indices]
            ylabel = ''
            title = ''
            if result_type == 'Bus voltage':
                y = self.voltage[indices]
                ylabel = '(p.u.)'
                title = 'Bus voltage '

            elif result_type == 'Branch power':
                y = self.Sbranch[indices]
                ylabel = '(MVA)'
                title = 'Branch power '

            elif result_type == 'Branch current':
                y = self.Ibranch[indices]
                ylabel = '(p.u.)'
                title = 'Branch current '

            elif result_type == 'Branch_loading':
                y = self.loading[indices] * 100
                ylabel = '(%)'
                title = 'Branch loading '

            elif result_type == 'Branch losses':
                y = self.losses[indices]
                ylabel = '(MVA)'
                title = 'Branch losses '

            elif result_type == 'Bus short circuit power':
                y = self.short_circuit_power[indices]
                ylabel = '(MVA)'
                title = 'Bus short circuit power'
            else:
                pass

            df = pd.DataFrame(data=y, index=labels, columns=[result_type])
            df.abs().plot(ax=ax, kind='bar', linewidth=LINEWIDTH)
            ax.set_ylabel(ylabel)
            ax.set_title(title)

            return df

        else:
            return None


class ShortCircuit(QRunnable):
    # progress_signal = pyqtSignal(float)
    # progress_text = pyqtSignal(str)
    # done_signal = pyqtSignal()

    def __init__(self, grid: MultiCircuit, options: ShortCircuitOptions, pf_results: PowerFlowResults):
        """
        PowerFlow class constructor
        @param grid: MultiCircuit Object
        """
        QRunnable.__init__(self)

        # Grid to run a power flow in
        self.grid = grid

        # power flow results
        self.pf_results = pf_results

        # Options to use
        self.options = options

        # compile the buses short circuit impedance array
        n = len(self.grid.buses)
        self.Zf = zeros(n, dtype=complex)
        for i in range(n):
            self.Zf[i] = self.grid.buses[i].Zf

        self.results = None

        self.__cancel__ = False

    def single_short_circuit(self, circuit: Circuit, Vpf):
        """
        Run a power flow simulation for a single circuit
        @param circuit:
        @param Vpf: Power flow voltage
        @return: short circuit results
        """
        # compute Zbus if needed
        if circuit.power_flow_input.Zbus is None:
            # is dense, so no need to store it as sparse
            circuit.power_flow_input.Zbus = inv(circuit.power_flow_input.Ybus).toarray()

        # Compute the short circuit
        V, SCpower = short_circuit_3p(bus_idx=self.options.bus_index,
                                      Zbus=circuit.power_flow_input.Zbus,
                                      Vbus=Vpf,
                                      Zf=self.Zf, baseMVA=circuit.Sbase)

        # Compute the branches power
        Sbranch, Ibranch, loading, losses = self.compute_branch_results(circuit=circuit, V=V)

        # voltage, Sbranch, loading, losses, error, converged, Qpv
        results = ShortCircuitResults(Sbus=circuit.power_flow_input.Sbus,
                                      voltage=V,
                                      Sbranch=Sbranch,
                                      Ibranch=Ibranch,
                                      loading=loading,
                                      losses=losses,
                                      SCpower=SCpower,
                                      error=0,
                                      converged=True,
                                      Qpv=None)

        return results

    @staticmethod
    def compute_branch_results(circuit: Circuit, V):
        """
        Compute the power flows trough the branches
        @param circuit: instance of Circuit
        @param V: Voltage solution array for the circuit buses
        @return: Sbranch, Ibranch, loading, losses
        """
        If = circuit.power_flow_input.Yf * V
        It = circuit.power_flow_input.Yt * V
        Sf = V[circuit.power_flow_input.F] * conj(If)
        St = V[circuit.power_flow_input.T] * conj(It)
        losses = Sf - St
        Ibranch = maximum(If, It)
        Sbranch = maximum(Sf, St)
        loading = Sbranch * circuit.Sbase / circuit.power_flow_input.branch_rates

        # idx = where(abs(loading) == inf)[0]
        # loading[idx] = 9999

        return Sbranch, Ibranch, loading, losses

    def run(self):
        """
        Run a power flow for every circuit
        @return:
        """
        # print('Short circuit at ', self.grid.name)
        # self.progress_signal.emit(0.0)

        n = len(self.grid.buses)
        m = len(self.grid.branches)
        results = ShortCircuitResults()  # yes, reuse this class
        results.initialize(n, m)
        k = 0
        for circuit in self.grid.circuits:
            if self.options.verbose:
                print('Solving ' + circuit.name)

            circuit.short_circuit_results = self.single_short_circuit(circuit=circuit,
                                                                      Vpf=self.pf_results.voltage[circuit.bus_original_idx])
            results.apply_from_island(circuit.short_circuit_results,
                                      circuit.bus_original_idx,
                                      circuit.branch_original_idx)

            # self.progress_signal.emit((k+1) / len(self.grid.circuits))
            k += 1

        self.results = results
        self.grid.short_circuit_results = results

    def cancel(self):
        self.__cancel__ = True
