import openai


def read_api_key_from_file(file_path):
    with open(file_path, 'r') as f:
        api_key = f.read().strip()
    return api_key


def call_gpt3_5_turbo(api_key, prompt):
    openai.api_key = api_key
    model_engine = "gpt-3.5-turbo" # "gpt-4"
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()



if __name__ == '__main__':
    api_key = read_api_key_from_file("./api_key.txt")
    prompt = "Tell me a joke."
    result = call_gpt3_5_turbo(api_key, prompt)
    print(result)
