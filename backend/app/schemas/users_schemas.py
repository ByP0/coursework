from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Optional
from email_validator import validate_email

from app.services.users_services import validate_phone


class SingUpUser(BaseModel):

    first_name: Annotated[str, Field(title="Имя", examples=["Александр"])]
    second_name: Annotated[str, Field(title="Фамилия", examples=["Иванов"])]
    password: Annotated[str, Field(title="Пароль", examples=["password"])]
    phone: Annotated[str, Field(title="Номер телефона", examples=["79219873524"], default=None)]
    email: Annotated[str, Field(title="Адрес электронной почты", examples=["example@gmail.com"])]

    @model_validator(mode="before")
    def check_data(cls, values):
        user_phone = values.get('phone')
        if user_phone:
            try:
                valid_phone = validate_phone(user_phone)
                if valid_phone is None:
                    raise ValueError("Invalid phone number")
                else:
                    values["phone"] = valid_phone
            except:
                return ValueError("Invalid phone number")

        new_email = values.get("email")
        if new_email is not None:
            try:
                validated_email = validate_email(new_email)
                if validated_email is None:
                    raise ValueError("Invalid email.")
            except:
                raise ValueError("Invalid email.")

        return values
    
class SingInUser(BaseModel):
    email: Annotated[str, Field(title="Адрес электронной почты", examples=["example@gmail.com"])]
    password: Annotated[str, Field(title="Пароль", examples=["password"])]
    
    @model_validator(mode="before")
    def check_email(cls, values):
        user_email = values.get('email')
        if user_email:
            try:
                validated_email = validate_email(user_email)
                if validated_email is None:
                    raise ValueError("Invalid email.")
            except:
                raise ValueError("Invalid email.")

        return values