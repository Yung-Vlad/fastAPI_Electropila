import uvicorn

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from mail import send_mail

app = FastAPI()

templates = Jinja2Templates(directory="html")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def get_page(request: Request) -> Jinja2Templates.TemplateResponse:
    return templates.TemplateResponse("main.html", {"request": request})


@app.post("/send")
async def thanks_page(request: Request, name: str = Form(...), phone: str = Form(...)) -> Jinja2Templates.TemplateResponse:
    valid = await send_mail(name, phone)
    if not valid:
        return templates.TemplateResponse("error.html", {"request": request})

    return templates.TemplateResponse("thank_you.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)