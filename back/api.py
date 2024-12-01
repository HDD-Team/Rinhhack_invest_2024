from fastapi import FastAPI, HTTPException, Depends, Security, File, UploadFile, Form, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from passlib.context import CryptContext
from datetime import datetime, timedelta
from itertools import zip_longest
from typing import Optional, List, Dict
from colorama import Fore, Style
from pydantic import BaseModel
from dotenv import load_dotenv
import subprocess
import asyncpg
import uvicorn
import shutil
import bcrypt
import logging
import random
import json
# import pytz
import os
import re

import smtplib
from email.mime.text import MIMEText    
from email.mime.multipart import MIMEMultipart
import yagmail


# Настройка логирования
class CustomFormatter(logging.Formatter):
    # Цвета для разных уровней логов
    LEVEL_COLORS = {
        logging.DEBUG: Fore.GREEN,
        logging.INFO: Fore.CYAN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):
        # Добавляем цвет в зависимости от уровня
        level_color = self.LEVEL_COLORS.get(record.levelno, Fore.WHITE)
        record.levelname = f"{level_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)

# Создаем кастомный обработчик
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter(fmt="%(levelname)s: %(message)s"))

# Применяем настройки
logging.basicConfig(level=logging.INFO, handlers=[handler])


def run_uvicorn():
    command = [
        "uvicorn", 
        "api:app", 
        "--log-config", "log_config.yaml", 
        "--host", "0.0.0.0", 
        "--port", "8001", 
        "--reload"
    ]
    subprocess.run(command)

# uvicorn api.main:app --log-config log_config.yaml --host 0.0.0.0 --port 8001 --reload



# Получаем параметры базы данных
load_dotenv('env.env')

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")


# Подключение к базе данных
DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?options=-c timezone=Etc/GMT-3"

# Глобальный пул подключений
pool = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    print("STARTUP FASTAPI")
    yield
    await pool.close()
    print("SHUTDOWN FASTAPI")

app = FastAPI(lifespan=lifespan)


# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Разрешаемые методы (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Разрешить все заголовки
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    logging.info(f"Incoming request: {request.method} {request.url}")
    logging.info(f"Request body: {body.decode('utf-8')}")
    response = await call_next(request)
    return response

# Настройки для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для хеширования пароля
async def get_password_hash(passwd):
    return bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Функция для проверки пароля
async def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))





class Register(BaseModel):
    first_name: str
    last_name: str
    second_name: str
    login: str
    password: str
    role: str

