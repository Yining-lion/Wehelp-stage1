from fastapi import FastAPI, Request, Form, Query, Body
from typing import Annotated
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import secrets
import mysql.connector
import json

con = mysql.connector.connect(
    user = "root",
    password = "1234",
    host = "localhost",
    database = "website"
)

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32)) # 設定 SessionMiddleware

templates = Jinja2Templates(directory="templates") # 設定模板

@app.get("/", response_class=HTMLResponse)
async def home(request: Request): # Jinja2Templates 需要 request 參數
    return templates.TemplateResponse( request=request,  name="index.html")

@app.post("/signup", response_class=RedirectResponse)
async def signup(
    request: Request,
    name: Annotated[str, Form()],
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    with con.cursor() as cursor: # 使用 with 開啟檔案，在最後會自動關閉
        cursor.execute("SELECT username FROM member WHERE username = %s", (username, ))
        dbUserName = cursor.fetchone() # 若查詢不到符合條件的資料，會回傳 None
        if dbUserName:
            return RedirectResponse(url="/error?message=帳號已被註冊過", status_code=303)
        cursor.execute("INSERT INTO member(name, username, password) VALUES(%s, %s, %s)", (name, username, password))
        con.commit()
        return RedirectResponse(url="/", status_code=303)

@app.post("/signin", response_class=RedirectResponse)
async def signin(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()], 
):
    with con.cursor() as cursor:
        cursor.execute("SELECT id, name, username, password FROM member WHERE username = %s", (username, ))
        dbUser = cursor.fetchone() # 若查詢不到符合條件的資料，會回傳 None
        if dbUser and password == dbUser[3]:
            request.session["SIGNED-IN"] = True
            request.session["ID"] = dbUser[0]
            request.session["NAME"] = dbUser[1]
            request.session["USERNAME"] = dbUser[2]
            return RedirectResponse(url="/member", status_code=303)
        return RedirectResponse(url="/error?message=帳號或密碼輸入錯誤", status_code=303)

@app.get("/signout", response_class=RedirectResponse)
async def signout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    if request.session.get("SIGNED-IN") == True:
        name = request.session.get("NAME")
        member_id = request.session.get("ID")
        with con.cursor() as cursor:
            cursor.execute("""
                        SELECT name, content, member_id, message.id FROM message 
                        INNER JOIN member ON member.id=message.member_id 
                        ORDER BY message.time DESC
                        """)
            dbMessages = cursor.fetchall()
            messages = [{"dbName": dbName, "dbContent": dbContent, "is_me": (db_member_id == member_id), "msg_id": msg_id} 
                        for dbName, dbContent, db_member_id, msg_id in dbMessages] 
            # [{'dbName': 'a', 'dbContent': '哈囉', 'is_me': True}, {'dbName': 'd', 'dbContent': '你好 d', 'is_me': False}, ...]
            return templates.TemplateResponse(request=request, name="member.html", context={"name": name, "messages": messages})
    return RedirectResponse(url="/", status_code=303)

@app.get("/api/member")
async def showName(
    request: Request,
    username: Annotated[str, Query()]
):
    if request.session.get("SIGNED-IN") != True:
        return JSONResponse(content={"data": None}, status_code=401) # 401 未授權 (Unauthorized)
    
    with con.cursor() as cursor:
        cursor.execute("SELECT id, name, username FROM member WHERE username= %s", (username, ))
        data = cursor.fetchone()
        if data:
            return {
                        "data":{
                        "id": data[0],
                        "name": data[1],
                        "username": data[2]
                        }
                    }
        else :
            return {"data": None}
        
@app.patch("/api/member")
async def updateName(
    request: Request,
):
    data = await request.json()
    name = data.get("name")
    id = request.session.get("ID")

    if request.session.get("SIGNED-IN") == True:
        with con.cursor() as cursor:
            cursor.execute("UPDATE member SET name = %s WHERE id= %s", (name, id))
            con.commit()
            request.session["NAME"] = name
            return {"ok": True}
    return {"error": True}

@app.post("/createMessage", response_class=RedirectResponse)
async def createMessage(
    request: Request,
    content: Annotated[str, Form()]
):
    member_id = request.session.get("ID")
    with con.cursor() as cursor:
        cursor.execute("INSERT INTO message(member_id, content) VALUES(%s, %s)", (member_id, content))
        con.commit()
        return RedirectResponse(url="/member", status_code=303)

@app.post("/deleteMessage", response_class=RedirectResponse)
async def deleteMessage(
    request: Request,
    msg_id: Annotated[int, Form()]
):
    member_id = request.session.get("ID")
    with con.cursor() as cursor:
        cursor.execute("SELECT member_id FROM message WHERE id = %s", (msg_id, ))
        db_member_id = cursor.fetchone()

        if db_member_id[0] == member_id:
            cursor.execute("DELETE FROM message WHERE id = %s", (msg_id, ))
            con.commit()
            return RedirectResponse(url="/member", status_code=303)

@app.get("/error", response_class=HTMLResponse)
async def error(
    request: Request, 
    message: Annotated[str, Query()]
):
    return templates.TemplateResponse(request=request, name="error.html", context={"message": message})

app.mount("/static", StaticFiles(directory="static"), name="static")