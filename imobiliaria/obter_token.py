# Configuração para permitir execução desse script sem estar no contexto do projeto Django
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imobiliaria.settings')

application = get_wsgi_application()

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from dotenv import load_dotenv
# Carrega as variáveis de ambiente
load_dotenv()

username = os.getenv('SUPERUSER_NAME')
password = os.getenv('SUPERUSER_PASSWORD')

# Obtém o usuário existente ou cria um novo
user, created = User.objects.get_or_create(username=username, defaults={'password': password})

if created:
    print(f"\nNovo usuário {username} criado.")
else:
    print(f"\nUsuário {username} já existia.")

# Gera o token de acesso
refresh = RefreshToken.for_user(user)

print("----------------------------------------------\n")
print("A duração do ACCESS TOKEN é de 12 horas e do REFRESH TOKEN de 30 dias.\n")
print("Utilize do REFRESH TOKEN para obter um novo ACCESS TOKEN através de um request para 'api/token/refresh/'\n\n")
print(f"ACCESS TOKEN: {str(refresh.access_token)}\n")
print(f"REFRESH TOKEN: {str(refresh)}\n\n")
print("----------------------------------------------")