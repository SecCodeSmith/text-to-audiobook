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

"""Smoke tests that exercise the whole pipeline with conftest mocks.

These catch broad classes of "the app crashes 5 minutes in" defects: a
broken import in a glue module, a misuse of dict-vs-attribute access, a
removed function reference, a contract change between stages.
"""

import importlib
from pathlib import Path

from src import pipeline


def _write_input_project(input_root: Path, name: str, *files: str) -> Path:
    proj = input_root / name
    proj.mkdir(parents=True, exist_ok=True)
    for i, body in enumerate(files):
        (proj / f"{i}_chapter.md").write_text(body, encoding="utf-8")
    return proj


def test_run_pipeline_end_to_end(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline.config, "INPUT_DIR", tmp_path / "input")
    monkeypatch.setattr(pipeline.config, "OUTPUT_DIR", tmp_path / "output")
    monkeypatch.setattr(pipeline.config, "CACHE_DIR", tmp_path / "cache")

    input_root = tmp_path / "input"
    _write_input_project(
        input_root, "book", "First chapter text. Hello.", "Second chapter. World."
    )

    results = pipeline.run(str(input_root), str(tmp_path / "output"))

    assert isinstance(results, dict)
    assert "book" in results


def test_pipeline_modules_are_importable():
    for mod in (
        "src.pipeline",
        "src.tts_engine",
        "src.llm_normalizer",
        "src.audio_assembler",
        "src.audio_postprocess",
        "src.chunker",
        "src.markdown_cleaner",
        "src.config",
        "src.logging_setup",
    ):
        importlib.import_module(mod)


def test_tts_engine_public_api_present():
    from src.tts_engine import TTSEngine

    engine = TTSEngine()
    for name in (
        "load",
        "unload",
        "synthesize_first",
        "synthesize_with_anchor",
        "process_all",
    ):
        assert callable(
            getattr(engine, name)
        ), f"TTSEngine.{name} missing or not callable"


def test_llm_normalizer_public_api_present():
    from src.llm_normalizer import LLMNormalizer

    norm = LLMNormalizer("nonexistent.gguf")
    for name in (
        "load",
        "unload",
        "normalize",
        "normalize_text",
        "analyze_emotions",
        "fill_context",
        "sort_files",
        "process_all",
    ):
        assert callable(getattr(norm, name)), f"LLMNormalizer.{name} missing"


def test_pipeline_public_api_present():
    for name in (
        "run",
        "prepare_segments",
        "generate_audio",
        "discover_projects",
        "load_cached_segments",
        "prepare_segments_for_project",
        "generate_audio_for_project",
    ):
        assert callable(getattr(pipeline, name)), f"pipeline.{name} missing"
