import requests
from base64 import b64encode
from datetime import date
import json
import os
from dotenv import load_dotenv
import ast

# Carregar variáveis do arquivo .env
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
contas = ast.literal_eval(os.getenv("CONTAS"))


def obter_token():
    auth = b64encode(f"{client_id}:{client_secret}".encode()).decode()
    url = "https://oauth.sandbox.bb.com.br/oauth/token"
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials", "scope": "extrato.conta-corrente"}
    r = requests.post(url, headers=headers, data=data)
    return r.json().get("access_token")


def consultar_extrato(token, agencia, numero, data_inicio, data_fim):
    url = "https://api.sandbox.bb.com.br/extrato/v1/contas-corrente/extrato"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "x-developer-key": client_id,
    }
    params = {
        "agencia": agencia,
        "numero": numero,
        "dataInicio": data_inicio,
        "dataFim": data_fim,
    }
    r = requests.get(url, headers=headers, params=params)
    return r.json()


def salvar_arquivo(extratos):
    with open(f"extrato_{date.today()}.json", "w") as f:
        json.dump(extratos, f, indent=4)


def main():
    token = obter_token()
    hoje = date.today().isoformat()
    extratos_total = []
    for conta in contas:
        extrato = consultar_extrato(
            token, conta["agencia"], conta["numero"], hoje, hoje
        )
        extratos_total.append({**conta, "extrato": extrato})
    salvar_arquivo(extratos_total)


if __name__ == "__main__":
    main()
