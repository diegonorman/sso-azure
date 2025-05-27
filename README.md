# SEMEQ SSO

Projeto Django com autenticação local personalizada e SSO Azure AD via SAML.

## Como rodar localmente

1. Crie e ative o ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute as migrações:
   ```bash
   python manage.py migrate
   ```
4. Crie o usuário admin:
   ```bash
   python manage.py createsuperuser --username admin --email admin@semeq.com
   # Use a senha: admin
   ```
5. Rode o servidor:
   ```bash
   python manage.py runserver
   ```

Acesse http://localhost:8000 para testar.

## SSO Azure AD

- Configure as URLs SAML no Azure conforme instruções do README.
- Domínio de produção: https://azure.semeq.com

## Estilo

- Interface clean, responsiva, com Bootstrap.
- Tela de login com logo da SEMEQ.
# sso-azure
