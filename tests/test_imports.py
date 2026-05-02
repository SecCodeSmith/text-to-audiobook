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

"""Real-import smoke tests.

Surfaces missing or version-broken runtime dependencies before any
pipeline code runs. Bypasses the mock injections in conftest.py with a
session-scoped fixture that pops every mocked module from sys.modules
exactly once. After that, normal imports return the real package and
sys.modules is populated correctly for the remaining tests.
"""
import importlib
import sys

import pytest


_MOCKED_BY_CONFTEST = (
    "torch",
    "transformers",
    "qwen_tts",
    "soundfile",
    "noisereduce",
    "scipy",
    "scipy.signal",
    "pydub",
    "customtkinter",
    "natsort",
    "huggingface_hub",
    "llama_cpp",
)


@pytest.fixture(scope="module", autouse=True)
def _restore_real_imports():
    """Drop conftest mocks once and let subsequent imports load the real packages."""
    saved = {name: sys.modules.pop(name, None) for name in _MOCKED_BY_CONFTEST}
    # Also drop project modules so they re-import bound to the real deps.
    project_mods = [m for m in list(sys.modules) if m.startswith("src.")]
    saved_project = {m: sys.modules.pop(m) for m in project_mods}
    yield
    # Restore conftest mocks so other test modules continue to see them.
    for name, mod in saved.items():
        if mod is not None:
            sys.modules[name] = mod
        else:
            sys.modules.pop(name, None)
    for name, mod in saved_project.items():
        sys.modules[name] = mod
        # Re-attach to parent package so `import parent.child` returns the
        # original module (not the v3 imported during this fixture's tests).
        if "." in name:
            parent_name, _, leaf = name.rpartition(".")
            parent = sys.modules.get(parent_name)
            if parent is not None:
                setattr(parent, leaf, mod)


@pytest.mark.parametrize(
    "module_name, required_attr",
    [
        ("torch", "cuda"),
        ("numpy", "ndarray"),
        ("transformers", "AutoModel"),
        ("qwen_tts", "Qwen3TTSModel"),
        ("soundfile", "write"),
        ("noisereduce", "reduce_noise"),
        ("scipy.signal", "butter"),
        ("pydub", "AudioSegment"),
        ("natsort", "natsorted"),
        ("huggingface_hub", "hf_hub_download"),
        ("llama_cpp", "Llama"),
        ("regex", "compile"),
    ],
)
def test_dependency_imports(module_name, required_attr):
    mod = importlib.import_module(module_name)
    assert hasattr(mod, required_attr), (
        f"{module_name} is installed but is missing attribute {required_attr!r}"
    )


def test_qwen_tts_has_required_generation_methods():
    qwen_tts = importlib.import_module("qwen_tts")
    cls = qwen_tts.Qwen3TTSModel
    for method in ("from_pretrained", "generate_voice_design",
                   "generate_voice_clone", "generate_custom_voice"):
        assert hasattr(cls, method), (
            f"Qwen3TTSModel.{method} is missing — package version drifted?"
        )


def test_transformers_version_is_recent_enough():
    transformers = importlib.import_module("transformers")
    version = transformers.__version__
    parts = version.split(".")
    major, minor = int(parts[0]), int(parts[1])
    assert (major, minor) >= (4, 45), (
        f"transformers {version} is too old; need >= 4.45.0 (see requirements.txt)"
    )


def test_qwen_tts_registers_qwen3_tts_model_type():
    """Qwen3TTSConfig must declare model_type='qwen3_tts' so wrapper registration works."""
    from qwen_tts.core.models.modeling_qwen3_tts import Qwen3TTSConfig
    assert Qwen3TTSConfig.model_type == "qwen3_tts"


def test_project_modules_importable():
    """Catches syntax errors / broken imports in src/ even without dedicated tests."""
    for mod in (
        "src.config",
        "src.tts_engine",
        "src.llm_normalizer",
        "src.pipeline",
        "src.audio_assembler",
        "src.audio_postprocess",
        "src.chunker",
        "src.markdown_cleaner",
        "src.logging_setup",
    ):
        sys.modules.pop(mod, None)
        importlib.import_module(mod)

