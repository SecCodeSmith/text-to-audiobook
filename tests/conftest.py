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
import json
from unittest.mock import MagicMock, patch
import numpy as np
import pytest

sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent))

def mock_from_pretrained(*args, **kwargs):
    model = MagicMock()
    model.device = 'cpu'
    model.to = MagicMock(return_value=model)
    model.generate = MagicMock(return_value=[np.random.randn(48000).astype(np.float32)])
    return model

def mock_auto_processor(*args, **kwargs):
    processor = MagicMock()
    processor.return_value = {
        'input_ids': np.array([[1, 2, 3]]),
        'attention_mask': np.array([[1, 1, 1]])
    }
    processor.__call__ = processor.return_value
    processor.to = MagicMock(return_value=processor)
    return processor

def mock_llama_init(*args, **kwargs):
    instance = MagicMock()
    instance.return_value = {
        'choices': [{'text': json.dumps({
            "normalized_text": "Sample normalized text",
            "emotion": "neutral",
            "detected_emotions": ["neutral"],
            "language": "english"
        })}]
    }
    instance.__call__ = instance.return_value
    return instance

mock_torch = MagicMock()
mock_torch.cuda.is_available.return_value = False
mock_torch.cuda.empty_cache.return_value = None
mock_torch.float16 = MagicMock()
sys.modules['torch'] = mock_torch

mock_llama_cpp = MagicMock()
mock_llama_cpp.Llama = mock_llama_init
sys.modules['llama_cpp'] = mock_llama_cpp

def mock_hf_hub_download(*args, **kwargs):
    from pathlib import Path
    local_dir = kwargs.get('local_dir')
    filename = kwargs.get('filename', 'model.gguf')
    if local_dir:
        Path(local_dir).mkdir(parents=True, exist_ok=True)
        return str(Path(local_dir) / filename)
    return f"/tmp/{filename}"

mock_hf_hub = MagicMock()
mock_hf_hub.hf_hub_download = mock_hf_hub_download
sys.modules['huggingface_hub'] = mock_hf_hub

mock_hf = MagicMock()
mock_hf.AutoModel.from_pretrained = mock_from_pretrained
mock_hf.AutoProcessor.from_pretrained = mock_auto_processor
sys.modules['transformers'] = mock_hf


def mock_qwen3_tts_from_pretrained(*args, **kwargs):
    wrapper = MagicMock()
    wrapper.model = MagicMock()
    wrapper.model.device = 'cpu'
    wrapper.processor = MagicMock()
    wrapper.generate = MagicMock(
        return_value=([np.zeros(48000, dtype=np.float32)], 24000)
    )
    wrapper.generate_voice_design = MagicMock(
        return_value=([np.zeros(48000, dtype=np.float32)], 24000)
    )
    wrapper.generate_voice_clone = MagicMock(
        return_value=([np.zeros(48000, dtype=np.float32)], 24000)
    )
    wrapper.generate_custom_voice = MagicMock(
        return_value=([np.zeros(48000, dtype=np.float32)], 24000)
    )
    return wrapper


mock_qwen_tts = MagicMock()
mock_qwen_tts.Qwen3TTSModel = MagicMock()
mock_qwen_tts.Qwen3TTSModel.from_pretrained = mock_qwen3_tts_from_pretrained
mock_qwen_tts.Qwen3TTSModel.generate_voice_design = MagicMock()
mock_qwen_tts.Qwen3TTSModel.generate_voice_clone = MagicMock()
mock_qwen_tts.Qwen3TTSModel.generate_custom_voice = MagicMock()
sys.modules['qwen_tts'] = mock_qwen_tts

mock_sf = MagicMock()
mock_sf.write = MagicMock()
mock_sf.read = MagicMock(return_value=(np.random.randn(48000).astype(np.float32), 24000))
sys.modules['soundfile'] = mock_sf

mock_nr = MagicMock()
mock_nr.reduce_noise = MagicMock(side_effect=lambda y, sr, stationary: y)
sys.modules['noisereduce'] = mock_nr

mock_scipy = MagicMock()
mock_signal = MagicMock()
mock_signal.butter = MagicMock(return_value=np.array([[1, 0, 0], [1, 0, 0]]))
mock_signal.sosfilt = MagicMock(side_effect=lambda sos, data: data)
mock_scipy.signal = mock_signal
sys.modules['scipy'] = mock_scipy
sys.modules['scipy.signal'] = mock_signal

class MockAudioSegment:
    def __init__(self, duration=2000):
        self.duration_seconds = duration / 1000.0
        self.data = b'fake audio data'

    @staticmethod
    def from_wav(path):
        return MockAudioSegment(2000)

    @staticmethod
    def silent(duration=500):
        return MockAudioSegment(duration)

    def append(self, other, crossfade=80):
        return MockAudioSegment(
            int(self.duration_seconds * 1000) + int(other.duration_seconds * 1000)
        )

    def export(self, path, format='mp3', bitrate=None):
        pass

mock_pydub = MagicMock()
mock_pydub.AudioSegment = MockAudioSegment
sys.modules['pydub'] = mock_pydub

mock_ctk = MagicMock()

class MockCTk:
    def __init__(self):
        pass
    def mainloop(self):
        pass
    def pack(self, **kwargs):
        return self
    def configure(self, **kwargs):
        pass

mock_ctk.CTk = MockCTk
mock_ctk.CTkFrame = MagicMock
mock_ctk.CTkLabel = MagicMock
mock_ctk.CTkButton = MagicMock
mock_ctk.CTkTextbox = MagicMock
mock_ctk.CTkProgressBar = MagicMock
mock_ctk.set_appearance_mode = MagicMock()
mock_ctk.set_default_color_theme = MagicMock()
sys.modules['customtkinter'] = mock_ctk

mock_tk = MagicMock()
mock_tk.filedialog = MagicMock()
sys.modules['tkinter'] = mock_tk

mock_natsort = MagicMock()
mock_natsort.natsorted = lambda x: sorted(x)
sys.modules['natsort'] = mock_natsort

@pytest.fixture
def sample_text():
    return "This is the first sentence. This is the second sentence. This is the third sentence."

@pytest.fixture
def sample_chunks():
    from src.chunker import Chunk
    return [
        Chunk(text="First chunk text.", ends_paragraph=False),
        Chunk(text="Second chunk text.", ends_paragraph=True),
    ]

@pytest.fixture
def tmp_wav_files(tmp_path):
    files = []
    for i in range(3):
        wav_file = tmp_path / f"chunk_{i:03d}.wav"
        wav_file.write_bytes(b"fake wav data")
        files.append(wav_file)
    return files

