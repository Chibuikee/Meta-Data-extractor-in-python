# import re
import unicodedata


def to_ascii(text):

    # Additional replacements for common characters
    replacements = {
        "–": "-",  # en dash
        "—": "-",  # em dash
        '"': '"',  # curly double quote left
        '"': '"',  # curly double quote right
        "'": "'",  # curly single quote
        "…": "...",  # ellipsis
        "€": "EUR",  # euro sign
        "£": "GBP",  # pound sign
        "©": "(c)",  # copyright sign
        "®": "(R)",  # registered trademark sign
        "™": "(TM)",  # trademark sign
    }

    # First, replace known characters
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)

    # Then, normalize and convert remaining characters
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(c for c in normalized if ord(c) < 128)

    return ascii_text


# Test the function
# test_strings = [
#     "Café au lait",
#     "Résumé",
#     "Niño",
#     "Größe",
#     "こんにちは",
#     "Привет",
#     "The em dash — is longer than the en dash –",
#     "Ellipsis… and © ® ™ symbols",
#     "€10 and £20",
# ]

# for string in test_strings:
#     print(f"Original: {string}")
#     print(f"ASCII:    {to_ascii(string)}")
#     print()
