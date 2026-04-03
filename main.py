from fastapi import FastAPI
from fastapi.responses import FileResponse
import sqlite3

app = FastAPI()


def get_db_cursor():
    connect = sqlite3.connect("password_saves.db")
    cursor = connect.cursor()
    return connect, cursor


@app.get("/")
def main():
    return FileResponse("index.html")


@app.get("/encode/{text}")
def a1z26_encode(text: str):
    connect, cursor = get_db_cursor()

    encoded_message = ""
    up_message = text.upper()

    for i in up_message:
        if not i.isalpha():
            return {"Error": "Wrong Format"}
        letter_encode = ord(i) - 64
        encoded_message += str(letter_encode)
        encoded_message += "-"
    encoded_message = encoded_message[:-1]

    cursor.execute("INSERT INTO Passwords (original_message, type, result) VALUES (?,?,?)",
                   (text, "encode", encoded_message))

    connect.commit()
    connect.close()

    return encoded_message


@app.get("/decode/{numbers}")
def a1z26_decode(numbers: str):

    connect, cursor = get_db_cursor()

    decoded_message = ""
    clean_numbers = numbers.replace(" ", "-")
    number_array = clean_numbers.split("-")

    for i in number_array:
        if not i.isdigit():
            return {"Error": "Wrong Format"}
        number_decode = int(i) + 64
        decoded_number = chr(number_decode)
        decoded_message += decoded_number

    cursor.execute("INSERT INTO Passwords (original_message, type, result) VALUES (?,?,?)",
                   (numbers, "decode", decoded_message))

    connect.commit()
    connect.close()
    return decoded_message


@app.get("/history")
def get_history():
    connect, cursor = get_db_cursor()

    cursor.execute("SELECT * FROM Passwords")
    all_data = cursor.fetchall()
    connect.close()
    return {"All Data": all_data}


@app.delete("/clear")
def wipe_databse():
    connect, cursor = get_db_cursor()

    cursor.execute("DELETE FROM Passwords")
    connect.commit()
    connect.close()
    return {"Message": "Wipe Completed"}
