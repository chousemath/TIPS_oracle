import unicodedata

def normalize(input: str) -> str:
    return unicodedata.normalize('NFC', input)

