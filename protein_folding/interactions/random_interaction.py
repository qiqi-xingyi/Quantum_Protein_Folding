import numpy as np
from qiskit_algorithms.utils import algorithm_globals

from .interaction import Interaction

# pylint: disable=too-few-public-methods

class RandomInteraction(Interaction):
    """A class defining a random interaction between beads of a peptide."""

    def calculate_energy_matrix(self, residue_sequence: str) -> np.ndarray:
        """
        Calculates an energy matrix for a random interaction.

        Args:
            residue_sequence: Dummy residue sequence; only used to infer the length of a chain.

        Returns:
            Numpy array of pair energies for amino acids.
        """
        chain_len = len(residue_sequence)
        pair_energies = -1 - 4 * algorithm_globals.random.random(
            (chain_len + 1, 2, chain_len + 1, 2)
        )
        return pair_energies
