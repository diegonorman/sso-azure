# SEMEQ SSO – Guia de Configuração e Replicação SSO Azure AD (SAML)

## O que foi configurado

- Autenticação local personalizada e SSO Azure AD via SAML 2.0.
- Backend SAML com `djangosaml2`.
- Variáveis sensíveis (SECRET_KEY, ALLOWED_HOSTS, URLs SAML) centralizadas no `.env`.
- Segurança: SSL obrigatório, cookies seguros, HSTS, XSS, etc.
- Interface responsiva com Bootstrap e tela de login customizada.
- Dockerfile e build.sh para deploy automatizado.
- README detalhado para replicação do SSO em outros projetos Django.

---

## Como rodar localmente

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute as migrações:
   ```bash
   python manage.py migrate
   ```
3. Crie o usuário admin:
   ```bash
   python manage.py createsuperuser --username admin --email admin@semeq.com
   # Use a senha: admin
   ```
4. Rode o servidor:
   ```bash
   python manage.py runserver
   ```

Acesse http://localhost:8000 para testar.

---

## SSO Azure AD

- Configure as URLs SAML no Azure conforme abaixo.
- Domínio de produção: https://azure.semeq.com

### Dependências (requirements.txt)
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
AZURE_SSO_METADATA_URL=https://login.microsoftonline.com/6e89e984-81f7-4e1d-b40b-d638ccf7c2b0/federationmetadata/2007-06/federationmetadata.xml?appid=dfb62140-482c-45ad-9078-5833ff72dcd2
SECRET_KEY=django-insecure-dga^#&+du$kr$q$_#zaxy&nbi55=q0qbop=8t@wiu%$m%(e1qr)
ALLOWED_HOSTS=azure.semeq.com,semeq-sso.onrender.com,sso-azure.onrender.com,localhost,127.0.0.1
```

### settings.py (principais pontos)
- Configuração de autenticação local e SSO SAML:
  ```python
  INSTALLED_APPS = [
      ...
      'authentication',
      'django_bootstrap5',
      'djangosaml2',
  ]
  MIDDLEWARE = [
      ...
      'django.contrib.sessions.middleware.SessionMiddleware',
      'semeq_sso.settings.EnsureSessionMiddleware',
      'djangosaml2.middleware.SamlSessionMiddleware',
      ...
  ]
  SAML_CONFIG = {
      'xmlsec_binary': '/usr/bin/xmlsec1',
      'entityid': 'https://azure.semeq.com/sso/metadata',
      'service': {
          'sp': {
              'endpoints': {
                  'assertion_consumer_service': [
                      ('https://azure.semeq.com/sso/acs/', 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST'),
                  ],
                  'single_logout_service': [
                      ('https://azure.semeq.com/logout', 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'),
                  ],
              },
              'allow_unsolicited': True,
              'authn_requests_signed': False,
              'logout_requests_signed': True,
              'want_assertions_signed': True,
              'want_response_signed': False,
          },
      },
      'metadata': {
          'remote': [
              {'url': 'https://login.microsoftonline.com/6e89e984-81f7-4e1d-b40b-d638ccf7c2b0/federationmetadata/2007-06/federationmetadata.xml?appid=dfb62140-482c-45ad-9078-5833ff72dcd2'}
          ],
      },
      'debug': True,
      'key_file': '',
      'cert_file': '',
  }
  SAML_ATTRIBUTE_MAPPING = {
      'name': ('username',),
      'givenName': ('first_name',),
      'surname': ('last_name',),
      'emailAddress': ('email',),
      'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name': ('username',),
      'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname': ('first_name',),
      'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname': ('last_name',),
      'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress': ('email',),
  }
  SAML_USE_NAME_ID_AS_USERNAME = False
  SAML_FAILURE_REDIRECT = '/sso/error/'
  ```
- URLs principais:
  ```python
  urlpatterns = [
      path('', auth_views.custom_login, name='root_login'),
      path('admin/', admin.site.urls),
      path('login/', auth_views.custom_login, name='login'),
      path('logout/', auth_views.custom_logout, name='logout'),
      path('dashboard/', auth_views.dashboard, name='dashboard'),
      path('sso/', include('djangosaml2.urls')),
      path('sso/acs', include('djangosaml2.urls')),
      path('sso/error/', views.sso_error, name='sso_error'),
  ]
  ```
- Views principais:
  ```python
  def custom_login(request): ...
  def custom_logout(request): ...
  @login_required
def dashboard(request): ...
  def sso_error(request): ...
  ```
- Templates:
  - `login.html`: Tela de login local com Bootstrap e logo SEMEQ.
  - `sso_error.html`: Mensagem amigável para falha de SSO.
  - `dashboard.html`: Tela pós-login.
  - `base.html`: Layout base com Bootstrap e navbar SEMEQ.

---

## Exemplo: Como implementar SSO Azure AD SAML em outro Django

1. Adicione as dependências ao seu `requirements.txt`:
   ```
   Django
djangosaml2
python3-saml
django-bootstrap5
   ```
2. Configure o Azure AD:
   - Crie um “Enterprise Application” do tipo SAML.
   - Configure as URLs de ACS, Logout e Metadata conforme seu domínio.
   - Use a URL de metadata do Azure no seu `.env`.
3. No seu settings.py:
   - Configure o bloco `SAML_CONFIG` conforme acima.
   - Adicione `'djangosaml2'` ao `INSTALLED_APPS` e configure o backend.
4. URLs:
   - Inclua as rotas do djangosaml2:
     ```python
     path('sso/', include('djangosaml2.urls')),
     ```
5. Templates:
   - Crie uma tela de login que ofereça login local e via SSO.
   - Crie uma tela amigável para erros SSO.

---

## Guia detalhado: Como implementar SSO Azure AD SAML em outro projeto Django ou Python

### 1. Dependências
Adicione ao seu `requirements.txt`:
```
Django
djangosaml2
python3-saml
django-bootstrap5
gunicorn
```

### 2. Configuração do Azure AD
- No portal Azure, crie um novo "Aplicativo Empresarial" do tipo SAML.
- Defina as URLs:
  - **ACS (Assertion Consumer Service):** `https://SEU_DOMINIO/sso/acs/`
  - **Logout:** `https://SEU_DOMINIO/logout`
  - **EntityID:** `https://SEU_DOMINIO/sso/metadata`
- Copie a URL de metadata gerada pelo Azure AD para usar no seu `.env`.
- No Azure, configure os atributos de saída para garantir que `name`, `givenName`, `surname`, `emailAddress` estejam presentes.

### 3. Variáveis de ambiente (.env)
Exemplo:
```env
AZURE_SSO_ACS=https://SEU_DOMINIO/sso/acs/
AZURE_SSO_LOGOUT=https://SEU_DOMINIO/logout
AZURE_SSO_METADATA_URL=https://login.microsoftonline.com/SEU_TENANT_ID/federationmetadata/2007-06/federationmetadata.xml?appid=SEU_APP_ID
SECRET_KEY=sua-secret-key
ALLOWED_HOSTS=SEU_DOMINIO,localhost,127.0.0.1
```

### 4. settings.py
- Adicione `'djangosaml2'` e `'django_bootstrap5'` ao `INSTALLED_APPS`.
- Configure o SAML conforme exemplo abaixo:
```python
SAML_CONFIG = {
    'xmlsec_binary': '/usr/bin/xmlsec1',
    'entityid': os.environ.get('AZURE_SSO_ENTITYID', 'https://SEU_DOMINIO/sso/metadata'),
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
            'allow_unsolicited': True,
            'authn_requests_signed': False,
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
    'debug': True,
    'key_file': '',
    'cert_file': '',
}
SAML_ATTRIBUTE_MAPPING = {
    'name': ('username',),
    'givenName': ('first_name',),
    'surname': ('last_name',),
    'emailAddress': ('email',),
    'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name': ('username',),
    'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname': ('first_name',),
    'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname': ('last_name',),
    'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress': ('email',),
}
SAML_USE_NAME_ID_AS_USERNAME = False
SAML_FAILURE_REDIRECT = '/sso/error/'
```

### 5. URLs
No seu `urls.py`:
```python
from django.urls import path, include
from authentication import views as auth_views
urlpatterns = [
    path('', auth_views.custom_login, name='root_login'),
    path('login/', auth_views.custom_login, name='login'),
    path('logout/', auth_views.custom_logout, name='logout'),
    path('dashboard/', auth_views.dashboard, name='dashboard'),
    path('sso/', include('djangosaml2.urls')),
    path('sso/acs', include('djangosaml2.urls')),
    path('sso/error/', auth_views.sso_error, name='sso_error'),
]
```

### 6. Views
Exemplo de views para login local, logout, dashboard e erro SSO:
```python
def custom_login(request): ...
def custom_logout(request): ...
@login_required
def dashboard(request): ...
def sso_error(request): ...
```

### 7. Templates
- `login.html`: Tela de login local com Bootstrap e logo.
- `sso_error.html`: Mensagem amigável para falha de SSO.
- `dashboard.html`: Tela pós-login.
- `base.html`: Layout base com Bootstrap e navbar.

### 8. Docker e Deploy (opcional)
- Use o `Dockerfile` e `build.sh` como exemplo para deploy automatizado.
- O Dockerfile já instala dependências de sistema para SAML.

### 9. Teste o fluxo
- Faça login local e via SSO Azure AD.
- Teste o tratamento de erros e o redirecionamento amigável.

---

**Dica:**
Se precisar de assinatura de AuthnRequest, gere um par de chaves PEM e configure no settings e no Azure AD.

Pronto! Com esse guia, você consegue adaptar o SSO Azure AD/SAML para qualquer projeto Django ou Python.

