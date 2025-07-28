from openai import OpenAI

client = OpenAI()

def summarize_text(text: str):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Summarize this medical information."},
            {"role": "user", "content": text}
        ]
    )
    return completion.choices[0].message.content
