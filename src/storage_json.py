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

"""JSON-file-based storage backend for chunk metadata and segments."""
import json
import logging
from pathlib import Path
from typing import Optional

from .storage import StorageBackend

logger = logging.getLogger(__name__)


class JsonStorage(StorageBackend):
    """File-based JSON storage in a project cache directory.

    Layout:
      <cache_dir>/analyze/chunk_NNN.json        (step A per-chunk metadata)
      <cache_dir>/segments/seg_GGGG.json        (step B/C/D final segment)
      <cache_dir>/chunk_NNN.json                (legacy back-compat)
    """

    def __init__(self, cache_dir: Path):
        self.cache_dir = Path(cache_dir)
        self.analyze_dir = self.cache_dir / "analyze"
        self.segments_dir = self.cache_dir / "segments"

    def init_schema(self) -> None:
        """Create cache directory structure."""
        for d in [self.cache_dir, self.analyze_dir, self.segments_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def save_chunk_meta(self, chunk_id: int, data: dict) -> None:
        """Save chunk metadata to analyze/chunk_NNN.json."""
        self.init_schema()
        path = self.analyze_dir / f"chunk_{chunk_id:03d}.json"
        try:
            path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as e:
            logger.error(f"Failed to save chunk {chunk_id}: {e}")

    def load_chunk_meta(self, chunk_id: int) -> Optional[dict]:
        """Load chunk metadata from analyze/chunk_NNN.json."""
        path = self.analyze_dir / f"chunk_{chunk_id:03d}.json"
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(f"Failed to load chunk {chunk_id}: {e}")
            return None

    def save_segment_meta(self, segment_id: int, data: dict) -> None:
        """Save segment metadata to segments/seg_GGGG.json."""
        self.init_schema()
        path = self.segments_dir / f"seg_{segment_id:04d}.json"
        try:
            path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as e:
            logger.error(f"Failed to save segment {segment_id}: {e}")

    def load_segment_meta(self, segment_id: int) -> Optional[dict]:
        """Load segment metadata from segments/seg_GGGG.json."""
        path = self.segments_dir / f"seg_{segment_id:04d}.json"
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(f"Failed to load segment {segment_id}: {e}")
            return None

    def delete_chunk(self, chunk_id: int) -> bool:
        """Delete chunk metadata."""
        path = self.analyze_dir / f"chunk_{chunk_id:03d}.json"
        if not path.exists():
            return False
        try:
            path.unlink()
            return True
        except Exception as e:
            logger.error(f"Failed to delete chunk {chunk_id}: {e}")
            return False

    def delete_segment(self, segment_id: int) -> bool:
        """Delete segment metadata."""
        path = self.segments_dir / f"seg_{segment_id:04d}.json"
        if not path.exists():
            return False
        try:
            path.unlink()
            return True
        except Exception as e:
            logger.error(f"Failed to delete segment {segment_id}: {e}")
            return False

    def list_all_segments(self) -> list[dict]:
        """Load all segments in order."""
        if not self.segments_dir.exists():
            return []
        files = sorted(self.segments_dir.glob("seg_*.json"))
        result = []
        for f in files:
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                result.append(data)
            except Exception as e:
                logger.warning(f"Failed to load {f.name}: {e}")
        return result

    def list_all_chunks(self) -> list[dict]:
        """Load all chunks in order."""
        if not self.analyze_dir.exists():
            return []
        files = sorted(self.analyze_dir.glob("chunk_*.json"))
        result = []
        for f in files:
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                result.append(data)
            except Exception as e:
                logger.warning(f"Failed to load {f.name}: {e}")
        return result

    def clear(self) -> None:
        """Delete all JSON files in cache."""
        import shutil
        for d in [self.analyze_dir, self.segments_dir]:
            if d.exists():
                shutil.rmtree(d)
        self.init_schema()

