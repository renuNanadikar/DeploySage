import os

from huggingface_hub import InferenceClient


MODEL_ID = "openai/gpt-oss-120b"
PROVIDER = "cerebras"


def build_pr_prompt(pr_title: str, diff: str) -> str:
    return f"""
You are DeploySage, an AI DevOps assistant.

Generate a clear pull request title and description from the following PR information.

Use only the provided PR title and diff.
Do not invent tests, files, or deployment details.
Keep the description concise and useful for a GitHub pull request.

Return the response in this exact format:

Title: <generated title>

Description:
<generated description>

PR Title:
{pr_title}

Code Diff:
{diff}
"""


def generate_pr_documentation(pr_title: str, diff: str) -> dict:
    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        raise RuntimeError("HF_TOKEN environment variable is missing.")

    client = InferenceClient(
        provider=PROVIDER,
        api_key=hf_token,
    )

    prompt = build_pr_prompt(pr_title=pr_title, diff=diff)

    completion = client.chat_completion(
        model=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=350,
        temperature=0.2,
    )

    generated_text = completion.choices[0].message.content.strip()

    return {
        "generated_title": f"AI Summary: {pr_title}",
        "generated_description": generated_text,
        "provider": "huggingface",
    }