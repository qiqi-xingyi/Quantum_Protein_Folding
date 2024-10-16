from abc import ABC
from typing import List, Sequence, Optional

from qiskit.quantum_info import SparsePauliOp  # 替换为 SparsePauliOp

from ..beads.base_bead import BaseBead
from ..pauli_ops_builder import (
    _build_full_identity,
    _build_pauli_z_op,
)


class BaseChain(ABC):
    """An abstract class defining a chain of a peptide."""

    def __init__(self, beads_list: Sequence[BaseBead]):
        """
        Args:
            beads_list: A list of beads that define the chain.
        """
        self._beads_list = beads_list

    def __getitem__(self, item):
        return self._beads_list[item]

    def __len__(self):
        return len(self._beads_list)

    @property
    def beads_list(self) -> Sequence[BaseBead]:
        """Returns the list of all beads in the chain."""
        return self._beads_list

    @property
    def residue_sequence(self) -> List[Optional[str]]:
        """
        Returns the list of all residue sequences in the chain.
        """
        residue_sequence = []
        for bead in self._beads_list:
            residue_sequence.append(bead.residue_type)
        return residue_sequence

    @staticmethod
    def _build_turn_qubit(chain_len: int, pauli_z_index: int) -> SparsePauliOp:  # 修改为 SparsePauliOp
        """
        Builds a SparsePauliOp of length 2 * (chain_len - 1) (number of qubits necessary to encode all
        turns for the chain of length chain_len) with a Pauli Z operator at a given index.

        Args:
            chain_len: length of the chain.
            pauli_z_index: index of a Pauli Z operator in a turn operator.

        Returns:
            A SparsePauliOp operator that encodes the turn following from a given bead index.
        """
        num_turn_qubits = 2 * (chain_len - 1)
        norm_factor = 0.5
        turn_qubit = norm_factor * _build_full_identity(
            num_turn_qubits
        ) - norm_factor * _build_pauli_z_op(num_turn_qubits, {pauli_z_index})
        return turn_qubit
