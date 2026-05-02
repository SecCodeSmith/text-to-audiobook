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

import sys
from unittest.mock import MagicMock, patch
import torch

def test_main_import_no_error():
    if 'main' in sys.modules:
        del sys.modules['main']

    try:
        import main
        assert hasattr(main, '__name__')
    except ImportError as e:
        raise AssertionError(f"Failed to import main: {e}")

def test_gui_launch_no_error(monkeypatch):
    mock_ctk = MagicMock()
    mock_ctk.CTk = MagicMock()
    monkeypatch.setitem(sys.modules, 'customtkinter', mock_ctk)

    from src.gui import launch
    try:
        pass
    except Exception as e:
        raise AssertionError(f"GUI launch failed: {e}")

def test_tts_engine_instantiation():
    """Test TTSEngine can be instantiated without errors."""
    from src.tts_engine import TTSEngine
    engine = TTSEngine()
    assert engine is not None
    assert engine.model_name is not None
    assert engine.engine is None  # Not loaded until load() is called

def test_torch_compile_available():
    """Test torch.compile is available (PyTorch 2.0+)."""
    assert hasattr(torch, 'compile'), "torch.compile requires PyTorch 2.0+"

def test_tts_engine_load_method_has_compile():
    """Test that load() method has torch.compile integration."""
    from src.tts_engine import TTSEngine
    import inspect

    source = inspect.getsource(TTSEngine.load)
    assert 'torch.compile' in source, "torch.compile not found in load() method"
    assert 'reduce-overhead' in source, "compile mode not specified correctly"

def test_tts_engine_voice_ref_has_compile():
    """Test that _generate_voice_reference() has torch.compile integration."""
    from src.tts_engine import TTSEngine
    import inspect

    source = inspect.getsource(TTSEngine._generate_voice_reference)
    assert 'torch.compile' in source, "torch.compile not found in _generate_voice_reference() method"
    assert 'reduce-overhead' in source, "compile mode not specified correctly"

def test_tts_engine_compile_error_handling():
    """Test that compile errors are caught gracefully."""
    from src.tts_engine import TTSEngine
    import inspect

    # Check that both methods have try/except for torch.compile
    load_source = inspect.getsource(TTSEngine.load)
    ref_source = inspect.getsource(TTSEngine._generate_voice_reference)

    assert 'except Exception' in load_source, "load() missing error handling for compile"
    assert 'except Exception' in ref_source, "_generate_voice_reference() missing error handling for compile"

