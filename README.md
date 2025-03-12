# 🤖 JAFS: Jarvis Agent Framework System

<p align="center">
  <img src="assets/jafs_logo.png" alt="JAFS AI Logo" width="200"/>
</p>

<p align="center">
  <a href="https://github.com/JoelHJames1/MultiAgentAISystem/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python version"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
  <a href="https://github.com/JoelHJames1/MultiAgentAISystem/blob/main/CONTRIBUTING.md"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg" alt="Contributions welcome"></a>
  <br>
  <a href="https://github.com/JoelHJames1/MultiAgentAISystem/stargazers"><img src="https://img.shields.io/github/stars/JoelHJames1/MultiAgentAISystem.svg?style=social&label=Star" alt="GitHub stars"></a>
  <a href="https://github.com/JoelHJames1/MultiAgentAISystem/network/members"><img src="https://img.shields.io/github/forks/JoelHJames1/MultiAgentAISystem.svg?style=social&label=Fork" alt="GitHub forks"></a>
  <a href="https://github.com/JoelHJames1/MultiAgentAISystem/issues"><img src="https://img.shields.io/github/issues/JoelHJames1/MultiAgentAISystem.svg" alt="GitHub issues"></a>
  <a href="https://makeapullrequest.com"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
</p>

## Table of Contents

