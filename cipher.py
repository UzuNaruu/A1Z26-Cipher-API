def encode_a1z26(text: str):
    encoded_message = ""
    up_message = text.upper()

    for i in up_message:
        if not i.isalpha():
            return {"Error": "Wrong Format"}
        letter_encode = ord(i) - 64
        encoded_message += str(letter_encode)
        encoded_message += "-"
    encoded_message = encoded_message[:-1]

    return encoded_message


def decode_a1z26(numbers: str):
    decoded_message = ""
    clean_numbers = numbers.replace(" ", "-")
    number_array = clean_numbers.split("-")

    for i in number_array:
        if not i.isdigit():
            return {"Error": "Wrong Format"}
        number_decode = int(i) + 64
        decoded_number = chr(number_decode)
        decoded_message += decoded_number

    return decoded_message
