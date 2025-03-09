import ollama

# Assuming ollama.list() is not needed for this example
# response = ollama.list()

res = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "user", "content": "why is the sky blue?"}
    ],
    stream=False  # Assuming you want to turn off streaming
)

# Assuming the response structure contains a 'message' key with a list of messages
print(res["Message"][0]["content"])