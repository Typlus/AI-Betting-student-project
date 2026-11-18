
from agent.model_interface import ModelInterface

def main():
    model = ModelInterface()

    response = model.generate_response(
        prompt="Explain what an AI agent is in three sentences.",
        system_prompt="You are a helpful AI assistant.",
        temperature=0.3,
        max_tokens=1024
    )

    print("\n--- GEMMA RESPONSE ---")
    print(repr(response))

if __name__ == "__main__":
    main()
