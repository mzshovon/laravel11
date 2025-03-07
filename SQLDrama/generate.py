import ollama

def generate(prompt):
    try:
        model = "mistral"
        # print(f"Building connectivity ollama with agent {model}")

        response = ollama.generate(
            model=model,
            prompt=f"Convert the following prompt into MYSQL query: {prompt}"
        )

        # parsed_response = response.text

        # print(f"Generating response from agent {model}...........")
        return response['response']

    except Exception as e:
        raise Exception(f"🐞 Something went wrong: Report:{e}")
