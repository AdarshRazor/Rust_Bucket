# Bhashini Client

[![PyPI version](https://badge.fury.io/py/bhashini-client.svg)](https://badge.fury.io/py/bhashini-client)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful and easy-to-use Python client for **Bhashini**, India's AI-led language translation platform. This library provides a simple interface to access **Automatic Speech Recognition (ASR)**, **Neural Machine Translation (NMT)**, and **Text-to-Speech (TTS)** services.

---

## 🚀 Features

- **ASR (Automatic Speech Recognition)**: Convert audio to text in multiple Indian languages.
- **NMT (Neural Machine Translation)**: Translate text between various Indian languages and English.
- **TTS (Text-to-Speech)**: Convert text to natural-sounding speech.
- **Service Discovery**: Easily list and find available models and services.

## 📦 Installation

Install the package via pip:

```bash
pip install bhashini-client
```

## 🛠 Usage

### Initialization

First, import the client and initialize it with your API key.

```python
from bhashini_client import BhashiniClient

# Initialize with your Bhashini API Key
client = BhashiniClient(api_key="YOUR_API_KEY")
```

---

### 1. Automatic Speech Recognition (ASR)

Convert audio files (from a URL) into text.

#### Parameters

| Parameter        | Type   | Required | Description                                                |
| :--------------- | :----- | :------- | :--------------------------------------------------------- |
| `audio_url`      | `str`  | **Yes**  | Publicly accessible URL of the audio file.                 |
| `source_lang`    | `str`  | **Yes**  | Language code of the audio (e.g., `'hi'`, `'en'`, `'te'`). |
| `serviceId`      | `str`  | No       | Specific model ID to use.                                  |
| `samplingRate`   | `int`  | No       | Sampling rate of the audio (e.g., `16000`, `44100`).       |
| `preProcessors`  | `list` | No       | List of pre-processing steps.                              |
| `postProcessors` | `list` | No       | List of post-processing steps.                             |

#### Example

```python
# Basic ASR
text = client.asr("https://example.com/audio.wav", "te")
print(f"Transcribed Text: {text}")

# Advanced ASR with specific service and sampling rate
text = client.asr(
    "https://example.com/audio.wav",
    "te",
    serviceId="bhashini/ai4bharat/conformer-multilingual-asr",
    samplingRate=44100
)
```

---

### 2. Neural Machine Translation (NMT)

Translate text from one language to another.

#### Parameters

| Parameter        | Type   | Required | Description                                          |
| :--------------- | :----- | :------- | :--------------------------------------------------- |
| `text`           | `str`  | **Yes**  | The text to translate.                               |
| `source_lang`    | `str`  | **Yes**  | Source language code (e.g., `'en'`).                 |
| `target_lang`    | `str`  | **Yes**  | Target language code (e.g., `'hi'`).                 |
| `serviceId`      | `str`  | No       | Specific model ID to use.                            |
| `numTranslation` | `int`  | No       | Number of translations to return.                    |
| `preProcessors`  | `list` | No       | List of pre-processing steps (e.g., `['glossary']`). |
| `postProcessors` | `list` | No       | List of post-processing steps.                       |

#### Example

```python
# Basic NMT: English -> Hindi
translation = client.nmt("Hello, how are you?", "en", "hi")
print(f"Translation: {translation}")

# NMT with processors
translation = client.nmt(
    "What are you doing?",
    "en",
    "hi",
    preProcessors=["glossary"]
)
```

---

### 3. Text-to-Speech (TTS)

Convert text into audio.

#### Parameters

| Parameter        | Type    | Required | Description                                                       |
| :--------------- | :------ | :------- | :---------------------------------------------------------------- |
| `text`           | `str`   | **Yes**  | The text to convert to speech.                                    |
| `source_lang`    | `str`   | **Yes**  | Language code of the text.                                        |
| `gender`         | `str`   | No       | Voice gender (`'male'` or `'female'`). Default: `'male'`.         |
| `format_`        | `str`   | No       | Audio format (e.g., `'wav'`, `'mp3'`). Default: `'wav'`.          |
| `save_to`        | `str`   | No       | File path to save the output audio (e.g., `'output.wav'`).        |
| `serviceId`      | `str`   | No       | Specific model ID to use.                                         |
| `speed`          | `float` | No       | Speed of speech (0.1 to 1.99).                                    |
| `samplingRate`   | `int`   | No       | Audio sampling rate (e.g., `24000`).                              |
| `return_base64`  | `bool`  | No       | If `True`, returns base64 string instead of saving/returning URL. |
| `preProcessors`  | `list`  | No       | List of pre-processing steps.                                     |
| `postProcessors` | `list`  | No       | List of post-processing steps.                                    |

#### Example

```python
# Basic TTS - Save to file
audio_path = client.tts("मेरा नाम विहिर है", "hi", save_to="output.wav")
print(f"Audio saved at: {audio_path}")

# TTS with specific gender and speed
client.tts(
    "Hello World",
    "en",
    gender="female",
    speed=0.9,
    save_to="hello_female.wav"
)

# TTS returning base64
base64_audio = client.tts("Hello", "en", return_base64=True)
```

---

### 🔍 Service Discovery

Find available services and models for different languages.

```python
# List NMT models for English to Gujarati
services = client.list_nmt_services("en", "gu")
print(services)

# List ASR models for Hindi
asr_services = client.list_asr_services("hi")

# List TTS models for Hindi
tts_services = client.list_tts_services("hi")

# Get details about a specific service
info = client.get_service_info("ai4bharat/conformer-hi-gpu--t4")
print(info)
```

## 📄 License

This project is licensed under the MIT License.
