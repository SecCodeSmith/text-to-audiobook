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
    import soundfile as sf
    import numpy as np
    from scipy import signal
except ImportError:
    sf = None
    np = None
    signal = None

logger = logging.getLogger(__name__)

def denoise(wav_path: Path):
    if sf is None or signal is None:
        logger.warning("Audio processing libraries not available")
        return

    wav_path = Path(wav_path)
    logger.info(f"Denoising: {wav_path}")

    try:
        audio, sr = sf.read(wav_path)

        # Remove sub-bass rumble below 60 Hz
        sos_hp = signal.butter(4, 60, 'hp', fs=sr, output='sos')
        audio = signal.sosfilt(sos_hp, audio)

        # Gentle high-frequency roll-off to reduce harshness / metallic TTS artifacts
        cutoff = min(9000, sr // 2 - 500)
        sos_lp = signal.butter(2, cutoff, 'lp', fs=sr, output='sos')
        audio = signal.sosfilt(sos_lp, audio)

        sf.write(wav_path, audio, sr)
        logger.debug(f"Post-processing complete: {wav_path}")

    except Exception as e:
        logger.error(f"Audio post-processing failed for {wav_path}: {e}")
        raise

