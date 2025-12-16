# User Guide

## Introduction
This document will help you set up, use, and troubleshoot the assistant to ensure a seamless experience.

---

## Installation
### Prerequisites
Before you begin, ensure you have the following installed:
- **Python 3.12+**
- **Node.js 18+**
- **Ollama** 
  - Follow the instructions at [Ollama.ai](https://ollama.ai) to install it.

---

## Usage

### Accessing the Application
- Start the backend server and the frontend as mentionned in the [Quick Start](../README.md#quick-start) section.
- Open your browser and navigate to `http://localhost:5173/`.

### Using the Assistant
1. **Voice Input**: Click the microphone icon to start speaking your query. Make sure to speak clearly and slowly. Once done, click the icon again to stop recording. Your audio will be transcribed and processed. The transcription may contain some spelling mistakes depending on the audio quality.
2. **Text Input**: Alternatively, you can type your questions directly into the input box and hit enter.


---
## Features

1. **Wine Pairing Suggestions**:
   - Ask the assistant for wine recommendations based on food.
   - Example: "What wine pairs well with raclette?"

2. **Wine Details**:
   - Retrieve detailed information about specific wines.
   - Example: "Tell me more about Pinot Noir."

3. **QR Code and Video Retrieval**:
   - Check if a wine has a QR code or video available.
   - Example: "Is there a video for Fendant?"

---

## Troubleshooting

### Common Issues

1. **Backend Not Starting**:
   - Ensure Ollama is installed and the `ministral-3:14b` model is pulled.
   - Check for missing Python dependencies and reinstall:
     ```bash
     uv sync
     ```

2. **Frontend Not Starting**:
   - Ensure all Node.js dependencies are installed:
     ```bash
     npm install
     ```

3. **Model Not Found**:
   - Verify the `ministral-3:14b` model is available in Ollama:
     ```bash
     ollama list
     ```

4. **Agent loading infinite loop**:
   - Refreshing the frontend page should resolve this issue. If it persists, restart the backend server.


---

## Contact
For further assistance, please contact the project team or open an issue on GitHub: [Ecommerce Assistant Issues](https://github.com/anouillz/Ecommerce-assistant/issues).