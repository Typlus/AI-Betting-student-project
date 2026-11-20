from agent.agent import Agent


def main():
    agent = Agent()

    response = agent.process_request(
        "Explain how historical sports statistics "
        "can help evaluate team performance."
    )

    print("\n--- AGENT RESPONSE ---")
    print(response)


if __name__ == "__main__":
    main()
