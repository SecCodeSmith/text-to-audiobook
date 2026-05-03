# License Information

This project incorporates several open-source libraries. Below is a comprehensive list of all dependencies and their respective licenses.

## Project License

text to audiobook is provided under the [AGPL License](../LICENSE).

---

## Third-Party Dependencies

### Core ML/Audio Libraries

#### 1. **PyTorch (torch)**
- **Version**: >=2.4.0
- **License**: BSD 3-Clause
- **Homepage**: https://pytorch.org/
- **Description**: Deep learning framework
- **License Text**: See https://github.com/pytorch/pytorch/blob/master/LICENSE

#### 2. **Transformers**
- **Version**: >=4.45.0
- **License**: Apache License 2.0
- **Homepage**: https://github.com/huggingface/transformers
- **Description**: State-of-the-art NLP models and tools
- **License Text**: See https://github.com/huggingface/transformers/blob/main/LICENSE

#### 3. **Qwen-TTS**
- **Version**: >=0.1.1
- **License**: Apache License 2.0
- **Homepage**: https://github.com/QwenLM/Qwen-TTS
- **Description**: Alibaba Qwen text-to-speech model
- **License Text**: See https://github.com/QwenLM/Qwen-TTS/blob/main/LICENSE

#### 4. **Llama-cpp-python**
- **Version**: >=0.3.0
- **License**: MIT
- **Homepage**: https://github.com/abetlen/llama-cpp-python
- **Description**: Python bindings for llama.cpp
- **License Text**: See https://github.com/abetlen/llama-cpp-python/blob/master/LICENSE

#### 5. **NumPy**
- **Version**: >=1.26.0
- **License**: BSD 3-Clause
- **Homepage**: https://numpy.org/
- **Description**: Numerical computing library
- **License Text**: See https://github.com/numpy/numpy/blob/main/LICENSE.txt

#### 6. **SciPy**
- **Version**: >=1.13.0
- **License**: BSD 3-Clause
- **Homepage**: https://scipy.org/
- **Description**: Scientific computing library
- **License Text**: See https://github.com/scipy/scipy/blob/main/LICENSE.txt

#### 7. **HuggingFace Hub**
- **Version**: >=0.23.0
- **License**: Apache License 2.0
- **Homepage**: https://github.com/huggingface/huggingface_hub
- **Description**: Client library for HuggingFace Hub
- **License Text**: See https://github.com/huggingface/huggingface_hub/blob/main/LICENSE

### Audio Processing

#### 8. **Soundfile**
- **Version**: >=0.12.1
- **License**: BSD 3-Clause
- **Homepage**: https://github.com/bastibe/SoundFile
- **Description**: Read/write sound files to NumPy arrays
- **License Text**: See https://github.com/bastibe/SoundFile/blob/master/LICENSE

#### 9. **Pydub**
- **Version**: >=0.25.1
- **License**: MIT
- **Homepage**: https://github.com/jiaaro/pydub
- **Description**: Simple audio manipulation
- **License Text**: See https://github.com/jiaaro/pydub/blob/master/LICENSE

#### 10. **Mutagen**
- **Version**: >=1.46.0
- **License**: MIT
- **Homepage**: https://github.com/quodlibet/mutagen
- **Description**: Audio metadata tagging library
- **License Text**: See https://github.com/quodlibet/mutagen/blob/master/LICENSE

#### 11. **Noisereduce**
- **Version**: >=3.0.3
- **License**: MIT
- **Homepage**: https://github.com/timsainb/noisereduce
- **Description**: Noise reduction using spectral gating
- **License Text**: See https://github.com/timsainb/noisereduce/blob/master/LICENSE

### Utilities

#### 12. **Accelerate**
- **Version**: >=1.11.0
- **License**: Apache License 2.0
- **Homepage**: https://github.com/huggingface/accelerate
- **Description**: Distributed training/inference acceleration
- **License Text**: See https://github.com/huggingface/accelerate/blob/main/LICENSE

#### 13. **Safetensors**
- **Version**: >=0.4.5
- **License**: Apache License 2.0
- **Homepage**: https://github.com/huggingface/safetensors
- **Description**: Safe serialization format for ML models
- **License Text**: See https://github.com/huggingface/safetensors/blob/main/LICENSE

#### 14. **Regex**
- **Version**: >=2024.9.11
- **License**: Apache License 2.0
- **Homepage**: https://github.com/regex-go/regex
- **Description**: Alternative regex implementation with more features
- **License Text**: See https://github.com/regex-go/regex/blob/master/LICENSE

#### 15. **Natsort**
- **Version**: >=8.4.0
- **License**: MIT
- **Homepage**: https://github.com/SethMMorton/natsort
- **Description**: Natural sorting for Python
- **License Text**: See https://github.com/SethMMorton/natsort/blob/master/LICENSE

#### 16. **CustomTkinter**
- **Version**: >=5.2.2
- **License**: MIT
- **Homepage**: https://github.com/TomSchimansky/CustomTkinter
- **Description**: Modern dark mode customizable tkinter UI library
- **License Text**: See https://github.com/TomSchimansky/CustomTkinter/blob/master/LICENSE

### Testing

#### 17. **Pytest**
- **Version**: >=8.3.0
- **License**: MIT
- **Homepage**: https://pytest.org/
- **Description**: Testing framework
- **License Text**: See https://github.com/pytest-dev/pytest/blob/main/LICENSE

#### 18. **Pytest-mock**
- **Version**: >=3.14.0
- **License**: MIT
- **Homepage**: https://github.com/pytest-dev/pytest-mock
- **Description**: Pytest plugin for mocking
- **License Text**: See https://github.com/pytest-dev/pytest-mock/blob/master/LICENSE

---

## License Summary

| License Type | Count | Libraries |
|---|---|---|
| MIT | 9 | pydub, noisereduce, natsort, customtkinter, pytest, pytest-mock, llama-cpp-python, mutagen |
| Apache 2.0 | 7 | transformers, qwen-tts, accelerate, safetensors, regex, huggingface_hub |
| BSD 3-Clause | 4 | torch, numpy, scipy, soundfile |

---

## Obtaining Full License Texts

For the complete license text of any dependency, you can:

1. Visit the project's GitHub repository (links provided above)
2. Check the installed package in your virtual environment:
   ```bash
   pip show <package-name>
   ```
3. Access the license through PyPI: `https://pypi.org/project/<package-name>/`

---

## Compliance Notes

- All dependencies use permissive open-source licenses (MIT, Apache 2.0, BSD)
- These licenses allow commercial and private use
- Modifications must retain copyright and license notices
- No warranty is provided for any third-party library

For questions regarding licensing, please contact: admin@seccodesmith.pl

---

*Last Updated: 2026-05-03*