# Эндпоинт для регистрации
@app.post("/register")
async def register(user: Register):
    print(user)
    # Проверка валидности роли
    if user.role not in ['child', 'teacher', 'parent']:
       
        return JSONResponse(status_code=400, content={"success": False, "message": "Invalid role"})

    async with pool.acquire() as conn:
        try:
            check_email = await conn.fetchval("""
            SELECT EXISTS (
                SELECT 1
                FROM users
                WHERE login = $1
            )
            """, user.login)
            if not check_email:
                # Хеширование пароля
                hashed_password = await get_password_hash(user.password)
                

                # # Генерация UUID и преобразование в строку
                # unique_id = str(uuid.uuid4())

                # # Обрезаем строку до первых 6 цифр
                # six_digit_number = int(unique_id.replace("-", "")[:6])
                six_digit_number = random.randint(100000, 999999)
                print(six_digit_number)
                # Вставка пользователя
                user_id = await conn.fetchval("""
                    INSERT INTO users (login, pass, verif_code, verif, role)
                    VALUES ($1, $2, $3, $4, $5) RETURNING id
                """, user.login, hashed_password, six_digit_number, False, user.role)
                if user.role == "child":
                    await conn.execute("""
                        INSERT INTO childs (id, first_name, last_name, second_name)
                        VALUES ($1, $2, $3, $4)
                    """, user_id, user.first_name, user.last_name, user.second_name)
                elif user.role == "teacher":
                    await conn.execute("""
                        INSERT INTO teachers (id, first_name, last_name, second_name, clases_id_owner)
                        VALUES ($1, $2, $3, $4, $5)
                    """, user_id, user.first_name, user.last_name, user.second_name, [])
                sender_email = "andr.bur-bur.4@mail.ru" 
                receiver_email = user.login
                password_mail = "hgKNHd9FmSHjA7XbTXEj"
                
                # yag = yagmail.SMTP(sender_email, password_mail)
                # yag.send(receiver_email, "Код для верификации", "Ваш код верификации почты:\n{six_digit_number}")
                # print("Email sent successfully!")

                msg = MIMEMultipart() 
                msg["From"] = sender_email
                msg["To"] = receiver_email
                msg["Subject"] = "Код подтвержения почты"

                body = f"Ваш код подтверждения:\n\n--> {six_digit_number} <--"
                msg.attach(MIMEText(body, "plain"))

                try:
                    server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
                    server.login(sender_email, password_mail)
                    server.sendmail(sender_email, receiver_email, msg.as_string())
                    print("Email sent successfully!")
                except Exception as e:
                    logging.error(e)
                    return JSONResponse(status_code=500, content={"success": False, "message": str(e)})
                finally:
                    server.quit()
                #TODO Добавить обработку
                # # Вставка данных кандидата или работодателя
                # if user.role == 'candidate':
                #     await conn.execute("""
                #         INSERT INTO candidates (candidate_id, first_name, last_name, phone)
                #         VALUES ($1, $2, $3, $4)
                #     """, user_id, user.first_name, user.last_name, user.phone)
                # elif user.role == 'employer':
                #     await conn.execute("""
                #         INSERT INTO employers (employer_id, first_name, last_name, phone)
                #         VALUES ($1, $2, $3, $4)
                #     """, user_id, user.first_name, user.last_name, user.phone)

                return {"success": True, "message": "send verification code on email", "user_id": user_id}
            else:
                return JSONResponse(status_code=500, content={"success": False, "message": "Email already exists."})
        except Exception as e:
            logging.error(e)
            return JSONResponse(status_code=500, content={"success": False, "message": str(e)})
        



class VerifCode(BaseModel):
    id: int
    code: int

@app.post('/register/verifi_code')
async def verificate_code(verif: VerifCode):
     async with pool.acquire() as conn:
        try:
            true_verif_code = await conn.fetchval("""
                    SELECT verif_code FROM users WHERE id = $1
                """, verif.id)
            if true_verif_code == verif.code:
                await conn.fetchrow("""
                UPDATE users SET verif = $1 WHERE id = $2
                """,True, verif.id)
                return JSONResponse(
                    status_code=200,
                    content={"success": True, "message": f"ID: {verif.id} is Baned"}
                )
        except Exception as e:
            logging.error(e)
            return JSONResponse(status_code=500, content={"success": False, "message": str(e)})
        
# Кастомная форма для авторизации
class CustomOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    def __init__(self, login: str, password: str):
        super().__init__(username=login, password=password)


# Эндпоинт для авторизации
@app.post("/token")
async def login(form_data: CustomOAuth2PasswordRequestForm = Depends()):
    print(form_data)
    async with pool.acquire() as conn:
        try:
            # Получение пользователя из базы данных
            user_data = await conn.fetchrow("""
                SELECT id, pass, role FROM users WHERE login = $1
            """, form_data.username)

            if not user_data:
                return JSONResponse(status_code=400, content={"success": False, "message": "Incorrect login or password"})

            check_pass = await verify_password(form_data.password, user_data['pass'])
            # Проверка пароля
            if not check_pass:
                return JSONResponse(status_code=400, content={"success": False, "message": "Incorrect login or password"})

            return JSONResponse(status_code=200, content={"success": True, "role": user_data["role"], "id": user_data['id']})
        
        except Exception as e:
            logging.error(e)
            return JSONResponse(status_code=500, content={"success": False, "message": str(e)})
        
