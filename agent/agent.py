from agent.model_interface import ModelInterface

class Agent:
    def __init__(self):
        self.model = ModelInterface()

        self.system_prompt = """
            You are an AI research assistant.

        Your responsibilities include:
        - Understanding user requests.
        - Providing clear, structured responses.
        - Analyzing sports statistics and historical performance.
        - Explaining the reasoning behind statistical conclusions.

        Never invent statistics or claim to have accessed data
        that was not provided.
        """

    def process_request(self, user_input):
        """
        Process a user request and returns the model response    
        """
        if not user_input or not user_input.strip():
            raise ValueError("User input is empty")
        response = self.model.generate_response(
            prompt=user_input,
            system_prompt=self.system_prompt,
            temperature=0.3,
            max_tokens=1024
        )
        return response


    