- [Introduction](#-introduction)
- [Why JAFS?](#-why-jafs)
- [Features & Capabilities](#-features--capabilities)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Running with Ollama](#-running-with-ollama)
- [Usage Examples](#-usage-examples)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## 🌟 Introduction

**JAFS** (Jarvis Agent Framework System) is a powerful, flexible, and accessible open-source AI agent framework designed to revolutionize task automation. Built with modern AI technologies and best practices, JAFS represents the next generation of AI agent frameworks, offering unparalleled capabilities and ease of use.

JAFS empowers users to create AI agents that can:
- Execute complex tasks through natural language instructions
- Collaborate in multi-agent environments to solve problems
- Interact with web services, documents, and code
- Process multimodal inputs including text, images, and audio
- Adapt to different domains and use cases

Whether you're a developer looking to build AI-powered applications, a researcher exploring agent-based systems, or an enthusiast interested in the latest AI technologies, JAFS provides the tools and flexibility you need to succeed.

## 💡 Why JAFS?

- **Truly Open Source**: No barriers, no invite codes, just pure open-source goodness
- **Hybrid Architecture**: Combines single-agent simplicity with multi-agent power
- **Flexible Model Support**: Works with OpenAI models, open-source models, or your own
- **Comprehensive Tool Ecosystem**: Web automation, document processing, code execution, and more
- **Community-First Design**: Built for contributions and extensions
- **Transparent Operation**: Clear explanations of all agent actions and decisions
- **Cross-Platform**: Works across different operating systems and environments

## ✨ Features & Capabilities

### 🧠 Advanced AI Agent Architecture

- **Hybrid Agent System**: Seamlessly switch between single-agent and multi-agent modes based on task complexity
- **Dynamic Task Planning**: Sophisticated planning system that breaks down complex tasks into manageable steps
- **Adaptive Resource Allocation**: Intelligently allocates computational resources based on task requirements
- **Memory Management**: Short-term and long-term memory systems for context retention across conversations
- **Explainable Actions**: Transparent reasoning and decision-making processes

### 🤝 Multi-Agent Collaboration

- **Specialized Agent Roles**: Pre-defined roles like Researcher, Coder, Planner, and more
- **Custom Role Creation**: Define your own agent roles with specific capabilities and knowledge
- **Inter-Agent Communication**: Structured protocols for efficient agent-to-agent communication
- **Consensus Mechanisms**: Collaborative decision-making through agent voting and consensus
- **Conflict Resolution**: Sophisticated protocols for resolving disagreements between agents

### 🛠️ Comprehensive Tool Ecosystem

- **Web Interaction**:
  - Full browser automation via Playwright
  - Web scraping and data extraction
  - Form filling and submission
  - Authentication handling

- **Information Retrieval**:
  - Search engine integration
  - Wikipedia access
  - News and current events sources
  - Specialized knowledge bases

- **Document Processing**:
  - PDF parsing and analysis
  - Office document handling (Word, Excel, PowerPoint)
  - Image recognition and OCR
  - Data extraction and transformation

- **Code Execution**:
  - Secure Python execution sandbox
  - Multiple language support
  - Package management
  - Output capture and analysis

- **Multimodal Processing**:
  - Image analysis and generation
  - Audio processing and transcription
  - Video analysis and summarization
  - Chart and graph interpretation

### 🔄 Flexible Model Integration

- **OpenAI API Support**: Seamless integration with GPT-4 and newer models
- **Open-Source Models**: Support for Llama, Mistral, and other open-source models via Ollama
- **Local Deployment**: Run models locally for privacy and reduced costs
- **Model Switching**: Automatically select the appropriate model based on task requirements
- **Fallback Mechanisms**: Gracefully handle API issues by switching to alternative models

## 🔧 Installation

JAFS supports multiple installation methods to accommodate different user preferences and environments.

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git

### Method 1: From Source (Recommended for Developers)

```bash
# Clone the repository
git clone https://github.com/JoelHJames1/MultiAgentAISystem.git
cd MultiAgentAISystem

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
PYTHONPATH=$(pwd) python -m jafs.main --task "Hello, world!"
```

## 🚀 Quick Start

Once installed, you can start using JAFS right away:

```bash
# Run JAFS with a simple task
PYTHONPATH=$(pwd) python -m jafs.main --task "Find the latest news about artificial intelligence"

# Run with a specific mode (single, multi, or auto)
PYTHONPATH=$(pwd) python -m jafs.main --mode multi --task "Research quantum computing"

# Run with verbose output
PYTHONPATH=$(pwd) python -m jafs.main --verbose --task "Calculate 2 + 2"
```

## 🤖 Running with Ollama

JAFS has built-in support for running with Ollama, which allows you to use open-source models locally. Here's how to set it up:

### 1. Install Ollama

First, you need to install Ollama on your system. Visit [Ollama's website](https://ollama.ai/) for installation instructions.

### 2. Pull a Model

After installing Ollama, pull a model that you want to use:

```bash
# Pull a model (e.g., qwq:32b, llama3, mistral, etc.)
ollama pull qwq:32b
```

### 3. Configure JAFS to Use Ollama

Edit the `config.yaml` file to use Ollama:

```yaml
# JAFS Configuration File

model:
  provider: ollama
  model_name: qwq:32b  # Replace with your preferred model
  base_url: "http://localhost:11434"  # Default Ollama API URL
  temperature: 0.7

agent:
  name: jafs
  mode: auto  # Options: single, multi, auto
  max_iterations: 10
  memory_capacity: 2000
  verbose: true

tools:
  enabled:
    - calculator
    - search
    - text
    - code

logging:
  level: DEBUG
  file: logs/jafs.log
```

### 4. Run JAFS with Ollama

Now you can run JAFS with Ollama:

```bash
# Run JAFS with Ollama
PYTHONPATH=$(pwd) python -m jafs.main --task "Calculate 2 + 2"
```

### 5. Troubleshooting Ollama Integration

If you encounter issues with Ollama integration:

- Make sure Ollama is running: `ollama serve`
- Verify the model is available: `ollama list`
- Check the base URL in config.yaml matches your Ollama setup
- Ensure the model name in config.yaml matches an available model

## 📋 Usage Examples

### Basic Examples

#### Simple Question Answering

```bash
PYTHONPATH=$(pwd) python -m jafs.main --task "What is the capital of France?"
```

#### Calculations

```bash
PYTHONPATH=$(pwd) python -m jafs.main --task "Calculate 3 * 4 + 5"
```

#### Multi-Agent Mode

```bash
PYTHONPATH=$(pwd) python -m jafs.main --mode multi --task "Research the impact of artificial intelligence on healthcare"
```

## 📚 Documentation

For detailed documentation, visit our [Documentation Site](https://github.com/JoelHJames1/MultiAgentAISystem/docs).

## 👥 Contributing

We welcome contributions from the community! JAFS is designed to be community-driven, and your input helps make it better for everyone.

### Ways to Contribute

- **Code Contributions**: Implement new features, fix bugs, or improve performance
- **Documentation**: Improve or expand documentation, add examples, fix typos
- **Bug Reports**: Report bugs or suggest improvements
- **Feature Requests**: Suggest new features or enhancements
- **Community Support**: Help answer questions and support other users

### Getting Started with Contributing

1. **Fork the Repository**

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/your-username/MultiAgentAISystem.git
cd MultiAgentAISystem
```

2. **Set Up Development Environment**

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. **Create a Branch**

```bash
# Create a branch for your contribution
git checkout -b feature/your-feature-name
```

4. **Make Your Changes**

- Follow the code style guidelines
- Add tests for new functionality
- Update documentation as needed

5. **Submit a Pull Request**

- Push your changes to your fork
- Submit a pull request from your branch to our main branch
- Provide a clear description of the changes and any related issues

## 📝 License

JAFS is released under the [MIT License](LICENSE).

```
MIT License

Copyright (c) 2025 JAFS AI Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
