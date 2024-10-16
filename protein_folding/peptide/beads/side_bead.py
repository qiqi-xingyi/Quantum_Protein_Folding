"""A class defining a side bead of a peptide."""
from typing import Tuple, Optional

from qiskit.quantum_info import SparsePauliOp  # 替换为 SparsePauliOp

from .base_bead import BaseBead

class SideBead(BaseBead):
    """A class defining a side bead of a peptide."""

    def __init__(
        self,
        main_index: int,
        side_index: int,
        residue_type: Optional[str],
        turn_qubits: Tuple[SparsePauliOp, SparsePauliOp],  # 修改为 SparsePauliOp
    ):
        """
        Args:
            main_index: Index of the bead on the main chain in a peptide to which the side
                        chain of this side bead is attached.
            side_index: Index of the bead on the related side chain in a peptide.
            residue_type: A character representing the type of a residue for the bead. Empty
                        string if a side bead does not exists.
            turn_qubits: A tuple of two Pauli operators that encodes the turn following from a given
                        bead index.
        """
        super().__init__(
            "side_chain",
            main_index,
            residue_type,
            turn_qubits,
            self._build_turn_indicator_fun_0,
            self._build_turn_indicator_fun_1,
            self._build_turn_indicator_fun_2,
            self._build_turn_indicator_fun_3,
        )
        self.side_index = side_index

    def __str__(self):
        return (
            self.chain_type
            + "_"
            + str(self.side_index)
            + "_main_chain_ind_"
            + str(self.main_index)
        )

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if not isinstance(other, SideBead):
            return False
        return (
            self.main_index == other.main_index
            and self.side_index == other.side_index
            and self.chain_type == other.chain_type
        )

    def _build_turn_indicator_fun_0(self) -> SparsePauliOp:  # 返回类型为 SparsePauliOp
        return (
            (
                (self._full_id - self._turn_qubits[0])
                @ (self._full_id - self._turn_qubits[1])
            )
            ^ self._full_id
        ).reduce()

    def _build_turn_indicator_fun_1(self) -> SparsePauliOp:  # 返回类型为 SparsePauliOp
        return (
            (self._turn_qubits[1] @ (self._turn_qubits[1] - self._turn_qubits[0]))
            ^ self._full_id
        ).reduce()

    def _build_turn_indicator_fun_2(self) -> SparsePauliOp:  # 返回类型为 SparsePauliOp
        return (
            (self._turn_qubits[0] @ (self._turn_qubits[0] - self._turn_qubits[1]))
            ^ self._full_id
        ).reduce()

    def _build_turn_indicator_fun_3(self) -> SparsePauliOp:  # 返回类型为 SparsePauliOp
        return (self._turn_qubits[0] @ self._turn_qubits[1] ^ self._full_id).reduce()
