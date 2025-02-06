from fastapi import FastAPI, Request, Form, Path, Query
from typing import Annotated
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
users = {"test":"test"} # 內建帳號密碼

app.add_middleware(SessionMiddleware, secret_key="qiAZnWciKWeZYoB") # 設定 SessionMiddleware

templates = Jinja2Templates(directory="templates") # 設定模板

@app.get("/", response_class=HTMLResponse)
async def home(request: Request): # Jinja2Templates 需要 request 參數
    return templates.TemplateResponse( request=request,  name="index.html")

@app.post("/signin", response_class=RedirectResponse)
async def signin(
    request: Request,
    username: Annotated[str, Form()], # 使用 Form() 時，username 和 password 預設是必要參數
    password: Annotated[str, Form()], 
    agree: Annotated[bool, Form()],
):
    if agree:
        # status_code=303：強制瀏覽器用 GET 方法重新請求新 URL，如果不指定 status_code=303，FastAPI 預設會使用 307，但 307 會讓瀏覽器用原本的 POST 方法重新請求
        if not username or not password:
            return RedirectResponse(url="/error?message=請輸入帳號及密碼", status_code=303) 
        elif username not in users or users[username] != password:
            return RedirectResponse(url="/error?message=帳號或密碼輸入錯誤", status_code=303)
        request.session["SIGNED-IN"] = True
        return RedirectResponse(url="/member", status_code=303)

@app.get("/signout", response_class=RedirectResponse)
async def signout(request: Request):
    request.session["SIGNED-IN"] = False
    return RedirectResponse(url="/", status_code=303)

@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    if request.session.get("SIGNED-IN") == True:
        return templates.TemplateResponse(request=request, name="member.html")
    return RedirectResponse(url="/", status_code=303)

@app.get("/error", response_class=HTMLResponse)
async def error(request: Request, message: Annotated[str, Query()]):
    return templates.TemplateResponse(request=request, name="error.html", context={"message": message})

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/square/{num}", response_class=HTMLResponse)
async def square(request: Request, num: Annotated[int, Path()]):
    square = num*num
    return templates.TemplateResponse(request=request, name="square.html", context={"square": square})