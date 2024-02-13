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
