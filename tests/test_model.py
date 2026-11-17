
from agent.model_interface import ModelInterface


model = ModelInterface()

response = model.generate_response(
    prompt="Explain what an AI agent is in three sentences."
)

print("\nModel response:")
print(response)

