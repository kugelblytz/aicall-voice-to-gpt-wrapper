# ChatAgent Class Usage Guide

This guide will help you understand how to use the `ChatAgent` class in your Python projects. This class is designed to interact with the Azure OpenAI API and generate chat completions.

## Prerequisites

- Python 3.9 or higher
- Azure OpenAI Python SDK

## Environment Variables

Before using the `ChatAgent` class, ensure that you have set the following environment variables:

- `AZURE_OPENAI_ENDPOINT`: The endpoint URL for the Azure OpenAI API.
- `AZURE_OPENAI_KEY`: Your Azure OpenAI API key.

The variables can be set in the .env file.

## Class Initialization

To initialize the `ChatAgent` class, you need to provide the following parameters:

- `system_prompt`: The initial system prompt.
- `temperature` (optional): Controls randomness in the model's responses. Default is 0.
- `model` (optional): The model to use for generating responses. Default is "gpt-35-turbo".
- `keep_context` (optional): If set to True, the chat history is kept between calls to `chat_completion`. Default is False.

```python
agent = ChatAgent(system_prompt="Hello, how can I assist you today?")
```

## Methods

`chat_completion(user_prompt)`
Generates a response from the model based on the user's prompt.

```pyhton
response = agent.chat_completion("What's the weather like?")
```

`get_history()`
Returns the chat history.

```pyhton
conversation_history = agent.get_history()
```

`_reset_history()`
Resets the chat history, keeping only the initial system prompt. This method is private and should not be called directly.
