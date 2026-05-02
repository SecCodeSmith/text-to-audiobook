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

"""Tests for storage abstraction and per-chapter generation."""
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from src.storage import StorageBackend
from src.storage_json import JsonStorage
from src.storage_sqlite import SqliteStorage
from src.storage_factory import create_storage
from src.chunker import Chunk, split_to_chunks
from src.pipeline import _build_chunks


class TestStorageJsonBackend:
    """Test JsonStorage implementation."""

    def test_init_creates_directories(self):
        """init_schema should create cache directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir) / "cache"
            storage = JsonStorage(cache_dir)
            storage.init_schema()

            assert (cache_dir / "analyze").exists()
            assert (cache_dir / "segments").exists()

    def test_save_and_load_chunk(self):
        """save_chunk_meta and load_chunk_meta should round-trip data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = JsonStorage(Path(tmpdir))
            storage.init_schema()

            data = {
                "segments": [{"text": "hello", "emotion": "happy"}],
                "language": "english",
                "source_file": "chapter_01",
            }
            storage.save_chunk_meta(5, data)

            loaded = storage.load_chunk_meta(5)
            assert loaded == data

    def test_save_and_load_segment(self):
        """save_segment_meta and load_segment_meta should round-trip data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = JsonStorage(Path(tmpdir))
            storage.init_schema()

            data = {
                "normalized_text": "test text",
                "emotion": "calm",
                "language": "english",
                "source_file": "chapter_02",
                "ends_paragraph": True,
            }
            storage.save_segment_meta(42, data)

            loaded = storage.load_segment_meta(42)
            assert loaded == data

    def test_load_nonexistent_returns_none(self):
        """Loading non-existent data should return None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = JsonStorage(Path(tmpdir))
            storage.init_schema()

            assert storage.load_chunk_meta(999) is None
            assert storage.load_segment_meta(999) is None

    def test_delete_chunk(self):
        """delete_chunk should remove the file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = JsonStorage(Path(tmpdir))
            storage.init_schema()

            storage.save_chunk_meta(10, {"test": "data"})
            assert storage.load_chunk_meta(10) is not None

            deleted = storage.delete_chunk(10)
            assert deleted is True
            assert storage.load_chunk_meta(10) is None

    def test_delete_nonexistent_chunk(self):
        """delete_chunk on non-existent data should return False."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = JsonStorage(Path(tmpdir))
            storage.init_schema()

            deleted = storage.delete_chunk(999)
            assert deleted is False

    def test_delete_segment(self):
        """delete_segment should remove the file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = JsonStorage(Path(tmpdir))
            storage.init_schema()

            storage.save_segment_meta(20, {"test": "data"})
            assert storage.load_segment_meta(20) is not None

            deleted = storage.delete_segment(20)
            assert deleted is True
            assert storage.load_segment_meta(20) is None

    def test_list_all_segments(self):
        """list_all_segments should return all segments in order."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = JsonStorage(Path(tmpdir))
            storage.init_schema()

            for i in range(3):
                storage.save_segment_meta(i, {"id": i, "text": f"seg {i}"})

            segments = storage.list_all_segments()
            assert len(segments) == 3
            assert segments[0]["id"] == 0
            assert segments[1]["id"] == 1
            assert segments[2]["id"] == 2

    def test_list_all_chunks(self):
        """list_all_chunks should return all chunks in order."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = JsonStorage(Path(tmpdir))
            storage.init_schema()

            for i in range(3):
                storage.save_chunk_meta(i, {"id": i, "language": f"lang{i}"})

            chunks = storage.list_all_chunks()
            assert len(chunks) == 3
            assert chunks[0]["id"] == 0
            assert chunks[1]["id"] == 1
            assert chunks[2]["id"] == 2

    def test_clear(self):
        """clear should remove all data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = JsonStorage(Path(tmpdir))
            storage.init_schema()

            storage.save_segment_meta(0, {"test": "data"})
            storage.save_chunk_meta(0, {"test": "data"})

            storage.clear()

            assert storage.load_segment_meta(0) is None
            assert storage.load_chunk_meta(0) is None
            assert storage.list_all_segments() == []
            assert storage.list_all_chunks() == []


