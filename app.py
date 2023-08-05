from fastapi import FastAPI
import uvicorn
from db_manager import db_connect

app = FastAPI()
db = db_connect()


@app.get("/login/{username}/{password}")
def login(username,password):
    
    user_detail = db["users"].find({"name":username,"password":password})


    if len(list(user_detail)) > 0:

        return "Login succesfull"

    return "Authentication failed"


@app.get("/login_v2/{username}/{password}")
def login_v2(username,password):
    
    user_detail = db["users"].find({"name":username})

    user_details = list(user_detail)

    if len(user_details) > 0:

        if user_details[0]['password'] == password:
            return "Login succesfull"

        return "Incorrect password"
    
    return "user not found"





if __name__ == "__main__":
    uvicorn.run("app:app",port=8000,reload=True)
