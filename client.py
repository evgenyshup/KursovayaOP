import requests
import json
from pydantic import BaseModel
from typing import Union
import re
    
    
class User(BaseModel):
    login:str
    email: str
    password: str


class AuthUser(BaseModel):
    login: str
    password: str


def send_get(url):
    headers = {'Authorization': 'xxx'}
    response = requests.get(url, headers = headers)
    return response.text, response.status_code

def validate_login(login):
    if len(login) < 8:
        print("Ошибка: Логин должен содержать не менее 8 символов")
        return False
    return True

def validate_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        print("Ошибка: Неверный формат email. Пример: user@gmail.com")
        return False
    return True

def validate_password(password):
    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>]).{10,}$'
    if not re.match(password_pattern, password):
        print("Ошибка: Пароль должен содержать мин. 10 символов, заглавные/строчные буквы, спецсимволы")
        return False
    return True

def reg():
    while True:
        login = input("Введите логин: ")
        if validate_login(login):
            break
    
    while True:
        email = input("Введите email: ")
        if validate_email(email):
            break
    
    while True:
        password = input("Введите пароль: ")
        if validate_password(password):
            break
    
    while True:
        confirm_password = input("Повторите пароль: ")
        if password == confirm_password:
            print("Пароли совпадают")
            break
        else:
            print("Ошибка: Пароли не совпадают. Попробуйте еще раз.")
    
    user_data = User(login=login, email=email, password=password)
    
    response = requests.post("http://localhost:8000/users/reg", json=user_data.model_dump())
    
    if response.status_code == 200:
        user = response.json()
        print(f"\nПользователь {user['login']} успешно зарегестрирован")
        return True
    else:
        error = response.json().get('detail', 'Ошибка')
        print(f"Произошла ошибка: {error}")
        return False


def auth():
    print("\nАВТОРИЗАЦИЯ")
    login = input("Логин: ")
    password = input("Пароль: ")
    
    user_data = AuthUser(login=login, password=password)
    
    response = requests.post("http://localhost:8000/users/auth", json=user_data.model_dump())
    
    if response.status_code == 200:
        user = response.json()
        print(f"\nАвторизация {user['login']} прошла успешно")
        return True
    else:
        error = response.json().get('detail', 'Ошибка')
        print(f"Произошла ошибка: {error}")
        return False
        
               
def sort_arr():
    print("\nСОРТИРОВКА МАССИВА")
    print("1 - Ввести массив вручную")
    print("2 - Сгенерировать случайный массив")
    print("3 - Назад")
     
    choice = input("Выберите действие: ")
    
    if choice == "1":
        array_input = input("Введите числа через пробел: ")
        try:
            array = [int(x) for x in array_input.split()]
            response = requests.post("http://localhost:8000/sort/gnom", json={"array": array})
            result = response.json()
            
            print(f"Исходный: {result['original']}")
            print(f"Отсортированный: {result['sorted']}")
            
        except ValueError:
            print("Ошибка корректности ввода")
    
    elif choice == "2":
        try:
            size = int(input("Введите размер массива: "))
            if size >= 0:
                import random
                array = [random.randint(1, 100) for _ in range(size)]
                response = requests.post("http://localhost:8000/sort/gnom", json={"array": array})
                result = response.json()
            
                print(f"\nИсходный: {result['original']}")
                print(f"Отсортированный: {result['sorted']}")
            else: 
                print("Размер массива не может быть отрицательным")
        except ValueError:
            print("Ошибка корректности ввода")
    
    elif choice == "3":
        return

    else: print("Неверно введена команда")
               
               
def main_menu():
    
    while True:
        try:
            print("\nВведите команду:")
            command = int(input("1 - Сортировка\n2 - История сортировок\n3 - Управление уч.записью\n4 - Выход из профиля\n"))
            
            match command:
                case 1:
                    sort_arr()
                case 2:
                    print("Здесь будет история сортировок")
                case 3:
                    print("Здесь будет управление уч.записью")    
                case 4:
                    break
                case _:
                    print("Неверная команда!")
                    
        except ValueError:
            print("Неверно введена команда!")
            
            
while True:
    try:
        print("\nВведите команду:")
        command = int(input("1 - Регистрация\n2 - Авторизация\n3 - Выйти из программы\n"))
        
        match command:
            case 1:
                if reg():
                    main_menu()
            case 2:
                if auth():
                    main_menu()
            case 3:
                print("Конец")
                break
            case _:
                print("Неверная команда!")
                
    except ValueError:
        print("Неверно введена команда!")
        

        