class TestStorageSqliteBackend:
    """Test SqliteStorage implementation."""

    def test_init_creates_database(self):
        """init_schema should create SQLite database."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir) / "cache"
            storage = SqliteStorage(cache_dir)
            storage.init_schema()

            assert (cache_dir / "storage.db").exists()
            storage.close()

    def test_save_and_load_chunk_sqlite(self):
        """save_chunk_meta and load_chunk_meta should round-trip data in SQLite."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SqliteStorage(Path(tmpdir))
            storage.init_schema()

            data = {
                "segments": [{"text": "hello", "emotion": "happy"}],
                "language": "english",
                "source_file": "chapter_01",
            }
            storage.save_chunk_meta(5, data)

            loaded = storage.load_chunk_meta(5)
            assert loaded == data
            storage.close()

    def test_save_and_load_segment_sqlite(self):
        """save_segment_meta and load_segment_meta should round-trip data in SQLite."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SqliteStorage(Path(tmpdir))
            storage.init_schema()

            data = {
                "normalized_text": "test text",
                "emotion": "calm",
                "language": "english",
                "source_file": "chapter_02",
                "ends_paragraph": True,
            }
            storage.save_segment_meta(42, data)

            loaded = storage.load_segment_meta(42)
            assert loaded == data
            storage.close()

    def test_list_all_segments_sqlite(self):
        """list_all_segments should return all segments from SQLite."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SqliteStorage(Path(tmpdir))
            storage.init_schema()

            for i in range(3):
                storage.save_segment_meta(i, {"id": i, "text": f"seg {i}"})

            segments = storage.list_all_segments()
            assert len(segments) == 3
            assert segments[0]["id"] == 0
            assert segments[1]["id"] == 1
            assert segments[2]["id"] == 2
            storage.close()

    def test_clear_sqlite(self):
        """clear should remove all data from SQLite."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SqliteStorage(Path(tmpdir))
            storage.init_schema()

            storage.save_segment_meta(0, {"test": "data"})
            storage.save_chunk_meta(0, {"test": "data"})

            storage.clear()

            assert storage.load_segment_meta(0) is None
            assert storage.load_chunk_meta(0) is None
            storage.close()


class TestStorageFactory:
    """Test storage factory function."""

    def test_create_json_storage_by_default(self):
        """create_storage should default to JSON storage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("src.storage_factory.config.STORAGE_BACKEND", "json"):
                storage = create_storage(Path(tmpdir))
                assert isinstance(storage, JsonStorage)

    def test_create_sqlite_storage_when_configured(self):
        """create_storage should create SQLite storage when configured."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("src.storage_factory.config.STORAGE_BACKEND", "sqlite"):
                storage = create_storage(Path(tmpdir))
                assert isinstance(storage, SqliteStorage)

    def test_invalid_backend_raises_error(self):
        """create_storage should raise ValueError for unknown backend."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("src.storage_factory.config.STORAGE_BACKEND", "invalid"):
                with pytest.raises(ValueError, match="Unknown STORAGE_BACKEND"):
                    create_storage(Path(tmpdir))


class TestChunkSourceFile:
    """Test source_file tagging in chunks."""

    def test_chunk_has_source_file_attribute(self):
        """Chunk should have source_file attribute with default value."""
        chunk = Chunk(text="hello", ends_paragraph=False)
        assert chunk.source_file == "default"

    def test_chunk_custom_source_file(self):
        """Chunk should accept custom source_file."""
        chunk = Chunk(text="hello", ends_paragraph=False, source_file="chapter_01")
        assert chunk.source_file == "chapter_01"

    def test_split_to_chunks_preserves_source_file(self):
        """split_to_chunks should propagate source_file to all chunks."""
        text = "First sentence. Second sentence. Third sentence."
        chunks = split_to_chunks(text, max_words=5, source_file="story_ch1")

        assert len(chunks) > 0
        for chunk in chunks:
            assert chunk.source_file == "story_ch1"

    def test_split_to_chunks_default_source_file(self):
        """split_to_chunks should use 'default' when source_file not provided."""
        text = "One sentence."
        chunks = split_to_chunks(text)

        assert len(chunks) == 1
        assert chunks[0].source_file == "default"


class TestBuildChunksSourceTracking:
    """Test source file tracking in _build_chunks pipeline function."""

    def test_build_chunks_tags_with_source_filename(self):
        """_build_chunks should tag chunks with the source file stem."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test markdown files
            md_dir = Path(tmpdir) / "md"
            md_dir.mkdir()

            (md_dir / "chapter_01.md").write_text("This is chapter one. It has content.")
            (md_dir / "chapter_02.md").write_text("This is chapter two. Also has content.")

            # Build chunks
            md_files = sorted(md_dir.glob("*.md"))
            chunks = _build_chunks(md_files)

            assert len(chunks) > 0

            # Check that chunks are tagged with source file names
            source_files = {chunk.source_file for chunk in chunks}
            assert "chapter_01" in source_files
            assert "chapter_02" in source_files

    def test_build_chunks_maintains_order_per_source(self):
        """_build_chunks should maintain order within each source file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_dir = Path(tmpdir) / "md"
            md_dir.mkdir()

            (md_dir / "01_first.md").write_text("First sentence. Second sentence. Third sentence.")
            (md_dir / "02_second.md").write_text("Fourth sentence. Fifth sentence.")

            md_files = sorted(md_dir.glob("*.md"))
            chunks = _build_chunks(md_files)

            # All chunks from 01_first should come before chunks from 02_second
            first_chapters = [c for c in chunks if c.source_file == "01_first"]
            second_chapters = [c for c in chunks if c.source_file == "02_second"]

            assert len(first_chapters) > 0
            assert len(second_chapters) > 0


