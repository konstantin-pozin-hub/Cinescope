import json
from enum import Enum

from pydantic import BaseModel, field_validator, Field, EmailStr

from typing import Optional


class Roles(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    USER = "USER"


class UserModel(BaseModel):
    fullName: str
    email: EmailStr
    roles: list[Roles]
    password: str = Field(..., min_length=8)
    verified: Optional[bool] = None
    banned: Optional[bool] = None


class ProductType(str, Enum):
    clothes = "Clothes"
    electrotec = "Electrotec"


class Product(BaseModel):
    name: str
    price: float
    in_stock: bool
    type: ProductType


@field_validator("in_stock", mode="before")
def convert_boolean(cls, value):
    if isinstance(value, str):
        return value.lower() == "true"
    return value


t_short = Product(name="H_and_M", price=1000.04, in_stock="true", type=ProductType.clothes)

json_data = t_short.model_dump_json()  # Сериализация
print(json_data)
data_dict = json.loads(json_data)
check_t_short = Product(**data_dict)
again_t_short = t_short.model_validate_json(json_data)  # Десериализация
print(t_short)
