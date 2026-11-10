from groq import Groq
from config import GROQ_API_KEY


def generate_response(
    user_message,
    language="English",
    conversation_history=None
):

    if not GROQ_API_KEY:
        raise ValueError("Groq API key is missing.")

    if not user_message or not user_message.strip():
        raise ValueError("Please enter a message.")

    client = Groq(api_key=GROQ_API_KEY)

    system_prompt = f"""
    You are a helpful multilingual AI voice assistant.
    Reply in {language}.
    Use simple and clear language.
    Remember the previous conversation.
    Give conversational and easy-to-understand answers.
    """

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    # Add the last 5 conversations
    if conversation_history:

        for conversation in conversation_history[-5:]:

            messages.append({
                "role": "user",
                "content": conversation["question"]
            })

            messages.append({
                "role": "assistant",
                "content": conversation["answer"]
            })

    # Add the current question
    messages.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()