import os
from openai import OpenAI
import argparse
import re

MAX_INPUT_LENGTH = 30

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, help="Input text", required=True)
    args = parser.parse_args()
    user_input = args.input

    print(f"Input: {user_input}")

    if validate_length_prompt(prompt=user_input):
        generate_branding_snipper(prompt=user_input)
        generate_keywords(prompt=user_input)
    else:
        raise ValueError(
            f"Input text is too long. Please limit to {MAX_INPUT_LENGTH} characters.\n"
            f"Submitted input is: {user_input}"
            )

def validate_length_prompt(prompt):
    return(len(prompt) <= 30)

def generate_keywords(prompt: str):

    OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")

    client = OpenAI(api_key=OPENAI_API_KEY)

    enriched_prompt = (
        f"Generate related branding keywords for {prompt}," 
        "return them as a comma separated list, and do not include"
        "any text or acknolwedgement other than the list.")

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "You are an expert marketing director"},
        {"role": "user", "content": (
            f"{enriched_prompt}"
        )},
    ]
    )

    keywords_text = response.choices[0].message.content

    #Strip keywords
    keywords_array = re.split(",|\n|;|-", keywords_text)
    keywords_array = [k.lower().strip() for k in keywords_array]
    keywords_array = [k for k in keywords_array if len(k) > 0]

    print(f"Keywords: {keywords_array}")

    return(keywords_array)

def generate_branding_snipper(prompt: str):

    OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")

    client = OpenAI(api_key=OPENAI_API_KEY)

    enriched_prompt = f"Generate upbeat branding snippet for {prompt}."

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "You are an expert marketing director"},
        {"role": "user", "content": (
            f"{enriched_prompt}"
        )},
    ]
    )

    branding_text = response.choices[0].message.content

    print(f"Branding Snippet: {branding_text}")
    return(branding_text)

if __name__ == "__main__":
    main()