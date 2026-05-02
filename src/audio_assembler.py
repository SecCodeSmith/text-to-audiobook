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
from pathlib import Path

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None

from . import config

logger = logging.getLogger(__name__)


def assemble(chunk_wavs: list[Path], chunk_meta: list, out_path: Path) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if AudioSegment is None:
        logger.warning("pydub not available, skipping assembly")
        return out_path

    logger.info(f"Assembling {len(chunk_wavs)} audio chunks")

    try:
        combined = None

        for i, wav_path in enumerate(chunk_wavs):
            logger.debug(f"Loading chunk {i}: {wav_path}")
            audio = AudioSegment.from_wav(str(wav_path))

            if combined is None:
                combined = audio
            else:
                combined = combined.append(audio, crossfade=config.CROSSFADE_MS)

            if i < len(chunk_meta):
                meta = chunk_meta[i]
                ends_paragraph = (
                    meta.get("ends_paragraph", False)
                    if isinstance(meta, dict)
                    else getattr(meta, "ends_paragraph", False)
                )
                silence_ms = (
                    config.SILENCE_AFTER_PARAGRAPH_MS
                    if ends_paragraph
                    else config.SILENCE_AFTER_PERIOD_MS
                )
                silence = AudioSegment.silent(duration=silence_ms)
                combined = combined.append(silence)

        if combined is None:
            logger.warning("No chunks to combine")
            return out_path

        wav_out = out_path.with_suffix(".wav")
        combined.export(str(wav_out), format="wav")
        logger.info(f"Exported WAV: {wav_out}")

        mp3_out = out_path.with_suffix(".mp3")
        combined.export(str(mp3_out), format="mp3", bitrate="192k")
        logger.info(f"Exported MP3: {mp3_out}")

        return mp3_out

    except Exception as e:
        logger.error(f"Assembly failed: {e}")
        raise
