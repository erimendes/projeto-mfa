import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import pyotp
import qrcode
from io import BytesIO
from .models import UserProfile
import base64
from django.contrib.auth.models import User
from minha_aplicacao.models import UserProfile

# Configuração de logging
logger = logging.getLogger(__name__)

def home(request):
    logger.debug("Acessando a página inicial.")
    return render(request, 'home.html')  # Retorne o template da página inicial

# View de login com MFA
def login_view(request):
    logger.debug("Iniciando processo de login.")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        logger.debug(f"Tentando autenticar usuário: {username}")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            logger.debug(f"Usuário {username} autenticado com sucesso.")
            
            # Garantir que o UserProfile existe
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            
            # Gerar ou pegar a chave secreta do usuário
            if created or not user_profile.mfa_secret:
                user_profile.mfa_secret = pyotp.random_base32()  # Gerar chave secreta
                user_profile.save()  # Salvar no banco de dados
                logger.debug(f"Chave secreta gerada para o usuário {username}.")

            
            
            # Gerar a URL do TOTP
            totp = pyotp.TOTP(user_profile.mfa_secret)
            qr_data = totp.provisioning_uri(name=user.username, issuer_name="MeuProjeto")
            
            # Gerar QR Code a partir da URL
            img = qrcode.make(qr_data)
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            
            # Codificar a imagem em base64
            qr_code_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
            
            logger.debug(f"QR Code gerado para o usuário {username}.")


            print(f"estou aqui {username}")
            # Exibir a chave secreta (opcional, para depuração)
            print(f"Chave secreta gerada: {user_profile.mfa_secret}")
            
            # Passando a chave secreta e o QR Code para o template
            return render(request, 'accounts/mfa_verify.html', {'user': user, 'qr_code': qr_code_base64})
        else:
            logger.warning(f"Falha ao autenticar o usuário: {username}.")
            return render(request, 'accounts/login.html', {'error': 'Invalid login'})
    
    return render(request, 'accounts/login.html')


# View para verificar o código MFA
@login_required
def mfa_verify(request):
    # Garantir que o mfa_secret exista para o usuário
    user = request.user
    try:
        # Tenta obter o perfil do usuário
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        # Se o perfil não existir, cria um novo
        user_profile = UserProfile.objects.create(user=user)
        logger.debug(f"Perfil de usuário criado para {user.username}")

    # Verificar se o usuário tem mfa_secret e, se não, gerar uma nova chave secreta
    if not user_profile.mfa_secret:
        logger.debug(f"Usuário {user.username} não tem chave MFA. Gerando uma chave para ele.")
        user_profile.mfa_secret = pyotp.random_base32()  # Gerar chave secreta
        user_profile.save()  # Salvar a chave secreta no banco de dados
        logger.debug(f"Chave secreta gerada: {user_profile.mfa_secret}")

    if request.method == 'POST':
        code = request.POST.get('mfa_code')

        # Log para depurar o código recebido
        logger.debug(f"Código MFA recebido: {code}")
        print(f"Código MFA recebido: {code}")
        print(f"Chave secreta recebido: {user_profile.mfa_secret}")

        if not code:
            logger.warning("Código MFA não foi fornecido pelo usuário.")
            return render(request, 'accounts/mfa_verify.html', {'error': 'Código não fornecido'})

        # Gerar o TOTP baseado na chave secreta do usuário
        totp = pyotp.TOTP(user_profile.mfa_secret)
        
        # Adicionando um log para ver o código gerado
        generated_code = totp.now()
        logger.debug(f"Código gerado para verificação: {generated_code}")
        print(f"Código gerado para verificação: {generated_code}")

        # Verificar se o código MFA é válido
        if totp.verify(code):
            logger.debug(f"Código MFA verificado com sucesso para o usuário: {user.username}. Redirecionando.")
            return redirect('home')  # Redireciona para a página inicial após a verificação do código
        else:
            logger.warning(f"Código MFA inválido para o usuário: {user.username}.")
            return render(request, 'accounts/mfa_verify.html', {'error': 'Código inválido'})

    # Se não for um POST, apenas renderize o formulário de verificação
    return render(request, 'accounts/mfa_verify.html')




@login_required
def logado(request):
    logger.debug(f"Usuário {request.user.username} acessando a página logado.")
    return render(request, 'logado.html')
