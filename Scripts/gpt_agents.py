import os
import re
from openai import AzureOpenAI
from dotenv import load_dotenv
from Scripts import speech_agent as speech

load_dotenv()


class _BaseAgent:
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2023-05-15"
    )

    def __init__(self, model="gpt-35-turbo"):
        """
                Constructor for ChatAgent.

                **system_prompt (str, optional):** Explains the role of GPT.

                **temperature (int, optional):** The level of randomness from 0 to 1. Defaults to 0.

                **model (str, optional):** The model to use. Defaults to "gpt-35-turbo".
        """
        self.temperature = 0
        self.model = model

    def chat_completion(self, messages):
        return self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=messages
        )


class ChatAgent(_BaseAgent):

    def __init__(self, system_prompt="You are a friendly assistant!", model="gpt-35-turbo"):
        """
                Constructor for ChatAgent.

                **system_prompt (str, optional):** Explains the role of GPT.

                **randomness (int, optional):** The level of randomness from 0 to 1. Defaults to 0.

                **model (str, optional):** The model to use. Defaults to "gpt-35-turbo".

                **keep_context (bool, optional):** Whether to keep the context. Defaults to False.
        """
        self.keep_context = False
        self.messages = [{"role": "system", "content": system_prompt}]
        self.speech = speech.SpeechAgent()
        super().__init__(model)

    def generate_response(self, user_prompt, conversation_transcript, sentences_count=2):
        # Update chat history with user input
        conversation_transcript.append({"role": "user", "content": f"Respond in up to {sentences_count} sentences: {user_prompt}"})

        self.messages = self.messages + conversation_transcript

        response = super().chat_completion(self.messages)

        assistant_response = response.choices[0].message.content

        conversation_transcript.append({"role": "assistant", "content": assistant_response})

        self._reset_history()

        return assistant_response

    def _reset_history(self):
        self.chat_history = [self.messages[0]]  # Keep the initial system prompt

    def get_history(self):
        return self.messages


class IntentAgent(_BaseAgent):
    def __init__(self, model="gpt-35-turbo"):
        """
                Constructor for ChatAgent.

                **model (str, optional):** The model to use. Defaults to "gpt-35-turbo".
                """
        self.temperature = 0
        self.model = model
        self.system_prompt_condition = {"role": "user", "content": "You are an agent that has the purpose check if"
                                                                   " a condition is met. Only answer in one word"
                                                                   " with yes or no."}
        self.system_prompt_intent = {"role": "user", "content": "You are an agent that has the purpose to understand "
                                                                "the users intent in one short sentence."}
        super().__init__(model)

    def check_intent(self, user_prompt, expected_intent):
        user_message = {"role": "user",
                        "content": f"Answer in one short sentence: What is the users Intent? User: {user_prompt}?"}
        response_content = self.generate_response(user_message)

        user_message = {"role": "user",
                        "content": f"Answer in one word yes or no. Does {response_content} have a similar or equal meaning"
                                   f" as {expected_intent}"}
        response_content = self.generate_response(user_message)

        if "yes" in response_content.lower():
            return True
        return False

    def generate_response(self, user_prompt):
        messages = [self.system_prompt_intent, user_prompt]
        response = super().chat_completion(messages)
        return response.choices[0].message.content


class CommanderAgent(_BaseAgent):
    def __init__(self, context, categories, model="gpt-35-turbo"):
        """
                Constructor for ChatAgent.

                **model (str, optional):** The model to use. Defaults to "gpt-35-turbo".
                """
        self.temperature = 0
        self.model = model
        self.speech = speech.SpeechAgent()
        self.context = context
        self.categories = categories
        super().__init__(model)

    def check_category(self, user_prompt, conversation_transcript):
        system_prompt = {"role": "user", "content": f"You are an agent that has the purpose classify a user "
                                                    f"prompt into a category. The context of you situation is as "
                                                    f"follows: {self.context} Your answer only be the category "
                                                    f"structured like this: "
                                                    f"[Category]"}

        user_prompt = {"role": "user",
                        "content": f"Out of these topics: {self.categories} which topic fits the user_prompt: "
                                   f"{user_prompt}?"}

        messages = [system_prompt] + conversation_transcript + [user_prompt]

        response_content = self.generate_response(messages)

        extracted_response = self.extract_bracket_content(response_content)

        print(f"Category: {extracted_response}")

        return extracted_response

    def generate_response(self, messages):
        response = super().chat_completion(messages)
        return response.choices[0].message.content

    def extract_bracket_content(self, text):
        match = re.search(r'\[(.*?)\]', text, flags=re.IGNORECASE)
        return match.group(1) if match else ''

    def say(self, string):
        self.speech.synthesize_speech(string)

    def start_listening(self):
        return self.speech.start_recognition()

    def stop_listening(self):
        self.speech.stop_recognition()