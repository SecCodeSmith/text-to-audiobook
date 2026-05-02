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

"""SQLite-based storage backend for chunk metadata and segments."""
import json
import logging
import sqlite3
from pathlib import Path
from typing import Optional

from .storage import StorageBackend

logger = logging.getLogger(__name__)


class SqliteStorage(StorageBackend):
    """SQLite storage for chunk metadata and TTS segments.

    Tables:
      chunks(chunk_id INTEGER PRIMARY KEY, data TEXT)
      segments(segment_id INTEGER PRIMARY KEY, data TEXT)

    Data is stored as JSON strings for flexibility.
    """

    def __init__(self, cache_dir: Path):
        self.cache_dir = Path(cache_dir)
        self.db_path = self.cache_dir / "storage.db"
        self._conn: Optional[sqlite3.Connection] = None

    def _get_conn(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self._conn is None:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def init_schema(self) -> None:
        """Create tables if they don't exist."""
        conn = self._get_conn()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    chunk_id INTEGER PRIMARY KEY,
                    data TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS segments (
                    segment_id INTEGER PRIMARY KEY,
                    data TEXT NOT NULL
                )
            """)
            conn.commit()
        except Exception as e:
            logger.error(f"Failed to initialize schema: {e}")
            raise

    def save_chunk_meta(self, chunk_id: int, data: dict) -> None:
        """Save chunk metadata to SQLite."""
        conn = self._get_conn()
        try:
            json_data = json.dumps(data, ensure_ascii=False)
            conn.execute(
                "INSERT OR REPLACE INTO chunks (chunk_id, data) VALUES (?, ?)",
                (chunk_id, json_data),
            )
            conn.commit()
        except Exception as e:
            logger.error(f"Failed to save chunk {chunk_id}: {e}")

    def load_chunk_meta(self, chunk_id: int) -> Optional[dict]:
        """Load chunk metadata from SQLite."""
        conn = self._get_conn()
        try:
            cursor = conn.execute(
                "SELECT data FROM chunks WHERE chunk_id = ?",
                (chunk_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return json.loads(row[0])
        except Exception as e:
            logger.error(f"Failed to load chunk {chunk_id}: {e}")
            return None

    def save_segment_meta(self, segment_id: int, data: dict) -> None:
        """Save segment metadata to SQLite."""
        conn = self._get_conn()
        try:
            json_data = json.dumps(data, ensure_ascii=False)
            conn.execute(
                "INSERT OR REPLACE INTO segments (segment_id, data) VALUES (?, ?)",
                (segment_id, json_data),
            )
            conn.commit()
        except Exception as e:
            logger.error(f"Failed to save segment {segment_id}: {e}")

    def load_segment_meta(self, segment_id: int) -> Optional[dict]:
        """Load segment metadata from SQLite."""
        conn = self._get_conn()
        try:
            cursor = conn.execute(
                "SELECT data FROM segments WHERE segment_id = ?",
                (segment_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return json.loads(row[0])
        except Exception as e:
            logger.error(f"Failed to load segment {segment_id}: {e}")
            return None

    def delete_chunk(self, chunk_id: int) -> bool:
        """Delete chunk metadata from SQLite."""
        conn = self._get_conn()
        try:
            cursor = conn.execute(
                "DELETE FROM chunks WHERE chunk_id = ?",
                (chunk_id,),
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to delete chunk {chunk_id}: {e}")
            return False

    def delete_segment(self, segment_id: int) -> bool:
        """Delete segment metadata from SQLite."""
        conn = self._get_conn()
        try:
            cursor = conn.execute(
                "DELETE FROM segments WHERE segment_id = ?",
                (segment_id,),
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to delete segment {segment_id}: {e}")
            return False

    def list_all_chunks(self) -> list[dict]:
        """Return all chunks ordered by chunk_id."""
        conn = self._get_conn()
        try:
            cursor = conn.execute(
                "SELECT chunk_id, data FROM chunks ORDER BY chunk_id"
            )
            return [
                {**json.loads(row[1]), "chunk_id": row[0]}
                for row in cursor.fetchall()
            ]
        except Exception as e:
            logger.error(f"Failed to list chunks: {e}")
            return []

    def list_all_segments(self) -> list[dict]:
        """Return all segments ordered by segment_id."""
        conn = self._get_conn()
        try:
            cursor = conn.execute(
                "SELECT segment_id, data FROM segments ORDER BY segment_id"
            )
            return [
                {**json.loads(row[1]), "segment_id": row[0]}
                for row in cursor.fetchall()
            ]
        except Exception as e:
            logger.error(f"Failed to list segments: {e}")
            return []

    def clear(self) -> None:
        """Clear all data from storage."""
        conn = self._get_conn()
        try:
            conn.execute("DELETE FROM chunks")
            conn.execute("DELETE FROM segments")
            conn.commit()
        except Exception as e:
            logger.error(f"Failed to clear storage: {e}")

    def close(self) -> None:
        """Close the database connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