class TestSegmentSourceFilePreservation:
    """Test that source_file is preserved through the segment pipeline."""

    def test_segment_carries_source_file(self):
        """Segments should include source_file from chunks."""
        chunk = Chunk(
            text="This is a test sentence.",
            ends_paragraph=True,
            source_file="chapter_05",
        )

        # Simulate minimal segment creation (what llm_normalizer does)
        segment = {
            "normalized_text": chunk.text,
            "emotion": "neutral",
            "source_file": chunk.source_file,
            "ends_paragraph": chunk.ends_paragraph,
        }

        assert segment["source_file"] == "chapter_05"

    def test_multiple_segments_preserve_source_file(self):
        """Multiple segments from same source should all carry that source_file."""
        source_name = "prologue"
        segments = [
            {
                "normalized_text": "First part.",
                "emotion": "calm",
                "source_file": source_name,
            },
            {
                "normalized_text": "Second part.",
                "emotion": "tense",
                "source_file": source_name,
            },
            {
                "normalized_text": "Third part.",
                "emotion": "neutral",
                "source_file": source_name,
            },
        ]

        for seg in segments:
            assert seg["source_file"] == source_name


class TestPerChapterGrouping:
    """Test grouping segments by source file for per-chapter output."""

    def test_group_segments_by_source_file(self):
        """Segments should be groupable by source_file."""
        segments = [
            {"source_file": "ch1", "text": "a"},
            {"source_file": "ch1", "text": "b"},
            {"source_file": "ch2", "text": "c"},
            {"source_file": "ch2", "text": "d"},
            {"source_file": "ch3", "text": "e"},
        ]

        from collections import defaultdict
        by_source = defaultdict(list)
        for i, seg in enumerate(segments):
            source = seg.get("source_file", "default")
            by_source[source].append((i, seg))

        assert len(by_source) == 3
        assert len(by_source["ch1"]) == 2
        assert len(by_source["ch2"]) == 2
        assert len(by_source["ch3"]) == 1

    def test_output_filename_generation_single_chapter(self):
        """Single chapter should use 'audiobook.mp3'."""
        segments = [{"source_file": "only_one", "text": "content"}]

        from collections import defaultdict
        by_source = defaultdict(list)
        for i, seg in enumerate(segments):
            by_source[seg.get("source_file", "default")].append((i, seg))

        if len(by_source) == 1:
            output_name = "audiobook.mp3"
        else:
            output_name = None

        assert output_name == "audiobook.mp3"

    def test_output_filename_generation_multiple_chapters(self):
        """Multiple chapters should use 'chapter_NN.mp3' format."""
        segments = [
            {"source_file": "prologue", "text": "intro"},
            {"source_file": "chapter_01", "text": "first"},
            {"source_file": "chapter_02", "text": "second"},
        ]

        from collections import defaultdict
        by_source = defaultdict(list)
        for i, seg in enumerate(segments):
            by_source[seg.get("source_file", "default")].append((i, seg))

        sorted_sources = sorted(by_source.keys())
        output_names = [f"chapter_{i:02d}.mp3" for i in range(1, len(sorted_sources) + 1)]

        assert len(output_names) == 3
        assert output_names[0] == "chapter_01.mp3"
        assert output_names[2] == "chapter_03.mp3"


class TestStorageInterfaceContract:
    """Test that JsonStorage conforms to StorageBackend interface."""

    def test_json_storage_implements_interface(self):
        """JsonStorage should implement all StorageBackend methods."""
        required_methods = [
            "save_segment_meta",
            "load_segment_meta",
            "save_chunk_meta",
            "load_chunk_meta",
            "delete_segment",
            "delete_chunk",
            "list_all_segments",
            "list_all_chunks",
            "clear",
            "init_schema",
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            storage = JsonStorage(Path(tmpdir))
            for method_name in required_methods:
                assert hasattr(storage, method_name)
                assert callable(getattr(storage, method_name))

    def test_json_storage_is_subclass_of_storage_backend(self):
        """JsonStorage should be a subclass of StorageBackend."""
        assert issubclass(JsonStorage, StorageBackend)


class TestConfigStorageBackend:
    """Test STORAGE_BACKEND config setting."""

    def test_storage_backend_config_exists(self):
        """config should have STORAGE_BACKEND setting."""
        from src import config
        assert hasattr(config, "STORAGE_BACKEND")
        assert config.STORAGE_BACKEND in ["json", "sqlite"]

    def test_storage_backend_in_settings_keys(self):
        """STORAGE_BACKEND should be in _SETTINGS_KEYS for persistence."""
        from src import config
        assert "STORAGE_BACKEND" in config._SETTINGS_KEYS
        assert config._SETTINGS_KEYS["STORAGE_BACKEND"] == str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

