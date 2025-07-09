from pyexpat.errors import messages


def ask_llm(client, context, query, model_name="gpt-4"):
    prompt = f"""
    Answer the question as truthfully as possible using only the provided context below.
    If the answer is not contained within the context, simply say "I don't know."

    Context:
    {context}
    
    Question:
    {query}
    
    Answer:
    """

    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content