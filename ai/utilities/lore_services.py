from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

savedLore = None
client = OpenAI()

# Function to generate art using DALL-E (requires separate OpenAI API key)
def generate_lore():
    """
    Generate a lore for an NFT collection in a paragraph.

    Returns:
        str: lore for nft colelction in paragraph
    """
    try:

        prompt = "Generate one interesting lore about Ethereum ecosystem and Devcon for a NFT collection in a paragraph"
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a creative NFT lore generator."},
                {"role": "user", "content": prompt},
            ],
        )

        res = response.choices[0].message.content
        return res

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
        prompt = f"{savedLore}\n\nAbove is a lore for an NFT collection, but this lore is not really attracting people. Create a new lore about Ethereum ecosystem and Devcon that may perform better than this one with a completely different style of story."
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a creative NFT lore generator."},
                {"role": "user", "content": prompt},
            ],
        )

        res = response.choices[0].message.content

        return res

    except Exception as e:
        return f"Error generating lore: {str(e)}"

