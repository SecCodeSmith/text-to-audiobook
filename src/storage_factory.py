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

"""Factory for creating storage backend instances based on config."""

import logging
from pathlib import Path

from . import config
from .storage import StorageBackend
from .storage_json import JsonStorage
from .storage_sqlite import SqliteStorage

logger = logging.getLogger(__name__)


def create_storage(cache_dir: Path) -> StorageBackend:
    """Create a storage backend instance based on config.STORAGE_BACKEND setting.

    Args:
        cache_dir: Directory for storage (JSON files or SQLite DB)

    Returns:
        StorageBackend instance (JsonStorage or SqliteStorage)

    Raises:
        ValueError: If STORAGE_BACKEND is set to an unknown value
    """
    backend = getattr(config, "STORAGE_BACKEND", "json").lower().strip()

    if backend == "json":
        logger.debug("Using JSON storage backend")
        return JsonStorage(cache_dir)
    elif backend == "sqlite":
        logger.debug("Using SQLite storage backend")
        return SqliteStorage(cache_dir)
    else:
        raise ValueError(
            f"Unknown STORAGE_BACKEND: {backend!r}. " f"Must be 'json' or 'sqlite'."
        )
