
import requests

class ModelInterface:
    """
    Handles communication between the Python agent
    and the locally hosted Llama.cpp model.
    """

    def __init__(
        self,
        base_url="http://localhost:9931/v1",
        model="ggml-org/gemma-4-E4B-it-GGUF:Q4_0",
        timeout=120
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def generate_response(
        self,
        prompt,
        system_prompt="You are a helpful AI assistant.",
        temperature=0.3,
        max_tokens=1024
    ):
        """
        Sends a prompt to the local model and returns its response.
        """

        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout
            )

            response.raise_for_status()

            result = response.json()

            print("\n--- RAW API RESPONSE ---")
            print(result)

            message = result["choices"][0]["message"]

            content = message.get("content", "")

            if not content:
                raise RuntimeError(
                    "Model returned no final answer. "
                    "Check reasoning output and token limit."
                )

            return content

        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                "Could not connect to the local Llama server."
            )

        except requests.exceptions.Timeout:
            raise RuntimeError(
                "The model took too long to respond."
            )

        except requests.exceptions.HTTPError as error:
            raise RuntimeError(
                f"Model API returned an HTTP error: {error}"
            )

        except (KeyError, IndexError, ValueError) as error:
            raise RuntimeError(
                f"Unexpected model API response: {error}"
            )


