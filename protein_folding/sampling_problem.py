"""An interface for sampling problems."""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union

from qiskit_algorithms import MinimumEigensolverResult
from qiskit.quantum_info import SparsePauliOp

if TYPE_CHECKING:
    from .protein_folding_result import ProteinFoldingResult


class SamplingProblem(ABC):
    """An interface for sampling problems."""

    @abstractmethod
    def qubit_op(self) -> SparsePauliOp:
        """Returns a qubit operator that represents a Hamiltonian encoding the sampling problem."""

    @abstractmethod
    def interpret(self, raw_result: MinimumEigensolverResult) -> "ProteinFoldingResult":
        """Interprets results of an optimization."""
