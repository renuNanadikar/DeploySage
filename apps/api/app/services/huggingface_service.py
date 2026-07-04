import os

from huggingface_hub import InferenceClient


MODEL_ID = "openai/gpt-oss-120b"
PROVIDER = "cerebras"


def generate_text(prompt: str, max_tokens: int = 350, temperature: float = 0.2) -> str:
    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        raise RuntimeError("HF_TOKEN environment variable is missing.")

    client = InferenceClient(
        provider=PROVIDER,
        api_key=hf_token,
    )

    completion = client.chat_completion(
        model=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return completion.choices[0].message.content.strip()