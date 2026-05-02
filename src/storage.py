# This file is part of text-to-audiobook
#
# text-to-audiobook is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# text-to-audiobook is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Abstract storage backend for chunk metadata and segment persistence."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional


class StorageBackend(ABC):
    """Abstract interface for persisting chunk metadata and segments.

    Implementations must support:
    - Save/load individual chunk metadata
    - Delete chunks and their associated data
    - Export all chunks in canonical form
    - Initialize/migrate storage schema
    """

    @abstractmethod
    def save_segment_meta(self, segment_id: int, data: dict) -> None:
        """Persist a TTS-ready segment record.

        Args:
            segment_id: 0-based index of the segment
            data: dict with keys like normalized_text, emotion, language, source_file, etc.
        """
        pass

    @abstractmethod
    def load_segment_meta(self, segment_id: int) -> Optional[dict]:
        """Load a segment record by ID.

        Returns None if not found or on error.
        """
        pass

    @abstractmethod
    def save_chunk_meta(self, chunk_id: int, data: dict) -> None:
        """Persist analysis-stage chunk metadata (intermediate cache).

        Args:
            chunk_id: 0-based chunk index
            data: dict with keys like segments, language, ends_paragraph, source_file, etc.
        """
        pass

    @abstractmethod
    def load_chunk_meta(self, chunk_id: int) -> Optional[dict]:
        """Load chunk metadata by ID.

        Returns None if not found or on error.
        """
        pass

    @abstractmethod
    def delete_segment(self, segment_id: int) -> bool:
        """Delete a segment record.

        Returns True if deleted, False if not found.
        """
        pass

    @abstractmethod
    def delete_chunk(self, chunk_id: int) -> bool:
        """Delete chunk metadata.

        Returns True if deleted, False if not found.
        """
        pass

    @abstractmethod
    def list_all_segments(self) -> list[dict]:
        """Return all segments in order, preserving IDs.

        Used for assembly stage. Each dict should include segment_id or be
        in a list where index = id.
        """
        pass

    @abstractmethod
    def list_all_chunks(self) -> list[dict]:
        """Return all chunks in order for inspection/migration."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all data from storage (used in tests)."""
        pass

    @abstractmethod
    def init_schema(self) -> None:
        """Initialize storage schema (create tables, directories, etc.)."""
        pass

