import re
import smtplib
from email.mime.text import MIMEText
from pydantic import BaseModel, ValidationError, field_validator, constr


class FormData(BaseModel):
    name: str
    phone: constr(pattern=r"^(\+)?(38)?0\d{9}$")

    @field_validator("phone")
    def validate_phone(cls, tel: str) -> str:
        if not tel:
            raise ValueError("Invalid phone number!")

        return tel


async def send_mail(name: str, phone: str) -> bool:
    try:
        FormData(name=name, phone=phone)
    except ValidationError as _ex:
        print(f"Invalid phone number: {_ex}")
        return False

    sender = "clothess951@gmail.com"
    password = "jpxj wxrc zdjg ixwb"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(f"{name}\n{phone}")
        msg["Subject"] = "ELECTROPILA"
        server.sendmail(sender, sender, msg.as_string())
        print("Successfully send msg!")

    except Exception as _ex:
        print(f"Some error...\n {_ex}")

    finally:
        server.quit()

    return True
