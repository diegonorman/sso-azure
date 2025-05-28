# SEMEQ SSO – Guia de Configuração e Replicação SSO Azure AD (SAML)

## O que foi configurado

### 1. Autenticação Local e SSO Azure AD
- Login local (usuário/senha) e login via SSO Azure AD usando SAML 2.0.
- Backend SAML com `djangosaml2`, integrando Django e Azure AD.

### 2. Segurança
- Variáveis sensíveis (SECRET_KEY, ALLOWED_HOSTS, URLs SAML) centralizadas no `.env`.
- Configurações de produção: SSL obrigatório, cookies seguros, HSTS, XSS, etc.
- SAML configurado para aceitar apenas respostas esperadas (`allow_unsolicited=False`), exigir assertions assinadas e requests assinadas (se necessário, com chave/certificado local).

### 3. Design e UX
- Interface responsiva e moderna com Bootstrap.
- Tela de login customizada com logo SEMEQ e tratamento amigável de erros SSO.

### 4. Documentação e Replicação
- README detalhado com deploy, variáveis, segurança e como replicar o SSO em outros projetos Django.

---

## Como foi configurado

### Dependências
No `requirements.txt`:
```
Django==4.2.21
python3-saml
djangosaml2>=1.10.1
django-bootstrap5
gunicorn
```

### Variáveis de ambiente (.env)
```env
AZURE_SSO_ACS=https://azure.semeq.com/sso/acs/
AZURE_SSO_LOGOUT=https://azure.semeq.com/logout
AZURE_SSO_METADATA_URL=https://login.microsoftonline.com/SEU_TENANT_ID/federationmetadata/2007-06/federationmetadata.xml?appid=SEU_APP_ID
SECRET_KEY=sua-secret-key
ALLOWED_HOSTS=azure.semeq.com,semeq-sso.onrender.com,sso-azure.onrender.com,localhost,127.0.0.1
```

### settings.py (principais pontos)
- Carrega variáveis do `.env` via `os.environ`.
- Configura o SAML:
  ```python
  SAML_CONFIG = {
      'xmlsec_binary': '/usr/bin/xmlsec1',
      'entityid': os.environ.get('AZURE_SSO_ENTITYID'),
      'service': {
          'sp': {
              'endpoints': {
                  'assertion_consumer_service': [
                      (os.environ.get('AZURE_SSO_ACS'), 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST'),
                  ],
                  'single_logout_service': [
                      (os.environ.get('AZURE_SSO_LOGOUT'), 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'),
                  ],
              },
              'allow_unsolicited': False,
              'authn_requests_signed': False,  # True se usar chave/certificado local
              'logout_requests_signed': True,
              'want_assertions_signed': True,
              'want_response_signed': False,
          },
      },
      'metadata': {
          'remote': [
              {'url': os.environ.get('AZURE_SSO_METADATA_URL')}
          ],
      },
      'debug': False,
      'key_file': '',  # Caminho do PEM se assinar requests
      'cert_file': '',
  }
  ```
- Mapeamento de atributos SAML para Azure AD:
  ```python
  SAML_ATTRIBUTE_MAPPING = {
      'name': ('username',),
      'givenName': ('first_name',),
      'surname': ('last_name',),
      'emailAddress': ('email',),
      # fallback URIs
      'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name': ('username',),
      'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname': ('first_name',),
      'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname': ('last_name',),
      'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress': ('email',),
  }
  ```
- Redirecionamento de falhas SSO:
  ```python
  SAML_FAILURE_REDIRECT = '/sso/error/'
  ```

---

## Exemplo: Como implementar SSO Azure AD SAML em outro Django

1. **Adicione as dependências** ao seu `requirements.txt`:
   ```
   Django
djangosaml2
python3-saml
django-bootstrap5
   ```
2. **Configure o Azure AD**:
   - Crie um “Enterprise Application” do tipo SAML.
   - Configure as URLs de ACS, Logout e Metadata conforme seu domínio.
   - Exporte o metadata XML do Azure e use a URL no seu `.env`.
3. **No seu settings.py**:
   - Importe `os` e leia variáveis do `.env`.
   - Configure o bloco `SAML_CONFIG` conforme acima.
   - Adicione `'djangosaml2'` ao `INSTALLED_APPS` e configure o backend.
4. **URLs**:
   - Inclua as rotas do djangosaml2:
     ```python
     path('sso/', include('djangosaml2.urls')),
     ```
5. **Templates**:
   - Crie uma tela de login que ofereça login local e via SSO.
   - Crie uma tela amigável para erros SSO.
6. **(Opcional) Assinatura de AuthnRequest**:
   - Gere um par de chaves PEM localmente:
     ```
     openssl req -x509 -newkey rsa:2048 -keyout saml.key -out saml.crt -days 365 -nodes -subj "/CN=seu-app"
     ```
   - Configure no `.env`:
     ```
     SAML_KEY_FILE=/caminho/absoluto/saml.key
     SAML_CERT_FILE=/caminho/absoluto/saml.crt
     ```
   - No `settings.py`:
     ```python
     'authn_requests_signed': True,
     'key_file': os.environ.get('SAML_KEY_FILE'),
     'cert_file': os.environ.get('SAML_CERT_FILE'),
     ```

---

## Por que foi feito assim?

- **Segurança**: Centralização de segredos, SSL, cookies seguros, HSTS, assinatura SAML.
- **Facilidade de replicação**: Separação de variáveis sensíveis, documentação clara, uso de padrões do Django.
- **Compatibilidade**: Mapeamento flexível de atributos SAML para Azure AD e outros IdPs.
- **UX**: Login bonito, responsivo, com tratamento de erros e identidade visual.

---

Se quiser um passo a passo ainda mais detalhado para outro projeto Django ou Python, posso gerar um guia específico!
