from db_manager import db_connect
from fastapi import HTTPException

db = db_connect()

def is_user(username,password):

    user_detail = db["users"].find({"name":username,"password":password})

    if len(list(user_detail)) > 0:
        return True
    else:
        raise HTTPException(403)