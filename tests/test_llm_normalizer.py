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


from src.llm_normalizer import LLMNormalizer


def test_normalize_returns_dict():
    normalizer = LLMNormalizer("fake_model.gguf")
    normalizer.load()
    result = normalizer.normalize("Sample text")
    assert isinstance(result, dict)
    assert "normalized_text" in result
    assert "emotion" in result
    assert "language" in result
    normalizer.unload()


def test_normalize_without_load():
    normalizer = LLMNormalizer("fake_model.gguf")
    result = normalizer.normalize("Sample text")
    assert isinstance(result, dict)
    assert result["normalized_text"] == "Sample text"
    assert result["emotion"] == "neutral"


def test_cache_file_creation(tmp_path):
    from src.chunker import Chunk

    normalizer = LLMNormalizer("fake_model.gguf")
    normalizer.load()

    chunks = [
        Chunk(text="First text.", ends_paragraph=False),
        Chunk(text="Second text.", ends_paragraph=True),
    ]

    cache_dir = tmp_path / "cache"
    results = normalizer.process_all(chunks, cache_dir)

    assert (cache_dir / "chunk_000.json").exists()
    assert (cache_dir / "chunk_001.json").exists()
    assert len(results) >= 1
    assert all("normalized_text" in r for r in results)

    normalizer.unload()


def test_cache_resumable(tmp_path):
    from src.chunker import Chunk

    normalizer = LLMNormalizer("fake_model.gguf")
    normalizer.load()

    chunks = [
        Chunk(text="First.", ends_paragraph=False),
        Chunk(text="Second.", ends_paragraph=False),
    ]

    cache_dir = tmp_path / "cache"

    normalizer.process_all(chunks, cache_dir)
    cache_file_1 = (cache_dir / "chunk_000.json").stat().st_mtime

    normalizer.process_all(chunks, cache_dir)
    cache_file_2 = (cache_dir / "chunk_000.json").stat().st_mtime

    assert cache_file_1 == cache_file_2

    normalizer.unload()


def test_unload_clears_model():
    normalizer = LLMNormalizer("fake_model.gguf")
    normalizer.load()
    normalizer.unload()
    assert normalizer.llm is None


def test_detect_language_returns_default_without_llm():
    normalizer = LLMNormalizer("fake_model.gguf")
    assert normalizer.detect_language("hola mundo") == LLMNormalizer.DEFAULT_LANGUAGE


def test_detect_language_returns_value_in_supported_set():
    from unittest.mock import MagicMock

    normalizer = LLMNormalizer("fake_model.gguf")
    fake_llm = MagicMock()
    fake_llm.return_value = {"choices": [{"text": '{"language": "spanish"}'}]}
    normalizer.llm = fake_llm
    assert normalizer.detect_language("Hola mundo") == "spanish"


def test_detect_language_falls_back_on_unknown_response():
    from unittest.mock import MagicMock

    normalizer = LLMNormalizer("fake_model.gguf")
    fake_llm = MagicMock()
    fake_llm.return_value = {"choices": [{"text": '{"language": "klingon"}'}]}
    normalizer.llm = fake_llm
    assert normalizer.detect_language("nuqneH") == LLMNormalizer.DEFAULT_LANGUAGE


def test_process_all_records_carry_language(tmp_path):
    from src.chunker import Chunk

    normalizer = LLMNormalizer("fake_model.gguf")
    normalizer.load()
    chunks = [Chunk(text="Hello world.", ends_paragraph=True)]
    cache_dir = tmp_path / "cache"
    results = normalizer.process_all(chunks, cache_dir)
    assert results, "process_all must produce at least one segment"
    for record in results:
        assert "language" in record
        assert record["language"] in LLMNormalizer.SUPPORTED_LANGUAGES
    normalizer.unload()
