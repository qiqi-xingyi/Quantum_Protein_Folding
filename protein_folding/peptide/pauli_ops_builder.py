"""Builds Pauli operators of a given size."""
from typing import Set

from qiskit.quantum_info import SparsePauliOp, Pauli  # 使用新版的 SparsePauliOp 和 Pauli


def _build_full_identity(num_qubits: int) -> SparsePauliOp:
    """
    Builds a full identity operator of a given size.

    Args:
        num_qubits: number of qubits on which a full identity operator will be created.

    Returns:
        A full identity operator of a given size.
    """
    # 构建长度为 num_qubits 的全身份操作符
    identity_str = 'I' * num_qubits
    return SparsePauliOp(Pauli(identity_str))


def _build_pauli_z_op(num_qubits: int, pauli_z_indices: Set[int]) -> SparsePauliOp:
    """
    Builds a Pauli operator of a given size with Pauli Z operators on indicated positions and
    identity operators on other positions.

    Args:
        num_qubits: number of qubits on which a Pauli operator will be created.
        pauli_z_indices: a set of indices in a Pauli operator on which a Pauli Z operator shall
                        appear.

    Returns:
        A Pauli operator of a given size with Pauli Z operators on indicated positions and
        identity operators on other positions.
    """
    # 构建长度为 num_qubits 的 Pauli 字符串，默认是全 I（identity）
    pauli_str = ['I'] * num_qubits

    # 将需要设置为 Z 的位置修改为 'Z'
    for index in pauli_z_indices:
        pauli_str[index] = 'Z'

    # 将字符串列表连接成 Pauli 字符串
    pauli_str = ''.join(pauli_str)

    # 使用 Pauli 字符串构建 SparsePauliOp
    return SparsePauliOp(Pauli(pauli_str))
