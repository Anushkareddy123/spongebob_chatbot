import os
import requests

# Load environment variables
env_path = os.path.expanduser("~/.soonerai.env")
with open(env_path) as f:
    for line in f:
        key, value = line.strip().split("=", 1)
        os.environ[key] = value

API_KEY = os.getenv("SOONERAI_API_KEY")
BASE_URL = os.getenv("SOONERAI_BASE_URL", "https://ai.sooners.us").rstrip("/")
MODEL = os.getenv("SOONERAI_MODEL", "gemma3:4b")

if not API_KEY:
    raise RuntimeError("Missing API key in ~/.soonerai.env")

# Initialize chat history with system message
history = [
    {"role": "system", "content": "You are SpongeBob SquarePants. Speak cheerfully and use ocean humor."}
]

print("Welcome to SpongeBob Chat! Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    # Add user message to history
    history.append({"role": "user", "content": user_input})

    # Call API
    response = requests.post(
        f"{BASE_URL}/api/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={"model": MODEL, "messages": history, "temperature": 0.6},
        timeout=60
    )

    if response.status_code == 200:
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        print("SpongeBob:", reply)
        # Add assistant reply to history
        history.append({"role": "assistant", "content": reply})
    else:
        print(f"Error {response.status_code}: {response.text}")
