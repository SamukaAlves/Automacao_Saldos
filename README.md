# 📄 BB Extrato Automático

Automação em Python para consultar extratos bancários de múltiplas contas do Banco do Brasil via API oficial (BB Developers), salvar o resultado em JSON consolidado e enviar o extrato formatado por e-mail.

---

## ✅ Funcionalidades

- Autenticação OAuth2 (client credentials)
- Consulta de extrato bancário por período (padrão: mês atual)
- Suporte a múltiplas contas
- Salvamento do extrato consolidado em arquivo `.json`
- Envio automático do extrato formatado no corpo do e-mail (um resumo por conta)
- Leitura de credenciais e dados sensíveis via `.env`

---

## 🛠️ Pré-requisitos

- Conta no Banco do Brasil
- Aplicativo criado no [BB Developers](https://developers.bb.com.br/)
- Python 3.8 ou superior
- Variáveis `.env` configuradas corretamente

---

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/SamukaAlves/Automacao_Saldos.git
cd Automacao_Extratos
```
2. Crie e ative um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```

---

## 🔐 Configuração do `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte formato:

```
CLIENT_ID=seu_client_id
CLIENT_SECRET=seu_client_secret
APP_KEY=sua_app_key
EMAIL=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_aplicativo
CONTAS=[{"agencia": "1234", "numero": "56789"}, {"agencia": "1111", "numero": "22222"}]
DESTINATARIOS=["destinatario1@email.com", "destinatario2@email.com"]
```

- `CONTAS` e `DESTINATARIOS` devem ser listas em formato JSON.
- Recomenda-se usar senha de aplicativo para o Gmail.

---

## ▶️ Como Usar

Execute o script principal:
```bash
python main.py
```
- O extrato consolidado será salvo em `extratos/extrato_bb_consolidado_<data>.json`.
- O e-mail será enviado automaticamente para os destinatários configurados, com o extrato formatado no corpo e o JSON em anexo.

---

## ⚠️ Observações

- O script está configurado para ambiente **sandbox** do BB. Para produção, ajuste as URLs e credenciais conforme necessário.
- Não há geração de arquivos Excel ou CSV.
- O período padrão é o dia atual, mas pode ser facilmente alterado no código.

---

## 📄 Licença

Este projeto é open-source sob a licença MIT. Veja o arquivo LICENSE para mais informações.

---

## 📬 Contato

Desenvolvido por Samuel Lima Alves  
Email: contatosamuel.lima23@gmail.com