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

from pathlib import Path

from src.audio_assembler import assemble
from src.chunker import Chunk


def test_assemble_returns_path(tmp_path):
    chunk_wavs = [tmp_path / f"chunk_{i}.wav" for i in range(3)]
    for wav in chunk_wavs:
        wav.write_bytes(b"fake wav")

    chunk_meta = [
        Chunk(text="First.", ends_paragraph=False),
        Chunk(text="Second.", ends_paragraph=True),
        Chunk(text="Third.", ends_paragraph=False),
    ]

    out_path = tmp_path / "output.mp3"
    result = assemble(chunk_wavs, chunk_meta, out_path)

    assert isinstance(result, Path)


def test_assemble_silence_gaps(tmp_path):
    chunk_wavs = [tmp_path / f"chunk_{i}.wav" for i in range(2)]
    for wav in chunk_wavs:
        wav.write_bytes(b"fake wav")

    chunk_meta = [
        Chunk(text="First.", ends_paragraph=False),
        Chunk(text="Second.", ends_paragraph=True),
    ]

    out_path = tmp_path / "output.mp3"
    result = assemble(chunk_wavs, chunk_meta, out_path)

    assert result is not None
