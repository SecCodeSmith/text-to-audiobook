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

import re
from dataclasses import dataclass

@dataclass
class Chunk:
    text: str
    ends_paragraph: bool
    source_file: str = "default"

def split_to_chunks(text: str, max_words: int = 499, source_file: str = "default") -> list[Chunk]:
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z"\'])', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    chunks = []
    current_chunk = []
    current_words = 0

    for i, sentence in enumerate(sentences):
        words = len(sentence.split())

        if current_words + words > max_words and current_chunk:
            chunks.append((current_chunk, False))
            current_chunk = [sentence]
            current_words = words
        else:
            current_chunk.append(sentence)
            current_words += words

    if current_chunk:
        chunks.append((current_chunk, False))

    paragraphs = text.split('\n\n')
    para_texts = [p.strip() for p in paragraphs if p.strip()]

    result = []
    for chunk_text_list, _ in chunks:
        chunk_text = ' '.join(chunk_text_list)
        ends_para = False

        for para in para_texts:
            if chunk_text.rstrip() == para.rstrip() or para.endswith(chunk_text.split()[-1] if chunk_text.split() else ''):
                ends_para = True
                break

        result.append(Chunk(text=chunk_text, ends_paragraph=ends_para, source_file=source_file))

    return result

