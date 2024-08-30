import requests
from openai import OpenAI


def orouter_stream_chat(system_message, user_prompt, model, max_tokens=4000, temperature=1):
    client = OpenAI(
        api_key="",
        base_url="https://openrouter.ai/api/v1")

    stream = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


def orouter_stream_messages(messages, model, max_tokens=4000, temperature=1):
    client = OpenAI(
        api_key="",
        base_url="https://openrouter.ai/api/v1")

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


def oroute_chat(system_message, prompt, model="microsoft/wizardlm-2-8x22b", max_tokens=4000, temperature=1):
    api_key = ""
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        # Raises an HTTPError if the response status code is 4XX or 5XX
        response.raise_for_status()
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def oroute_messages(messages, model="microsoft/wizardlm-2-8x22b", temperature=1, max_tokens=4000):
    api_key = ""
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    return response_json['choices'][0]['message']['content']
