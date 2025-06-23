import os
import json
from datetime import date, datetime
import requests
from base64 import b64encode
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

# Carregar variáveis do .env
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
app_key = os.getenv("APP_KEY")
contas = json.loads(os.getenv("CONTAS"))
email_origem = os.getenv("EMAIL")
email_senha = os.getenv("EMAIL_PASSWORD")
destinatarios = json.loads(os.getenv("DESTINATARIOS", "[]"))


def formatar_extrato_texto(extrato):
    """Formata o extrato em um texto legível para e-mails."""
    texto_formatado = (
        f"Extrato da Conta {extrato['numero']} - Agência {extrato['agencia']}\n"
    )
    texto_formatado += f"Período: {extrato['dataInicio']} a {extrato['dataFim']}\n"
    texto_formatado += f"Saldo Inicial: R$ {extrato.get('saldoInicial', 0):.2f}\n"
    texto_formatado += f"Saldo Final: R$ {extrato.get('saldoFinal', 0):.2f}\n"
    texto_formatado += "Lançamentos:\n"
    for lancamento in extrato.get("lancamentos", []):
        tipo = "Crédito" if lancamento["tipo"] == "C" else "Débito"
        texto_formatado += (
            f"  - {lancamento['dataMovimento']}: {tipo} - "
            f"{lancamento['descricao']} - R$ {lancamento['valor']:.2f}\n"
        )
    texto_formatado += f"Total de Lançamentos: {len(extrato.get('lancamentos', []))}\n"
    return texto_formatado


def obter_token():
    """Obtém token de acesso da API do BB (sandbox)"""
    auth = b64encode(f"{client_id}:{client_secret}".encode()).decode()
    url = "https://oauth.sandbox.bb.com.br/oauth/token"
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data, timeout=30)
    if response.status_code in [200, 201]:
        token_data = response.json()
        token = token_data.get("access_token")
        if token:
            return token
    raise Exception(f"Erro ao obter token: {response.text}")


def consultar_extrato(token, agencia, numero, data_inicio, data_fim):
    """Consulta extrato no endpoint do sandbox."""
    endpoint = "https://api.sandbox.bb.com.br/extratos/v1/conta-corrente"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-developer-key": app_key,
    }
    params = {
        "agencia": agencia,
        "conta": numero,
        "dataInicio": data_inicio,
        "dataFim": data_fim,
    }
    response = requests.get(endpoint, headers=headers, params=params, timeout=30)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao consultar extrato: {response.text}")


def salvar_json_consolidado(extratos_total, data_ref):
    os.makedirs("extratos", exist_ok=True)
    json_path = f"extratos/extrato_bb_consolidado_{data_ref}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(extratos_total, f, indent=4, ensure_ascii=False, default=str)
    return json_path


def enviar_email(assunto, corpo, arquivos=[]):
    if not email_origem or not email_senha:
        print("❌ Credenciais de email não configuradas no .env")
        return False
    if not destinatarios:
        print("❌ Lista de destinatários vazia no .env")
        return False
    try:
        msg = EmailMessage()
        msg["Subject"] = assunto
        msg["From"] = email_origem
        msg["To"] = ", ".join(destinatarios)
        msg.set_content(corpo)
        for arquivo in arquivos:
            if os.path.exists(arquivo):
                with open(arquivo, "rb") as f:
                    conteudo = f.read()
                    nome = os.path.basename(arquivo)
                    msg.add_attachment(
                        conteudo, maintype="application", subtype="json", filename=nome
                    )
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_origem, email_senha)
            smtp.send_message(msg)
        print(f"✅ E-mail enviado com sucesso para {len(destinatarios)} destinatário(s)")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False


def main():
    print("=" * 70)
    hoje = date.today()
    data_inicio = hoje.strftime("%Y-%m-%d")
    data_fim = hoje.strftime("%Y-%m-%d")
    extratos_total = []
    try:
        token = obter_token()
    except Exception as e:
        print(f"❌ Erro ao obter token: {e}")
        return
    corpo_email = ""
    for conta in contas:
        agencia = conta.get("agencia")
        numero = conta.get("numero")
        try:
            extrato = consultar_extrato(token, agencia, numero, data_inicio, data_fim)
            extratos_total.append({"agencia": agencia, "numero": numero, "extrato": extrato})
            corpo_email += formatar_extrato_texto(extrato) + "\n\n"
        except Exception as e:
            corpo_email += f"Erro ao consultar extrato da conta {numero} agência {agencia}: {e}\n\n"
    data_ref = data_fim.replace("-", "")
    json_path = salvar_json_consolidado(extratos_total, data_ref)
    assunto = f"Extratos Bancários - {data_fim}"
    enviar_email(assunto, corpo_email, arquivos=[json_path])
    print(f"\n{'='*70}")
    print("🏁 PROCESSAMENTO CONCLUÍDO")
    print(f"   ⏰ Finalizado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
