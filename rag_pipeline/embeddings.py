from openai import OpenAI


def embed_text(client: OpenAI, text: str, model_name: str = "text-embedding-3-small"):
    response = client.embeddings.create(
        model=model_name,
        input=text
    )

    return response.data[0].embedding