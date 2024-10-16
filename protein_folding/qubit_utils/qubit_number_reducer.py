from typing import Union, List, Dict, Tuple

import numpy as np
from qiskit.quantum_info import PauliList, SparsePauliOp, Pauli  # 使用新的 SparsePauliOp 和 Pauli


def remove_unused_qubits(
    total_hamiltonian: SparsePauliOp
) -> Tuple[SparsePauliOp, List[int]]:
    """
    Removes those qubits from a total Hamiltonian that are equal to an identity operator across
    all terms, i.e. they are irrelevant for the problem. It makes the number of qubits required
    for encoding the problem smaller or equal.

    Args:
        total_hamiltonian: A full Hamiltonian for the protein folding problem.

    Returns:
        Tuple consisting of the total_hamiltonian compressed to an equivalent Hamiltonian and
        indices of qubits in the original Hamiltonian that were unused as optimization variables.
    """
    unused_qubits = _find_unused_qubits(total_hamiltonian)
    num_qubits = total_hamiltonian.num_qubits

    return (
        _compress_sparse_pauli_op(num_qubits, total_hamiltonian, unused_qubits),
        unused_qubits,
    )


def _compress_sparse_pauli_op(
    num_qubits: int, total_hamiltonian: SparsePauliOp, unused_qubits: List[int]
) -> SparsePauliOp:
    table_z = total_hamiltonian.paulis.z
    table_x = total_hamiltonian.paulis.x
    new_table_z, new_table_x = _calc_reduced_pauli_tables(
        num_qubits, table_x, table_z, unused_qubits
    )
    total_hamiltonian_compressed = SparsePauliOp(Pauli((new_table_z, new_table_x)), coeffs=total_hamiltonian.coeffs)
    return total_hamiltonian_compressed


def _calc_reduced_pauli_tables(
    num_qubits: int, table_x, table_z, unused_qubits: List[int]
) -> Tuple[List[bool], List[bool]]:
    new_table_z = []
    new_table_x = []
    for ind in range(num_qubits):
        if ind not in unused_qubits:
            new_table_z.append(table_z[ind])
            new_table_x.append(table_x[ind])

    return new_table_z, new_table_x


def _find_unused_qubits(total_hamiltonian: SparsePauliOp) -> List[int]:
    used_map: Dict[int, bool] = {}
    unused = []
    num_qubits = total_hamiltonian.num_qubits

    table_z = total_hamiltonian.paulis.z
    _update_used_map(num_qubits, table_z, used_map)

    for ind in range(num_qubits):
        if ind not in used_map:
            unused.append(ind)

    return unused


def _update_used_map(num_qubits: int, table_z, used_map: Dict[int, bool]):
    for ind in range(num_qubits):
        if table_z[ind]:
            used_map[ind] = True