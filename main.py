from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_PASSWORD = os.getenv("VIP_PASSWORD")
app = FastAPI()


def get_db_cursor():
    DB_URL = os.getenv("DB_URL")
    connect = psycopg2.connect(DB_URL)
    cursor = connect.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Passwords(
        id SERIAL PRIMARY KEY,
        original_message TEXT,
        type TEXT,
        result TEXT
    )
    """)
    connect.commit()
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

    cursor.execute("INSERT INTO Passwords (original_message, type, result) VALUES (%s,%s,%s)",
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

    cursor.execute("INSERT INTO Passwords (original_message, type, result) VALUES (%s,%s,%s)",
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
def wipe_databse(x_hidden_password: str = Header(None)):
    if x_hidden_password != SECRET_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized access.")
    connect, cursor = get_db_cursor()

    cursor.execute("DELETE FROM Passwords")
    connect.commit()
    connect.close()
    return {"Message": "Wipe Completed"}
