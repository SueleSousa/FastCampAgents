from enum import auto, IntFlag #a biblioteca enum permite criar numerações
from typing import Any #essa biblioteca é um suporte para tipos de dados

#Pydant é uma biblioteca de validação de dados
from pydantic import (
    BaseModel, #essa é a base de toda a validação dos dados da biblioteca pydantic
    EmailStr, #no caso valida se o e-mail está num formato válido
    Field,  #função que permite adicionar mais informações às nossas funções, dados, etc
    SecretStr, #função que permite esconder o valor de uma string
    ValidationError, #função para validação de dados
)


class Role(IntFlag): #define o objeto role, que é composto de autor, editor, desenvolvedor e administrador
    Author = auto()    
    Editor = auto() 
    Developer = auto() 
    Admin = Author | Editor | Developer #combinação de todos os dados anteriores


class User(BaseModel): #define o objeto user, composto de nome, email, password e role
    name: str = Field(examples=["Arjan"]) 
    email: EmailStr = Field(
        examples=["example@arjancodes.com"],
        description="The email address of the user",
        frozen=True,
    )
    password: SecretStr = Field(
        examples=["Password123"], description="The password of the user"
    )
    role: Role = Field(default=None, description="The role of the user")

    #nesse objeto utilizou a função Field do Pydantic para dar exemplos de quais dados estão corretos

def validate(data: dict[str, Any]) -> None: #essa é a função criada para validar os dados inseridos no user
    try:
        user = User.model_validate(data) #utiliza a biblioteca model_validade para validar os dados
        print(user)
    except ValidationError as e: #caso os dados não sejam válidos, a mesangem de erro é mostrada
        print("User is invalid")
        for error in e.errors():
            print(error)


def main() -> None: #essa é a função principal que chama as funções de validação
    good_data = {
        "name": "Arjan",
        "email": "example@arjancodes.com",
        "password": "Password123",
    }
    bad_data = {"email": "<bad data>", "password": "<bad data>"}

    validate(good_data)
    validate(bad_data)


if __name__ == "__main__":
    main()