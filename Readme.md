# GPT Voice Wrapper Library Usage Guide

Welcome to the GPT Voice Wrapper Library! This library is designed to streamline the process of creating specialized chat agents for handling diverse tasks within a simulated hardware store environment. With the introduction of multiple expert agents and a commanding agent, this library offers a structured approach to managing customer inquiries and directing them to the appropriate expert based on their needs.

---

## Prerequisites

- Python 3.9 or higher
- Access to an appropriate AI model API (e.g., Azure OpenAI, GPT-3, or equivalent)

---

## Installation

Ensure you have Python installed on your system and your preferred AI model API set up. The library does not include API access; you must obtain this separately from your AI provider.

---

## Environment Setup

1. **Clone the Repository**: Clone the project repository to your local machine.

2. **.env File**: Copy the provided `.env` file in your project root directory.

3. **Load Environment Variables**: Ensure your script loads the environment variables from the `.env` file at runtime, using a library such as `python-dotenv`.

---

## Quick Start

1. **Define Agents**: Create instances of `ChatAgent` for different expertise areas within your domain, such as general assistance, wood, fasteners, and payment queries.

2. **Initialize Commander and Intent Agents**: Set up a `CommanderAgent` to manage user interactions and direct them to the appropriate expert agent. Use an `IntentAgent` to detect specific user intents, like wanting to end the conversation.

3. **Implement Conversation Logic**: Use the provided script structure to facilitate a conversation flow, directing user prompts to the relevant agent and handling their responses.

---

## Detailed Guide

### Agent Initialization

Each `ChatAgent` needs a unique system prompt that defines its role and expertise. For example:

```python
general_agent = gpt.ChatAgent("You are the general assistant in a hardware store...")
```

### `CommanderAgent`

The `CommanderAgent` serves as the orchestrator of user interactions, efficiently directing inquiries to the relevant expert agents. It makes decisions based on the context of the conversation and predefined categories, ensuring that users are connected with the most appropriate source of assistance.

```python
commander = gpt.CommanderAgent(context, categories)
```

### `IntentAgent`
The `IntentAgent` specializes in recognizing specific user intents, such as the desire to conclude the conversation. By identifying these intents, the IntentAgent facilitates smooth and intuitive interactions, enhancing the overall user experience.

```python
intent_agent = gpt.IntentAgent()
```

### Handling User Inputs
The system is designed to continuously process user inputs, dynamically categorizing inquiries and identifying intents to ensure that each request is addressed by the most suitable agent. This loop forms the core of the conversational flow, enabling responsive and intelligent dialogue management.

```python
if __name__ == "__main__":
    # Main loop to handle conversation flow
```

### Methods

- **`generate_response(user_prompt, conversation_transcript, answer_sentence_count)`**: This method allows agents to generate contextually relevant responses based on the user's prompt and the ongoing conversation history. The `answer_sentence_count` parameter specifies the number of sentences in the response, allowing for control over the verbosity of the agent's replies.

- **`check_category(speech_input, conversation_transcript)`**: Utilized by the `CommanderAgent` to determine the appropriate category for each user inquiry. This method analyzes the user's speech input and the existing conversation transcript to accurately route the query to the corresponding expert agent.

- **`check_intent(speech_input, target_intent)`**: Employs the `IntentAgent's` capabilities to detect specific user intents within the conversation. This method is crucial for identifying when users express particular desires or actions, such as wanting to conclude the conversation, facilitating tailored responses and actions based on these intents.

### Examples
For practical implementation guidance, refer to the script example provided with the library. This example offers a detailed look at setting up the agents and orchestrating a simulated conversation within a hardware store context, demonstrating the library's capabilities in action.

### Conclusion
This library represents a significant advancement in building conversational AI agents, offering a flexible and structured framework for handling specialized tasks. Through the collaborative efforts of the CommanderAgent, IntentAgent, and various expert ChatAgents, it provides a robust solution for managing complex customer inquiries with nuance and efficiency.

---

## Explanation of main.py example

```python
from Scripts import gpt_agents as gpt

conversation_transcript = []

general_agent = gpt.ChatAgent("You are the general assistant in a hardware store. Your task is to greet and extract from the customer what is the problem they are trying to solve. You cannot provide solutions")

wood_agent = gpt.ChatAgent("You are the wood expert. You can provide help on how to solve the customers problem using 4mm,8mm, and 10mm wood. Available in MDF and plywood you cannot provide solutions")

fasteners_agent = gpt.ChatAgent("You are a fastener expert. You can provide help on how to solve the customers problem using m4, m6 and m8 bolts or wood screws available in standard sizes. You cannot provide solutions")

payment_agent = gpt.ChatAgent("You are a payment agent.You can assist customers with payment problems when paying with card, cash or other payment methods. You cannot provide solutions")

context = "You the general assistant in a hardware store. You are deciding which expert the user should talk to."
categories = "Wood, Fasteners, Payments, General"
commander = gpt.CommanderAgent(context, categories)

intent_agent =  gpt.IntentAgent()


def switch_case(case_value, user_prompt, conversation_transcript):
    if case_value == 'Wood':
        response = wood_agent.generate_response(user_prompt, conversation_transcript, 2)
        return response
    elif case_value == 'Fasteners':
        response = fasteners_agent.generate_response(user_prompt, conversation_transcript, 2)
        return response
    elif case_value == 'Payments':
        response = payment_agent.generate_response(user_prompt, conversation_transcript, 2)
        return response
    else:
        response = general_agent.generate_response(user_prompt, conversation_transcript, 2)
        return response


if __name__ == "__main__":
    commander.say("Hey there, how can I help?")
    while True:
        speech_input = commander.start_listening()
        category = commander.check_category(speech_input, conversation_transcript)
        intent_met = intent_agent.check_intent(speech_input, "Wants to say goodbye.")
        print(f"Want's to say goodbye is {intent_met}.")
        if not intent_met:
            response = switch_case(category, speech_input, conversation_transcript)
            print(f"{category} Agent says: {response}")
            commander.say(response)
        else:
            commander.say("I hope I was able to assist you. Goodbye!")
            break
```


This script initializes a conversational AI system with multiple specialized agents designed for handling various aspects of customer service in a virtual hardware store environment. Here's a breakdown of its components and workflow:

1. **Agent Initialization**: Four distinct `ChatAgent` instances are created, each specialized in a different area: general assistance, wood, fasteners, and payments. These agents are designed to understand and respond to customer inquiries within their respective domains.

2. **CommanderAgent Setup**: The `CommanderAgent` is initialized with a general context and a list of categories. It serves as the primary interface for user interactions, directing inquiries to the appropriate expert agent based on the conversation's context.

3. **IntentAgent Setup**: An `IntentAgent` is initialized to detect specific user intents, such as the desire to end the conversation.

4. **Conversation Logic**: The `switch_case` function routes the user's inquiry to the relevant expert agent based on the detected category. Each agent generates a response considering the user's prompt and the conversation history.

5. **Main Loop**: The script enters a loop where it continuously listens for user input, categorizes the inquiry, checks for specific intents (like saying goodbye), and generates responses through the appropriate agent. The loop breaks when the user expresses the intent to conclude the conversation.

This script exemplifies how to orchestrate a conversational AI system with specialized roles for a more nuanced and effective customer service experience.

---