@app.post("/child")
async def display_child(id: int):
    async with pool.acquire() as conn:
        try:
            check_user = await conn.fetchval("""
            SELECT EXISTS (
                SELECT 1
                FROM users
                WHERE id = $1
            )
            """, id)
            if check_user:
                # Получение пользователя из базы данных
                user_data = await conn.fetchrow("""
                SELECT 
                    childs.id, 
                    childs.first_name AS child_first_name, 
                    childs.last_name AS child_last_name, 
                    clases.class_number,    
                    teachers.first_name AS teacher_first_name, 
                    teachers.last_name AS teacher_last_name, 
                    courses.course_name, 
                    courses.course_description, 
                    parents.first_name AS parent_first_name, 
                    parents.last_name AS parent_last_name
                FROM 
                    childs 
                LEFT JOIN 
                    clases ON childs.class_id = clases.id
                LEFT JOIN 
                    teachers ON clases.id = ANY(teachers.clases_id_owner)
                LEFT JOIN 
                    courses ON clases.courses_id = courses.id
                LEFT JOIN 
                    parents ON childs.id = ANY(parents.childs_id_owner)
                WHERE 
                    childs.id = $1;  -- выбираем ребёнка по id
                """, id)


                # return JSONResponse(status_code=200, content={"success": True, "message": user_data})
                return {"success": True, "message": user_data}

        except Exception as e:
            logging.error(e)
            return JSONResponse(status_code=500, content={"success": False, "message": str(e)})

class ChildEdit(BaseModel):
    id: int
    child_first_name: str
    child_last_name: str

@app.put('/child/edit')
async def child_ebit(data: ChildEdit):
    async with pool.acquire() as conn:
        try:
            check_user = await conn.fetchval("""
            SELECT EXISTS (
                SELECT 1
                FROM users
                WHERE id = $1
            )
            """, data.id)
            if check_user:
                await conn.fetchrow("""
                UPDATE childs SET first_name = $1, last_name = $2 WHERE id = $3
                """,data.child_first_name, data.child_last_name, data.id)
                return JSONResponse(
                    status_code=200,
                    content={"success": True, "message": f"ID: {data.id} is edit successfuly"}
                )
            
            else:
                return JSONResponse(
                status_code=404,
                content={"success": False, "message": f"User with ID: {data.id} not found"}
            )
        except Exception as e:
            logging.error(e)
            return JSONResponse(status_code=500, content={"success": False, "message": str(e)})


@app.post("/teacher")
async def display_teacher(teacher_id: int):
    async with pool.acquire() as conn:
        try:
            check_user = await conn.fetchval("""
            SELECT EXISTS (
                SELECT 1
                FROM users
                WHERE id = $1
            )
            """, teacher_id)
            if check_user:
                # Получение пользователя из базы данных
                user_data = await conn.fetchrow("""
                    SELECT 
                        teachers.first_name,
                        teachers.last_name,
                        teachers.second_name,
                        teachers.clases_id_owner AS class_list,
                        users.login AS email
                    FROM
                        teachers
                    JOIN users ON teachers.id = users.id
                    WHERE 
                        teachers.id = $1
                """, teacher_id)
                child_list_to_class = []

                for class_id in user_data['class_list']:
                    class_data = await conn.fetchrow("""
                        SELECT 
                            clases.class_number,
                            clases.childs_list_id AS child_list
                        FROM
                            clases
                        WHERE 
                            id = $1
                    """, class_id)
                    child_list = []
                    for child_id in class_data['child_list']:
                        child_fio = await conn.fetchrow("""
                        SELECT 
                            childs.first_name,
                            childs.last_name,
                            childs.second_name
                        FROM
                            childs
                        WHERE 
                            id = $1
                    """, child_id)
                        child_list.append((child_id, f'{child_fio['first_name']} {child_fio['last_name']} {child_fio['second_name']}'))
                    print(class_data)
                    child_list_to_class.append((class_data['class_number'], child_list, class_id))
                print(child_list_to_class)

                result_data = {
                    "success": True,
                    "message": {
                        "first_name": user_data['first_name'],
                        "last_name": user_data['last_name'],
                        "second_name": user_data['second_name'],
                        "email": user_data['email'],
                        "clases_owner": child_list_to_class
                    }
                }
                
                return JSONResponse(status_code=200, content=result_data)
                # return {"success": True, "message": user_data}

        except Exception as e:
            logging.error(e)
            return JSONResponse(status_code=500, content={"success": False, "message": str(e)})


