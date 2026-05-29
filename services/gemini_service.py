from google import genai


client = genai.Client(
    api_key="YOUR_GEMINI_API_KEY"
)


def ask_ai(prompt):
    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text
