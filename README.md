# 📄 BB Extrato Automático

Aplicação Python para consultar e salvar diariamente o extrato bancário de contas do Banco do Brasil, utilizando a API oficial do BB (via portal BB Developers).

---

## ✅ Funcionalidades

- Autenticação via OAuth2 (client credentials)
- Consulta ao extrato bancário por intervalo de datas
- Suporte a múltiplas contas
- Salvamento em arquivo `.json` com data do dia
- Leitura de credenciais e dados sensíveis a partir de variáveis de ambiente (`.env`)

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
cd bb-extrato
Crie e ative um ambiente virtual (opcional, mas recomendado):

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
Instale as dependências:

pip install -r requirements.txt

🔐 Arquivo .env
Crie um arquivo .env na raiz do projeto com as seguintes variáveis:
.env:
CLIENT_ID=seu_client_id_aqui
CLIENT_SECRET=seu_client_secret_aqui

# Contas para consulta
CONTA_1_AGENCIA=1234
CONTA_1_NUMERO=56789

CONTA_2_AGENCIA=1111
CONTA_2_NUMERO=22222

▶️ Como Usar
Execute o script principal:

python extrato.py
O extrato será salvo como:
extrato_2025-06-09.json

🧪 Testes com Postman
Você pode testar os endpoints da API diretamente no Postman. A coleção pronta está disponível no arquivo:

bb_extrato_sandbox.postman_collection.json

⚠️ Observações
Esta aplicação usa o ambiente sandbox do BB.

Para acesso real, é necessário:

Certificado digital A1

Aprovação formal do BB

Gerente de relacionamento para intermediar o processo

📄 Licença
Este projeto é open-source sob a licença MIT. Veja o arquivo LICENSE para mais informações.

📬 Contato
Desenvolvido por Samuel Lima Alves
Email: contatosamuel.lima23@gmail.com