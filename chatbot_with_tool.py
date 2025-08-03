import re
import json
import requests
from datetime import datetime
from calculator_tool import calculate
import os
from dotenv import load_dotenv
import nltk
from nltk import word_tokenize, pos_tag


# Ensure you have the necessary NLTK resources downloaded
# Uncomment the following lines if you haven't downloaded these resources yet and do it only once

# import nltk
# nltk.download("punkt")
# nltk.download("averaged_perceptron_tagger")



load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"


def is_math_expression(text: str) -> bool:
    return bool(re.search(r"\d+\s*[\+\-\*/]\s*\d+", text.lower()) or
                re.search(r"(add|plus|sum|subtract|minus|difference|multiply|times|product|divide|divided)", text.lower()))

def extract_math_expression(text: str) -> str:
    text = text.lower().strip()
    conversions = [
        (r'sum\s+of\s+(\d+)\s+and\s+(\d+)', r'\1 + \2'),
        (r'add\s+(\d+)\s+and\s+(\d+)', r'\1 + \2'),
        (r'add\s+(\d+)\s+to\s+(\d+)', r'\2 + \1'),
        (r'subtract\s+(\d+)\s+from\s+(\d+)', r'\2 - \1'),
        (r'(\d+)\s+minus\s+(\d+)', r'\1 - \2'),
        (r'(\d+)\s+plus\s+(\d+)', r'\1 + \2'),
        (r'multiply\s+(\d+)\s+and\s+(\d+)', r'\1 * \2'),
        (r'(\d+)\s+times\s+(\d+)', r'\1 * \2'),
        (r'divide\s+(\d+)\s+by\s+(\d+)', r'\1 / \2'),
        (r'(\d+)\s+divided\s+by\s+(\d+)', r'\1 / \2')
    ]
    for pattern, repl in conversions:
        match = re.search(pattern, text)
        if match:
            return re.sub(pattern, repl, text)
    cleaned = re.sub(r"[^\d\+\-\*/\.]", " ", text)
    return re.sub(r"\s+", " ", cleaned).strip()

def contains_question_word(text: str) -> bool:
    question_words = {"what", "who", "when", "where", "why", "how", "which", "whom", "whose"}
    tokens = word_tokenize(text.lower())
    tagged = pos_tag(tokens)
    return any(word in question_words and tag.startswith("W") for word, tag in tagged)

def is_multi_query(text: str) -> bool:
    return is_math_expression(text) and contains_question_word(text)

def is_greeting(text: str) -> bool:
    return text.lower() in ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]

def build_prompt(user_input: str) -> str:
    return (
        "You are a helpful assistant that always answers step-by-step.\n"
        "Avoid solving direct math calculations.\n"
        f"User question: {user_input}\n"
        "Respond clearly and logically with steps:"
    )

def call_groq_llm(prompt: str, step_by_step: bool = True) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that explains everything step-by-step." if step_by_step else
                       "You are a helpful assistant that answers concisely."
        },
        {"role": "user", "content": prompt}
    ]

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error communicating with Groq: {e}"


def chatbot():
    print("Chatbot with LLM + Calculator Tool\nType 'exit' to quit\n")
    log = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Bot: Goodbye!")
            break

        entry = {
            "timestamp": str(datetime.now()),
            "user_input": user_input
        }

        if is_greeting(user_input):
            response = "Hello! How can I help you today?"
            # entry["tool_used"] = "greeting"

        elif is_multi_query(user_input):
            response = "I'm currently not able to handle multiple questions in a single input. Please ask one at a time."
            # entry["tool_used"] = "none"

        elif is_math_expression(user_input):
            expression = extract_math_expression(user_input)
            try:
                result = calculate(expression)
                response = f"The calculator tool is being used.\nThe result is: {result}"
            except Exception as e:
                response = f"The calculator tool is being used.\nError in calculation: {str(e)}"
            entry["tool_used"] = "calculator"
            # entry["expression"] = expression

        elif contains_question_word(user_input):
            response = call_groq_llm(user_input, step_by_step=False)
            # entry["tool_used"] = "LLM (direct)"

        else:
            prompt = build_prompt(user_input)
            response = call_groq_llm(prompt, step_by_step=True)
            # entry["tool_used"] = "LLM (step-by-step)"

        # print(f"[Tool Used]: {entry['tool_used']}")
        print("Bot:", response)
        print()

        entry["bot_response"] = response
        log.append(entry)

    with open("interaction_logs.json", "w") as f:
        json.dump(log, f, indent=4)
        print("Interaction log saved to interaction_logs.json")

if __name__ == "__main__":
    chatbot()
