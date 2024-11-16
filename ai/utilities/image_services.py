import os
from openai import OpenAI
from dotenv import load_dotenv
import utilities.lore_services as lore_services

load_dotenv(override=True)

savedLore = None
client = OpenAI()

# Function to generate art using DALL-E (requires separate OpenAI API key)
def generate_art():
    """
    Generate art using DALL-E based on a text prompt.

    Returns:
        str: Status message about the art generation, including the image URL if successful
    """

    try:
        global savedLore
        if savedLore:
            lore = lore_services.generate_new_lore()
        else:
            lore = lore_services.generate_lore()

        prompt = f"{lore}\n\nGenerate one NFT art based on this lore "
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )


        # savedLore = lore
        image_url = response.data[0].url
        return f"Generated artwork available at: {image_url}"

    except Exception as e:
        return f"Error generating artwork: {str(e)}"