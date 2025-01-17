
from django.contrib.auth.models import User

# Encontrar um usuário pelo nome de usuário
user = User.objects.get(username='francisco')

# Acessar o perfil do usuário
user_profile = user.userprofile

# Exibir o mfa_secret
print(user_profile.mfa_secret)
