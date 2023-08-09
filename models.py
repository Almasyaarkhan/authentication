from pydantic import BaseModel

class User(BaseModel):
    name: str
    password: str

class UserUpdateModel(BaseModel):
    name: str
    old_password: str
    new_password: str


class UsernameUpdateModel(BaseModel):
    old_username:str
    new_username:str
    password:str


class UserUpdateAddressModel(BaseModel):
    name: str
    new_address:str

class UserUpdateModel_V2(BaseModel):
    name: str
    new_password: str