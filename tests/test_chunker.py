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

from src.chunker import split_to_chunks, Chunk

def test_chunks_under_max_words():
    text = "First sentence. Second sentence. Third sentence."
    chunks = split_to_chunks(text, max_words=10)
    for chunk in chunks:
        word_count = len(chunk.text.split())
        assert word_count < 11, f"Chunk exceeds max_words: {word_count}"

def test_chunks_end_with_sentence_boundary():
    text = "This is sentence one. This is sentence two. This is sentence three."
    chunks = split_to_chunks(text)
    for chunk in chunks:
        text_stripped = chunk.text.rstrip()
        last_char = text_stripped[-1] if text_stripped else ''
        assert last_char in ['.', '!', '?'], f"Chunk doesn't end in sentence boundary: {text_stripped}"

def test_single_short_text():
    text = "Short text."
    chunks = split_to_chunks(text)
    assert len(chunks) >= 1
    assert chunks[0].text.strip() == "Short text."

def test_paragraph_flag():
    text = "First paragraph.\n\nSecond paragraph."
    chunks = split_to_chunks(text)
    assert len(chunks) > 0
    for chunk in chunks:
        assert isinstance(chunk.ends_paragraph, bool)

def test_empty_text():
    text = ""
    chunks = split_to_chunks(text)
    assert len(chunks) == 0

def test_very_long_sentence():
    long_sentence = "This is a very long sentence that contains many words " * 30 + "."
    chunks = split_to_chunks(long_sentence, max_words=50)
    assert len(chunks) > 0

