import base64

def base64_to_file(encoded_file: str) -> bytes:
    base64_str = encoded_file.split(",")[1]
    decoded = base64.b64decode(base64_str)

    return decoded