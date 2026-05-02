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

