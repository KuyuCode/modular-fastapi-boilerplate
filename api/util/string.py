def snake_to_pascal(source: str, sep: str = "_") -> str:
    return "".join(word[0].upper() + word[1:] for word in source.split(sep) if word)
