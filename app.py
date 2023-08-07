from fastapi import FastAPI, Body
import uvicorn
from models import User, UserUpdateModel, UsernameUpdateModel
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


@app.post('/signup')
def create_user(user:User):

    add_user = db['users'].insert_one(dict(user))

    return "signup successful"


@app.patch('/update_password')
def update_password(user:UserUpdateModel):

    user_detail = db["users"].find({"name":user.name,"password":user.old_password})


    if len(list(user_detail)) > 0:
        update_user_password = db['users'].update_one({"name":user.name},{"$set":{"password":user.new_password}})
        return "password updated succesfully"

    return "User not found or password is incorrect"

@app.patch('/update_username')
def update_username(user:UsernameUpdateModel):

    user_detail = db["users"].find({"name":user.old_username,"password":user.password})

    if len(list(user_detail)) > 0:
        update_newusername = db['users'].update_one({"name":user.old_username},{"$set":{"name":user.new_username}})
        return "new username updated succesfully"

    return "User not found or password is incorrect"







if __name__ == "__main__":
    uvicorn.run("app:app",port=8000,reload=True)
