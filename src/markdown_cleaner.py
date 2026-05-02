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


def clean(md: str) -> str:
    lines = md.split("\n")
    cleaned = []

    in_code_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code_fence = not in_code_fence
            continue

        if in_code_fence:
            continue

        if re.match(r"^\s*#+\s", line):
            continue

        line = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", line)

        line = re.sub(r"\*\*([^\*]+)\*\*", r"\1", line)
        line = re.sub(r"\*([^\*]+)\*", r"\1", line)
        line = re.sub(r"__([^_]+)__", r"\1", line)
        line = re.sub(r"_([^_]+)_", r"\1", line)

        line = re.sub(r"`([^`]+)`", r"\1", line)

        line = re.sub(r"https?://[^\s]+", "", line)

        line = re.sub(r"<[^>]+>", "", line)

        if line.strip():
            cleaned.append(line)
        elif cleaned and cleaned[-1] != "":
            cleaned.append("")

    text = "\n".join(cleaned)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
