from llm import generate_response

try:
    print("Testing Groq LLM...")

    answer = generate_response(
        "What is Artificial Intelligence?",
        "English"
    )

    print("\nAI Response:")
    print(answer)

    print("\nSUCCESS! Groq LLM is working.")

except Exception as error:
    print("ERROR:", error)