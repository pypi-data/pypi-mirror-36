from GridCal.Engine.CalculationEngine import MultiCircuit, BranchType
from networkx import DiGraph, all_simple_paths
import numpy as np
import pandas as pd
from scipy.sparse import lil_matrix, csc_matrix

from PyQt5.QtCore import QThread, QRunnable, pyqtSignal

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def get_branches_of_bus(B, j):
    """
    Get the indices of the branches connected to the bus j
    :param B: Branch-bus CSC matrix
    :param j: bus index
    :return: list of branches in the bus
    """
    return [B.indices[k] for k in range(B.indptr[j], B.indptr[j + 1])]


def reduce_grid(circuit: MultiCircuit, rx_criteria=True, rx_threshold=1e-5,
                type_criteria=True, selected_type=BranchType.Branch):

    deleted_any = True
    while deleted_any:
        deleted_any = reduce_grid_brute(circuit=circuit, rx_criteria=rx_criteria, rx_threshold=rx_threshold,
                                        type_criteria=type_criteria, selected_type=selected_type)


def reduce_grid_brute(circuit: MultiCircuit, rx_criteria=True, rx_threshold=1e-5,
                      type_criteria=True, selected_type=BranchType.Branch):
    """
    Remove the first branch found to be removed.
    this function is meant to be called until it returns false
    Args:
        circuit: Circuit to modify in-place
        rx_criteria: use the r+x threshold to select branches?
        rx_threshold: r+x threshold
        type_criteria: use the branch type criteria to remove branches?
        selected_type: branch type

    Returns:
        - Was any branch deleted? (True / False)
        - Number of branches found to be deleted
        - name of the branch
    """

    # form C
    m = len(circuit.branches)
    n = len(circuit.buses)
    buses_dict = {bus: i for i, bus in enumerate(circuit.buses)}
    branches_to_keep_idx = list()
    branches_to_remove_idx = list()
    C = lil_matrix((m, n), dtype=int)
    graph = DiGraph()

    for i in range(len(circuit.branches)):
        # get the from and to bus indices
        f = buses_dict[circuit.branches[i].bus_from]
        t = buses_dict[circuit.branches[i].bus_to]
        graph.add_edge(f, t)
        C[i, f] = 1
        C[i, t] = -1

        # check if to select the branch for removal
        chosen_to_be_removed = False

        if type_criteria:

            # is this branch of the selected type?
            if circuit.branches[i].branch_type == selected_type:

                # am I looking for branches of this type under an r+x threshold?
                if rx_criteria:

                    rx = circuit.branches[i].R + circuit.branches[i].X

                    # if the r+x criteria is met, add it
                    if rx < rx_threshold:
                        print(i, '->', rx, '<', rx_threshold)
                        branches_to_remove_idx.append(i)
                        chosen_to_be_removed = True

                else:
                    # Add the branch because it was selected and there is no further criteria
                    branches_to_remove_idx.append(i)
                    chosen_to_be_removed = True

        if not chosen_to_be_removed:
            branches_to_keep_idx.append(i)

    C = csc_matrix(C)

    # atempt to remove
    if len(branches_to_remove_idx) > 0:

        # get the first index
        br_idx = branches_to_remove_idx[0]
        br_name = circuit.branches[br_idx].name
        bus_f = circuit.branches[br_idx].bus_from
        bus_t = circuit.branches[br_idx].bus_to
        f = buses_dict[bus_f]
        t = buses_dict[bus_t]

        # get the number of paths
        n_paths = len(list(all_simple_paths(graph, f, t)))

        # print('Deleting: ', circuit.branches[br_idx].name)

        if n_paths == 1:

            # print('\tMerging', bus_f.name, bus_t.name)

            # removing the bus f
            branches = get_branches_of_bus(C, f)

            for k in branches:
                f2 = buses_dict[circuit.branches[k].bus_from]
                t2 = buses_dict[circuit.branches[k].bus_to]

                if f2 == f:
                    circuit.branches[k].bus_from = bus_t
                elif t2 == t2:
                    circuit.branches[k].bus_to = bus_t

            # merge buses
            bus_t.merge(bus_f)

            # delete bus
            circuit.buses.pop(f)

            # remove the branch and that's it
            circuit.branches.pop(br_idx)

        else:
            # print('\tsimple_delete')
            # remove the branch and that's it
            circuit.branches.pop(br_idx)

        return True, len(branches_to_remove_idx), br_name
    else:
        return False, len(branches_to_remove_idx), ''


class TopologyReductionOptions:

    def __init__(self, rx_criteria=False, rx_threshold=1e-5,
                 type_criteria=True, selected_type=BranchType.Branch):
        """
        Topology reduction options
        :param rx_criteria:
        :param rx_threshold:
        :param type_criteria:
        :param selected_type:
        """

        self.rx_criteria = rx_criteria
        self.rx_threshold = rx_threshold
        self.type_criteria = type_criteria
        self.selected_type = selected_type


class TopologyReduction(QThread):
    progress_signal = pyqtSignal(float)
    progress_text = pyqtSignal(str)
    done_signal = pyqtSignal()

    def __init__(self, grid: MultiCircuit, options: TopologyReductionOptions):
        """
        Topology reduction driver
        :param grid: MultiCircuit instance
        :param options:
        """
        QThread.__init__(self)

        self.grid = grid

        self.options = options

        self.__cancel__ = False

    def run(self):
        """
        Run the monte carlo simulation
        @return:
        """
        self.progress_signal.emit(0.0)

        deleted_any = True
        i = 0
        total = 1

        while deleted_any:

            # delete branch
            deleted_any, n_left, br_name = reduce_grid_brute(circuit=self.grid,
                                                             rx_criteria=self.options.rx_criteria,
                                                             rx_threshold=self.options.rx_threshold,
                                                             type_criteria=self.options.type_criteria,
                                                             selected_type=self.options.selected_type)

            if i == 0:
                total = n_left

            if deleted_any:
                self.progress_text.emit('Removed branch ' + br_name)
                progress = (i+1) / total * 100
                self.progress_signal.emit(progress)

            # increase counter
            i += 1

        self.progress_text.emit('Done')
        self.progress_signal.emit(0.0)
        self.done_signal.emit()

    def cancel(self):
        """
        Cancel the simulation
        :return:
        """
        self.__cancel__ = True
        self.progress_signal.emit(0.0)
        self.progress_text.emit('Cancelled')
        self.done_signal.emit()


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    # fname = 'D:\\GitHub\\GridCal\\Grids_and_profiles\\grids\\Reduction Model 3.xlsx'
    fname = 'D:\\GitHub\\GridCal\\UnderDevelopment\\GridCal\\Engine\\Importers\\Export_sensible_v15_modif.json.xlsx'

    circuit_ = MultiCircuit()
    circuit_.load_file(fname)
    # circuit.compile()
    top = TopologyReduction(grid=circuit_, rx_criteria=False, rx_threshold=1e-5,
                            type_criteria=True, selected_type=BranchType.Branch)
    top.run()
    # circuit_.compile()
    # circuit_.plot_graph()
    # plt.show()