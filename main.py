from typing import Union, List
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import json
import time
from os import listdir
from os.path import isfile, join
import os
import random

app = FastAPI()


class User(BaseModel):
    login:str
    email: str
    password: str
    role: Union[str, None] = "basic role"
    token: Union[str, None] = None
    id: Union[int, None] = -1


class AuthUser(BaseModel):
    login: str
    password: str


class SortRequest(BaseModel):
    array: List[int]
    

@app.post("/users/reg")
def create_user(user: User):
       
    # Проверка существования пользователя
    for file in os.listdir("users"):
        with open(f"users/{file}", 'r') as f:
            data = json.load(f)
            if data['login'] == user.login:
                raise HTTPException(status_code=400, detail="Логин уже занят")
            if data['email'] == user.email:
                raise HTTPException(status_code=400, detail="Email уже занят")
            
    user.id = int(time.time())
    user.token = str(random.getrandbits(128))
    
    with open(f"users/user_{user.id}.json", 'w') as f:
        json.dump(user.model_dump(), f)
        return user
    
@app.post("/users/auth")
def auth_user(params: AuthUser):
    json_files_names = [file for file in os.listdir('users/') if file.endswith('.json')]
    for json_file_name in json_files_names:
        file_path = os.path.join('users/', json_file_name)
        with open(file_path, 'r') as f:
            json_item = json.load(f)
            user = User(**json_item)
            if user.login == params.login and user.password == params.password:
                return {"login": user.login, "token": user.token}
            
    raise HTTPException(status_code=401, detail="Неверный логин или пароль")


@app.post("/sort/gnom")
def sort_gnom(request: SortRequest):
    try:
        array = request.array.copy()
        n = len(array)
        i = 0
        while i < n - 1:
            if array[i] <= array[i + 1]:
                i += 1
            else:
                array[i], array[i + 1] = array[i + 1], array[i]
                if i > 0:
                    i -= 1
        return {"original": request.array, "sorted": array}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при сортировке")


    

