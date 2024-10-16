"""Changes certain qubits to fixed values."""
from typing import Union

import numpy as np
from qiskit.quantum_info import SparsePauliOp, PauliList, Pauli  # 使用新的 PauliList 和 SparsePauliOp


def _fix_qubits(
    operator: Union[int, SparsePauliOp],  # 移除 OperatorBase
    has_side_chain_second_bead: bool = False,
) -> Union[int, SparsePauliOp]:
    """
    Assigns predefined values for turns qubits on positions 0, 1, 2, 3, 5 in the main chain
    without the loss of generality (see the paper https://arxiv.org/pdf/1908.02163.pdf). Qubits
    on these position are considered fixed and not subject to optimization.

    Args:
        operator: an operator whose qubits shall be fixed.

    Returns:
        An operator with relevant qubits changed to fixed values.
    """
    # operator might be 0 (int) because it is initialized as operator = 0; then we should not
    # attempt fixing qubits
    if not isinstance(operator, SparsePauliOp):
        return operator
    operator = operator.reduce()

    table_z = np.copy(operator.paulis.z)
    table_x = np.copy(operator.paulis.x)
    _preset_binary_vals(table_z, has_side_chain_second_bead)

    return SparsePauliOp(Pauli((table_z, table_x)), coeffs=operator.coeffs)


def _calc_updated_coeffs(
    hamiltonian: SparsePauliOp, table_z, has_side_chain_second_bead: bool
) -> np.ndarray:
    coeffs = np.copy(hamiltonian.coeffs[0])
    if len(table_z) > 1 and table_z[1]:
        coeffs = -1 * coeffs
    if (
        not has_side_chain_second_bead
        and len(table_z) > 6
        and table_z[5]
    ):
        coeffs = -1 * coeffs
    return coeffs


def _preset_binary_vals(table_z, has_side_chain_second_bead: bool):
    main_beads_indices = [0, 1, 2, 3]
    if not has_side_chain_second_bead:
        main_beads_indices.append(5)
    for index in main_beads_indices:
        _preset_single_binary_val(table_z, index)


def _preset_single_binary_val(table_z, index: int):
    try:
        table_z[index] = False  # 直接设置为 False，无需使用 np.bool_
    except IndexError:
        pass
