"""Hash table implementation using separate chaining for collision resolution.

Internal structure:
- Fixed-size array of `size` cells (default 10), initialized to None.
- Each occupied cell holds a list of (key, value) tuples — the chain.
- Custom hash function uses modular arithmetic; no Python hash() builtin.
"""

from typing import Any


class HashTable:
    """Hash table with separate chaining for collision resolution."""

    def __init__(self, size: int = 10) -> None:
        self.size = size
        # Fixed-size array; each cell is None or list[tuple[str, Any]]
        self._table: list[list[tuple[str, Any]] | None] = [None] * size

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _hash(self, key: str) -> int:
        """Compute cell index for *key*.

        Algorithm: sum ASCII values of every character in the string
        representation of the key, then take modulo table size.

        No Python hash() builtin is used.
        Average time complexity: O(k) where k = len(str(key)).
        """
        return sum(ord(c) for c in str(key)) % self.size

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def insert(self, key: str, value: Any) -> None:
        """Insert a key-value pair, or update the value if the key exists.

        Average time complexity: O(1).
        Worst case (all keys map to same cell): O(n).
        """
        index = self._hash(key)
        if self._table[index] is None:
            self._table[index] = [(key, value)]
        else:
            # Update existing key in chain if present
            chain = self._table[index]
            for i, (k, _) in enumerate(chain):
                if k == key:
                    chain[i] = (key, value)
                    return
            # Key not in chain — append (collision via separate chaining)
            chain.append((key, value))

    def search(self, key: str) -> Any | None:
        """Return the value associated with *key*, or None if not found.

        Average time complexity: O(1).
        Worst case: O(n).
        """
        index = self._hash(key)
        chain = self._table[index]
        if chain is None:
            return None
        for k, v in chain:
            if k == key:
                return v
        return None

    def delete(self, key: str) -> bool:
        """Remove the key-value pair for *key*.

        Returns True if the key was found and removed, False otherwise.

        Average time complexity: O(1).
        Worst case: O(n).
        """
        index = self._hash(key)
        chain = self._table[index]
        if chain is None:
            return False
        for i, (k, _) in enumerate(chain):
            if k == key:
                chain.pop(i)
                if not chain:
                    self._table[index] = None
                return True
        return False

    def list_all(self) -> list[tuple[str, Any]]:
        """Return all (key, value) pairs stored in the table.

        Time complexity: O(n) where n = total number of elements.
        """
        result: list[tuple[str, Any]] = []
        for chain in self._table:
            if chain:
                result.extend(chain)
        return result

    def stats(self) -> dict[str, Any]:
        """Return internal metrics describing the hash table state.

        Time complexity: O(n + size).

        Returned dict keys:
          table_size          — total cells in the backing array
          total_elements      — number of stored key-value pairs
          used_cells          — cells that contain at least one element
          cells_with_collision — cells with two or more elements
          load_factor         — total_elements / table_size
          distribution        — list of element counts, one entry per cell index
        """
        distribution = [len(chain) if chain else 0 for chain in self._table]
        total_elements = sum(distribution)
        used_cells = sum(1 for c in distribution if c > 0)
        cells_with_collision = sum(1 for c in distribution if c >= 2)
        load_factor = round(total_elements / self.size, 4)

        return {
            "table_size": self.size,
            "total_elements": total_elements,
            "used_cells": used_cells,
            "cells_with_collision": cells_with_collision,
            "load_factor": load_factor,
            "distribution": distribution,
        }
