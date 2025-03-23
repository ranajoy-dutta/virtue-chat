# Local/Personal Chatbot

This project is a personal, local yet scalable and extendable chatbot application that integrates with a large language model (LLM) to provide conversational AI capabilities. The application is built using Python and leverages various libraries and frameworks to manage the chat interface, database interactions, and LLM integrations.
Another objective is to have this as a project with different reusable components for other side projects (Often serves as a boilderplate / jump starter :) ).    

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Future Improvements](#future-improvements)
- [License](#license)

## Features

- **Multi-Provider LLM Integration**: Supports multiple LLM providers, including Mistral, OpenAI, and Gemini.
- **Chat Interface**: Provides a web-based chat interface using Gradio.
- **Streaming Responses**: Supports both standard and streaming responses from LLMs.
- **Session Management**: Manages chat sessions and stores chat history in a database. TODO: Load historical chats using user login. Currently, though history is saved in database, but gradio relies on browser local storage natively.
- **Configurable**: Easily configurable via YAML files and environment variables.
- **Extensible**: Designed to be easily extended with new LLM providers and additional features.


## Installation

### Clone the repository:

```bash
git clone https://github.com/ranajoy-dutta/virtue.git
cd virtue
```

### Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Set up environment variables:

Create a `.env` file in the root directory and add your API keys and other environment variables:

```env
MISTRAL_API_KEY=your_mistral_api_key
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

## Usage

### Run the chat interface:

```bash
python app.py
```


## Future Improvements

- **Additional LLM Providers**: Integrate more LLM providers such as OpenAI and Gemini.
- **Agents**: TODO:Functionality with custom agents.
- **Documents**: TODO: Add custom documents / Chat with docs / Add docs data to context / Generic RAG.
- **Privacy Layer / PII**: TODO: Scan / Mask / Fake PII data internally and locally before sending it to LLM.
- **Deployment**: TODO: Simplify deployment using docker. 
- **Enhanced UI**: Improve the user interface with more features and better design.
- **User Authentication**: Add user authentication to manage user-specific chat histories.
- **Advanced Memory Management**: Implement more sophisticated memory management strategies.
- **Analytics and Monitoring**: Add analytics and monitoring to track usage and performance.
- **Error Handling**: Improve error handling and logging for better debugging and reliability.
- **Testing**: Add comprehensive unit and integration tests.

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). You are free to use, modify, and distribute this software for non-commercial and commercial purposes, provided that any modifications or derivative works are also licensed under AGPL-3.0. If you use this project in an enterprise setting, attribution to the original author, **Ranajoy Dutta**, is required. See the [LICENSE](./LICENSE) file for more details.

