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

from src.markdown_cleaner import clean


def test_strip_headers():
    md = "# Title\nSome text"
    assert "Title" not in clean(md)
    assert "Some text" in clean(md)


def test_strip_bold():
    md = "This is **bold** text"
    result = clean(md)
    assert "bold" in result
    assert "**" not in result


def test_strip_italic():
    md = "This is *italic* text"
    result = clean(md)
    assert "italic" in result
    assert "*" not in result


def test_strip_links():
    md = "Check out [this link](https://example.com)"
    result = clean(md)
    assert "this link" in result
    assert "https://" not in result


def test_preserve_paragraphs():
    md = "First paragraph.\n\nSecond paragraph."
    result = clean(md)
    assert "First paragraph" in result
    assert "Second paragraph" in result


def test_strip_code_fence():
    md = "Text\n```python\ncode\n```\nMore text"
    result = clean(md)
    assert "code" not in result
    assert "Text" in result
    assert "More text" in result


def test_strip_inline_code():
    md = "Use `function()` in the code"
    result = clean(md)
    assert "function()" in result
    assert "`" not in result
