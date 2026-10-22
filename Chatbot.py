
import json
import re
import random
from pathlib import Path

# Get the folder containing chatbot.py
BASE_DIR = Path(__file__).resolve().parent
FAQ_FILE = BASE_DIR / "sample_faq.json"


def load_faq():
    """Load the supplied greetings and FAQs from JSON."""
    try:
        with open(FAQ_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"Error: {FAQ_FILE.name} was not found.")
        print("Place sample_faq.json beside chatbot.py.")
        raise SystemExit(1)

    except json.JSONDecodeError as error:
        print("Error: The JSON file is invalid:", error)
        raise SystemExit(1)

    if not isinstance(data, dict):
        print("Error: The JSON root must be an object.")
        raise SystemExit(1)

    if not isinstance(data.get("greetings"), list):
        print("Error: Missing or invalid greetings list.")
        raise SystemExit(1)

    if not isinstance(data.get("faqs"), list):
        print("Error: Missing or invalid faqs list.")
        raise SystemExit(1)

    for faq in data["faqs"]:
        if (
            not isinstance(faq, dict)
            or not isinstance(faq.get("question"), str)
            or not isinstance(faq.get("answer"), str)
        ):
            print("Error: Each FAQ needs a question and answer.")
            raise SystemExit(1)

    return data


def normalize_text(text):
    """Convert input to lowercase and normalize whitespace."""
    return " ".join(text.lower().strip().split())


def is_greeting(message, greetings):
    """Check whether the user entered a greeting."""
    for greeting in greetings:
        pattern = (
            r"(?<!\w)"
            + re.escape(normalize_text(greeting))
            + r"(?!\w)"
        )

        if re.search(pattern, message, re.IGNORECASE):
            return True

    return False


def find_faqs(message, faqs):
    """Match questions using keywords and regular expressions."""

    # Each pattern identifies the topic of a supplied FAQ.
    rules = [
        (
            r"\b(hours?|opening|closing|open|close|operation|operating)\b",
            r"\bhours?\b|\boperation\b",
        ),
        (
            r"\b(internship|project|submit|submission|github|repository|repo)\b",
            r"\binternship\b|\bproject\b|\bsubmit\b",
        ),
        (
            r"\b(certificates?|certification|issued|receive|received)\b",
            r"\bcertificate\b",
        ),
    ]

    matched = []

    for user_pattern, faq_pattern in rules:
        if re.search(user_pattern, message, re.IGNORECASE):
            for faq in faqs:
                if re.search(
                    faq_pattern, faq["question"], re.IGNORECASE
                ):
                    if faq not in matched:
                        matched.append(faq)
                    break

    return matched


def get_response(message, data):
    """Identify the user's intent and prepare a response."""

    # Handle greetings.
    if is_greeting(message, data["greetings"]):
        greeting = random.choice(data["greetings"])
        return f"{greeting.capitalize()}! Welcome to the assistant."

    # Handle questions from the supplied JSON file.
    matched_faqs = find_faqs(message, data["faqs"])

    if matched_faqs:
        return "\n".join(
            "Bot: " + faq["answer"]
            for faq in matched_faqs
        )

    # Fallback for unrecognized questions.
    return (
        "I'm sorry, I didn't understand your question.\n"
        "You can ask about business hours, internship project "
        "submission, or certificates."
    )


def run_chatbot():
    """Start the interactive terminal assistant."""
    data = load_faq()

    print("=" * 55)
    print("       RULE-BASED TERMINAL CHATBOT")
    print("=" * 55)
    print("Bot: Hello! How can I help you today?")
    print("Bot: Ask about hours, project submission, or certificates.")
    print("Bot: Type bye, exit, or quit to stop.")
    print("-" * 55)

    while True:
        try:
            user_input = input("\nYou: ")

        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break

        message = normalize_text(user_input)

        if not message:
            print("Bot: Please enter a message.")
            continue

        # Remove ending punctuation for exit-command checking.
        command = re.sub(r"[.!?]+$", "", message).strip()

        if command in ("bye", "exit", "quit"):
            print("Bot: Goodbye! Have a nice day.")
            break

        response = get_response(message, data)

        if response.startswith("Bot:"):
            print(response)
        else:
            print("Bot:", response)


if __name__ == "__main__":
    run_chatbot()