@app.put("/teacher/edit_class")
async def display_teacher(class_id: int, login: str):
    async with pool.acquire() as conn:
        try:
            child_list = await conn.fetchval(""" 
                SELECT 
                    childs_list_id 
                FROM 
                    clases 
                WHERE 
                    id = $1
            """, class_id)

            # Если child_list == None, инициализируем его как пустой список
            if child_list is None:
                child_list = []

            child_id = await conn.fetchval(""" 
                SELECT 
                    id 
                FROM 
                    users 
                WHERE 
                    login = $1 AND role = 'child'
            """, login)

            if child_id:
                child_list.append(child_id)

                await conn.fetchrow(""" 
                    UPDATE clases 
                    SET childs_list_id = $1 
                    WHERE id = $2
                """, child_list, class_id)
                
                teacher_id = await conn.fetchval("""
                        SELECT 
                            teachers.id
                        FROM
                            teachers
                        JOIN clases ON clases.id = ANY(teachers.clases_id_owner)
                        WHERE 
                            clases.id = $1
                    """, class_id)

                await conn.fetchrow(""" 
                    UPDATE childs
                    SET class_id = $1, teacher_id = $2 
                    WHERE id = $3
                """, class_id, teacher_id, child_id)

                return JSONResponse(status_code=200, content={"success": True, "message": "Adding successfully"})

            else:
                return JSONResponse(status_code=404, content={"success": False, "message": "User not found"})

        except Exception as e:
            logging.error(e)
            return JSONResponse(status_code=500, content={"success": False, "message": str(e)})

        

@app.put("/teacher/add_class")
async def add_class(class_number: str, teacher_id: int):
    async with pool.acquire() as conn:
        try:
            # Вставка нового класса и получение его ID
            class_id = await conn.fetchval("""
                INSERT INTO clases (class_number, childs_list_id)
                VALUES ($1, $2) RETURNING id
            """, class_number, [])

            # Получаем текущий список классов для преподавателя
            clases_id_owner_list = await conn.fetchval("""
                SELECT clases_id_owner FROM teachers WHERE id = $1
            """, teacher_id)

            # Если список пуст, создаем новый
            if clases_id_owner_list is None:
                clases_id_owner_list = []

            # Добавляем новый class_id в список
            clases_id_owner_list.append(class_id)

            # Обновляем список классов у преподавателя
            await conn.fetchrow("""
                UPDATE teachers
                SET clases_id_owner = $1
                WHERE id = $2
            """, clases_id_owner_list, teacher_id)

            return JSONResponse(status_code=200, content={"success": True, "message": "Adding successfully", "class_id": class_id})
        
        except Exception as e:
            logging.error(e)
            return JSONResponse(status_code=500, content={"success": False, "message": str(e)})
       


@app.post("/verify_code")
async def dialog(code: str = Form(...)):
    try:
        #TODO:дописать на серваке
        ...
    except Exception as e:
            logging.error(e)
            return JSONResponse(status_code=500, content={"success": False, "message": str(e)})


app.post("/help")
async def dialog(help_ask: str, task: str, question: str):
    try:
        #TODO:дописать на серваке
        ...
    except Exception as e:
            logging.error(e)
            return JSONResponse(status_code=500, content={"success": False, "message": str(e)})



if __name__ == "__main__":
    run_uvicorn()