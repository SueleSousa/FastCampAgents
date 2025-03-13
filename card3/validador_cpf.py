#criando um validador de cpf

from typing import Any #essa biblioteca é um suporte para tipos de dados
import re #biblioteca que procura padrões no texto
from pydantic import BaseModel, field_validator, Field #Pydant é uma biblioteca de validação de dados

#cria a classe CPF, informando quais os requisitos para o cpf
class CPF(BaseModel):
    numero: str = Field(...,
                        description = "CPF do usuário",
                        exemples=["123.456.789-09"],
                        min_length=11,
                        max_lenght=14
                        )

    @field_validator('numero')  #valida o número cpf que foi inserido
    @classmethod
    def validar_cpf(cls, v: str) -> str: #como estamos trabalhando com a classe CPF, se usa o cls para referenciar a classe
        cpf = re.sub(r'[^0-9]', '', v) #substitui tudo que não é número por nada

        if len(cpf) != 11:
            raise ValueError('CPF deve conter 11 dígitos') #se o cpf não tiver 11 dígitos, retorna um erro
        
        if len(set(cpf)) == 1:
            raise ValueError('CPF inválido: todos os dígitos são iguais') #se o cpf tiver todos os dígitos iguais, retorna um erro
        
        #validação dos dígitos verificadores 1 e 2, que são aqueles após o hífen. 
        #seguindo o p exemplo do site https://dicasdeprogramacao.com.br/algoritmo-para-validar-cpf/

        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = soma % 11
        digito1 = 0 if resto <2 else 11 - resto

        if int(cpf[9]) != digito1:
            raise ValueError('CPF inválido: primeiro dígito verificador incorreto')
       
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        if int(cpf[10]) != digito2:
            raise ValueError('CPF inválido: segundo dígito verificador incorreto')
            
        #Se forem aprovados na verificação, o cpf é validado e retorna o cpf formatado.
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
 

def main() -> None:
    # Testes com CPFs válidos e inválidos
    cpfs_teste = [
        "529.982.247-25",  
        "111.111.111-11",  
        "123.456.789-00",  
        "abc.def.ghi-jk",  
        "123.456.789",     
        "52998224725"      
    ]

    for cpf_teste in cpfs_teste:
        try:
            cpf = CPF(numero=cpf_teste)
            print(f"CPF válido: {cpf.numero}")
        except ValueError as e:
            print(f"CPF inválido ({cpf_teste}): {str(e)}")

if __name__ == "__main__":
    main()