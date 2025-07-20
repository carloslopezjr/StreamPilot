from openai import OpenAI
import requests
import re

client = OpenAI(api_key="")


def gen_desc(prompt):

    responses_text = []

    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "user", "content": f"Create me a title following this description: {prompt}"},
            {"role": "user", "content": "Give me a description based on the title given by the previous prompt"},
            {"role": "user", "content": "Based on the description and on the title give me a prompt that i can give dall-3-e for a thubnail image"},
            {"role": "user", "content": "Make sure all of the responses start with the following format Title: and dont add quotations at the start and end of the response"}
        ],
        max_tokens=1000
    )

    api_response = response.choices[0].message.content

    print(api_response)

    matches = re.findall(r":\s*(.*)", api_response)

    for match in matches:
        responses_text.append(match)


    # call gen_image to generate the image based on the description
    #gen_image(responses_text[2])
    return responses_text

def gen_image(desc):

    # Generate an image using DALL·E 3
    response = client.images.generate(
        model="dall-e-3",
        prompt=desc,
        size="1024x1024",           # or "1792x1024" or "1024x1792"
        quality="standard",         # or "hd" if you have access
        n=1                         # number of images
    )

    # Get the temporary image URL
    image_url = response.data[0].url
    print("🖼️ Generated image URL:", image_url)

    # Download the image
    img_response = requests.get(image_url)

    if img_response.status_code == 200:
        with open("generated_image.png", "wb") as f:
            f.write(img_response.content)
        print("Image saved as generated_image.png")
    else:
        print("Failed to download image. Status code:", img_response.status_code)

print(gen_desc("I'm doing a livestream where im going to solve three leetcode binary search problems"))
