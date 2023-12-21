import base64

string = "qwerty"  # enter your mySQL password here
 
def maskPsw():
    encode = base64.b64encode(string.encode("utf-8"))

    # Decoding the string
    decode = base64.b64decode(encode).decode("utf-8")
    
    return decode