# 🍷 Wine E-commerce Assistant
![Architecture](docs/images/architecture.svg)

![Python](https://img.shields.io/badge/Python-3.12-blue)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![LangChain](https://img.shields.io/badge/LangChain-🦜🔗-green)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

> **An intelligent sommelier assistant that listens, thinks, and responds.**
> Designed to guide customers of [Les Celliers de Sion](https://celliers.ch) through an interactive and multimodal shopping experience.

## Project Highlights

This project transforms the classic e-commerce experience into a fluid conversation using an advanced RAG (Retrieval Augmented Generation) architecture.

* **Contextual Intelligence (RAG):** Combines the power of a **LLM** with a vector knowledge base (FAISS) built from PDF sheets and the official website.
* **Voice Interactions:**
    **Input:** Fast audio transcription via **Whisper**.
* **Autonomous Agent (LangGraph):** An agent capable of planning its actions using multiple tools before responding and giving the source of its information.
* **Performance:** Backend optimized with **FastAPI** and package management via **uv**.
* **Interface:** Responsive UI built with **React** and **Vite**.

<img src="docs/images/interface.png" alt="Interface" width="300" style="display: block; margin: 0 auto;" />

---

## Quick Start

### Prerequisites
- Install Ollama 
    - Follow instructions at https://ollama.ai to install it on your system

- For Mac and Linux users, install [zbar](https://pypi.org/project/pyzbar/) (used for Qr code reading): 
    ```bash
    # MacOS
    brew install zbar
    ```
    ```bash
    # Linux 
    sudo apt-get install libzbar0
    ```
    It should be already included in Windows installation.

### Setup and Run
```bash
# Clone the repository
git clone https://github.com/anouillz/Ecommerce-assistant.git
# Navigate to project directory
cd Ecommerce-assistant
```

```bash
# Pull ollama moddel 
ollama pull ministral-3:14b
```

```bash
# Package management
uv sync
# Run backend server
uv run python backend/api.py
```

```bash
# navigate to frontend directory
cd frontend
# install npm and run server
npm install
npm run dev
```

---

## Documentation
You can find more detailed information in the documentation:
- [User Guide](docs/user-guide.md): Instructions for setting up, using, and troubleshooting the assistant.
- [Developer Guide](docs/dev-guide.md): Technical details about the architecture, code structure, and development workflow.