import enum
import hashlib #biblioteca para criptografar os dados
import re #biblioteca que procura padrões no texto
from typing import Any #essa biblioteca é um suporte para tipos de dados

#Pydant é uma biblioteca de validação de dados
from pydantic import (
    BaseModel, #essa é a base de toda a validação dos dados da biblioteca pydantic
    EmailStr, #no caso valida se o e-mail está num formato válido
    Field, #função que permite adicionar mais informações às nossas funções, dados, etc
    field_validator, #valida campos específicos do modelo
    model_validator, #valida o modelo como um todo
    SecretStr, #função que permite esconder o valor de uma string
    ValidationError, #função para validação de dados
)

#Regex que valida o user e o passaword

VALID_PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
VALID_NAME_REGEX = re.compile(r"^[a-zA-Z]{2,}$")

 #define o objeto role, que é composto de autor, editor, desenvolvedor e administrador
class Role(enum.IntFlag):
    Author = 1
    Editor = 2
    Admin = 4
    SuperAdmin = 8

#define o objeto user, composto de nome, email, password e role
class User(BaseModel):
    name: str = Field(examples=["Arjan"])
    email: EmailStr = Field(
        examples=["user@arjancodes.com"],
        description="The email address of the user",
        frozen=True,
    )
    password: SecretStr = Field(
        examples=["Password123"], description="The password of the user"
    )
    role: Role = Field(
        default=None, description="The role of the user", examples=[1, 2, 4, 8]
    )
    #nesse objeto utilizou a função Field do Pydantic para dar exemplos de quais dados estão corretos

    #usa o field_validator para validar especificamente alguns campos do modelo
    @field_validator("name")
    @classmethod #É uma função que pode ser chamada sem precisar de uma instância na classe
    def validate_name(cls, v: str) -> str:
        if not VALID_NAME_REGEX.match(v):
            raise ValueError(
                "Name is invalid, must contain only letters and be at least 2 characters long"
            )
        return v

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, v: int | str | Role) -> Role:
        op = {int: lambda x: Role(x), str: lambda x: Role[x], Role: lambda x: x}
        try:
            return op[type(v)](v)
        except (KeyError, ValueError):
            raise ValueError(
                f"Role is invalid, please use one of the following: {', '.join([x.name for x in Role])}"
            )

    @model_validator(mode="before")
    @classmethod
    def validate_user(cls, v: dict[str, Any]) -> dict[str, Any]:
        if "name" not in v or "password" not in v:
            raise ValueError("Name and password are required")
        if v["name"].casefold() in v["password"].casefold():
            raise ValueError("Password cannot contain name")
        if not VALID_PASSWORD_REGEX.match(v["password"]):
            raise ValueError(
                "Password is invalid, must contain 8 characters, 1 uppercase, 1 lowercase, 1 number"
            )
        v["password"] = hashlib.sha256(v["password"].encode()).hexdigest()
        return v


def validate(data: dict[str, Any]) -> None: #essa é a função criada para validar os dados inseridos no user
    try:
        user = User.model_validate(data) #utiliza a biblioteca model_validade para validar os dados
        print(user)
    except ValidationError as e: #caso os dados não sejam válidos, a mesangem de erro é mostrada
        print("User is invalid:")
        print(e)


def main() -> None: #essa é a função principal que chama as funções de validação
    test_data = dict(
        good_data={
            "name": "Arjan",
            "email": "example@arjancodes.com",
            "password": "Password123",
            "role": "Admin",
        },
        bad_role={
            "name": "Arjan",
            "email": "example@arjancodes.com",
            "password": "Password123",
            "role": "Programmer",
        },
        bad_data={
            "name": "Arjan",
            "email": "bad email",
            "password": "bad password",
        },
        bad_name={
            "name": "Arjan<-_->",
            "email": "example@arjancodes.com",
            "password": "Password123",
        },
        duplicate={
            "name": "Arjan",
            "email": "example@arjancodes.com",
            "password": "Arjan123",
        },
        missing_data={
            "email": "<bad data>",
            "password": "<bad data>",
        },
    )

    for example_name, data in test_data.items():
        print(example_name)
        validate(data)
        print()


if __name__ == "__main__":
    main()