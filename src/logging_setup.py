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

import logging
from logging.handlers import RotatingFileHandler

from . import config

_gui_callback = None
_console_handler: logging.Handler | None = None
_file_handler: logging.Handler | None = None


class GUIHandler(logging.Handler):
    def emit(self, record):
        if _gui_callback:
            try:
                msg = self.format(record)
                _gui_callback(msg)
            except Exception:
                self.handleError(record)


def bootstrap():
    global _console_handler, _file_handler
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    formatter = logging.Formatter(config.LOG_FORMAT)

    _console_handler = logging.StreamHandler()
    _console_handler.setLevel(logging.INFO)
    _console_handler.setFormatter(formatter)
    root.addHandler(_console_handler)

    _file_handler = RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=config.LOG_MAX_BYTES,
        backupCount=config.LOG_BACKUP_COUNT,
    )
    _file_handler.setLevel(logging.DEBUG)
    _file_handler.setFormatter(formatter)
    root.addHandler(_file_handler)


def attach_gui_handler(callback):
    global _gui_callback
    _gui_callback = callback
    root = logging.getLogger()
    gui_h = GUIHandler()
    gui_h.setFormatter(logging.Formatter(config.LOG_FORMAT))
    root.addHandler(gui_h)


def set_levels(console_level: str = "INFO", file_level: str = "DEBUG") -> None:
    """Reconfigure log levels on the live handlers (called from Settings popup)."""
    if _console_handler is not None:
        _console_handler.setLevel(getattr(logging, console_level.upper(), logging.INFO))
    if _file_handler is not None:
        _file_handler.setLevel(getattr(logging, file_level.upper(), logging.DEBUG))
