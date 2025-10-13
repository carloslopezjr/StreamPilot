import ollama
import re

def gen_desc(prompt):
    
    responses_text = []
    response = ollama.chat(model="gpt-oss:20b", messages=[
        {"role": "user", "content": f"Create me a title following this description for a youtube stream: {prompt}"},
        {"role": "user", "content": "Give me a description for the stream based on the title given by the previous prompt"},
        {"role": "user", "content": "Based on the description and on the title give me a prompt that i can give dall-3-e for a thubnail. Please make it to YouTube thubnail standards."},
        {"role": "user", "content": "Make sure all of the responses start with the following format Title: and dont add quotations at the start and end of the response"}
    ])


    matches = re.findall(r":\s*(.*)", response['message']['content'])

    for match in matches:
        responses_text.append(match.strip())

    return { "title" : responses_text[0], "description" : responses_text[1] }