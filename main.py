from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from database import get_db_cursor, SECRET_PASSWORD
from cipher import decode_a1z26, encode_a1z26

app = FastAPI()


@app.get("/")
def main():
    return FileResponse("index.html")


@app.get("/encode/{text}")
def a1z26_encode(text: str):
    connect, cursor = get_db_cursor()
    encoded_message = encode_a1z26(text)

    if type(encoded_message) == dict:
        connect.close()
        return encoded_message

    cursor.execute("INSERT INTO Passwords (original_message, type, result) VALUES (%s,%s,%s)",
                   (text, "encode", encoded_message))

    connect.commit()
    connect.close()

    return encoded_message


@app.get("/decode/{numbers}")
def a1z26_decode(numbers: str):

    connect, cursor = get_db_cursor()
    decoded_message = decode_a1z26(numbers)

    if type(decoded_message) == dict:
        connect.close()
        return decoded_message

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
