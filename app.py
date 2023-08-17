from fastapi import FastAPI, Depends
import uvicorn
from models import *
from db_manager import db_connect
from decorators import is_user

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


@app.patch('/update_address')
def update_address(user:UserUpdateAddressModel):

    user_detail = db["addresses"].find({"name":user.name})

    if len(list(user_detail)) > 0:
        update_newaddress = db['addresses'].update_one({"name":user.name},{"$set":{
            "address":user.new_address
            }
            })
        return "new username updated succesfully"

    return "update address sucessfully"


@app.patch('/update_password_v2',dependencies=[Depends(is_user)])
def update_password_v2(user:UserUpdateModel_V2):

    update_user_password = db['users'].update_one({"name":user.name},{"$set":{
        "password":user.new_password,
        }
        })
    return "password updated succesfully"


@app.patch('/update_user_details',dependencies=[Depends(is_user)])
def update_user_details(user_details:DetailsUpdateModel):

    try:
        update_user_details = db['user_details'].update_one({"name":user_details.name},{"$set":{
        "name" :user_details.name,
        "gender":user_details.gender,
        "ph_number":user_details.ph_number,
        "education":user_details.education,
        "father_name":user_details.father_name
        }
        })

        return "User details updated successfully"
    except Exception as e:
        return f"{e}"

@app.delete('/delet_user_details/{name}/',dependencies=[Depends(is_user)])
def delete_user_details(name:str):

    try:
        update_user_details = db['user_details'].delete_one({"name":name})

        return "User details updated successfully"
    except Exception as e:
        return f"{e}"

if __name__ == "__main__":
    uvicorn.run("app:app",port=8000,reload=True)
