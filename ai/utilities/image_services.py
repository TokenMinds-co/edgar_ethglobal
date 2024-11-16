from openai import OpenAI


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
            lore = generate_new_lore()
        else:
            lore = generate_lore()

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


# Function to generate art using DALL-E (requires separate OpenAI API key)
def generate_lore():
    """
    Generate a lore for an NFT collection in a paragraph.

    Returns:
        str: lore for nft colelction in paragraph
    """
    try:
        print("Generating Lore...\n")

        prompt = "Generate one interesting lore for a NFT collection in a paragraph"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative NFT lore generator."},
                {"role": "user", "content": prompt},
            ],
        )

        new_lore = response["choices"][0]["message"]["content"]

        print(f"{new_lore}")
        return new_lore

    except Exception as e:
        return f"Error generating lore: {str(e)}"


def generate_new_lore():
    """
    Generate a new fresh lore for an NFT collection in a paragraph based on previous lore.

    Returns:
        str: lore for nft colelction in paragraph
    """

    try:
        global savedLore
        prompt = f"{savedLore}\n\nAbove is a lore for an NFT collection, but this lore is not really attracting people. Create a new lore for an NFT collection that may perform better than this one with a completely different style of story."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative NFT lore generator."},
                {"role": "user", "content": prompt},
            ],
        )

        new_lore = response["choices"][0]["message"]["content"]

        return new_lore

    except Exception as e:
        return f"Error generating lore: {str(e)}"
