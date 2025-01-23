#  minha_aplicacao/views.py
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
from .models import Sobremesa
from .forms import SobremesaForm  # Importando o formulário

# Configuração de logging
logger = logging.getLogger(__name__)

def home(request):
    logger.debug("Acessando a página inicial.")
    return render(request, 'home.html')  # Retorne o template da página inicial

# @login_required
def logado_view(request):
    logger.debug(f"Usuário {request.user.username} acessando a página logado.")
    return render(request, 'logado.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

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

            # Registrar o usuário no sistema 
            login(request, user)
            
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
            return render(request, 'accounts/mfa_verify.html', {'user': user, 'qr_code': qr_code_base64, 'user_id': user.id})
        else:
            logger.warning(f"Falha ao autenticar o usuário: {username}.")
            return render(request, 'accounts/login.html', {'error': 'Invalid login'})
    
    return render(request, 'accounts/login.html')


# View para verificar o código MFA
# @login_required
def mfa_verify_view(request):
    user_id = request.POST.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.warning(f"Usuário com ID {user_id} não encontrado.")
        return render(request, 'accounts/mfa_verify.html', {'error': 'Usuário não encontrado'})

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)
        logger.debug(f"Perfil de usuário criado para {user.username}")

    # Garantir que o usuário tenha uma chave secreta
    if not user_profile.mfa_secret:
        user_profile.mfa_secret = pyotp.random_base32()
        user_profile.save()
        logger.debug(f"Chave secreta gerada para o usuário {user.username}: {user_profile.mfa_secret}")

    # Gerar QR Code novamente
    totp = pyotp.TOTP(user_profile.mfa_secret)
    qr_data = totp.provisioning_uri(name=user.username, issuer_name="MeuProjeto")
    img = qrcode.make(qr_data)
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    qr_code_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    if request.method == 'POST':
        code = request.POST.get('mfa_code')

        if not code:
            logger.warning("Código MFA não fornecido pelo usuário.")
            return render(request, 'accounts/mfa_verify.html', {
                'error': 'Código não fornecido',
                'user': user,
                'qr_code': qr_code_base64,
                'user_id': user.id
            })

        if totp.verify(code):
            logger.debug(f"Código MFA verificado com sucesso para o usuário: {user.username}.")
            return redirect('logado')
        else:
            logger.warning(f"Código MFA inválido para o usuário: {user.username}.")
            return render(request, 'accounts/mfa_verify.html', {
                'error': 'Código inválido',
                'user': user,
                'qr_code': qr_code_base64,
                'user_id': user.id
            })

    return render(request, 'accounts/mfa_verify.html', {
        'user': user,
        'qr_code': qr_code_base64,
        'user_id': user.id
    })

def menu_view(request):
    return render(request, 'menu.html')

def item1_view(request):
    return render(request, 'item1.html')

def sobre_view(request):
    sobremesas = Sobremesa.objects.all()  # Recupera todas as sobremesas do banco de dados
    return render(request, 'sobre.html', {'sobremesas': sobremesas})

def item2_view(request):
    return render(request, 'bebidas.html')

def item1_content(request):
    return render(request, 'item1_content.html')

def item2_content(request):
    return render(request, 'item2_content.html')

def item3_content(request):
    return render(request, 'sobre_content.html')


from django.shortcuts import render, redirect
from .models import Sobremesa

def adicionar_sobremesa_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        imagem = request.FILES.get('imagem')  # Captura o arquivo de imagem enviado

        Sobremesa.objects.create(
            nome=nome,
            descricao=descricao,
            preco=preco,
            imagem=imagem
        )
        return redirect('sobremesas')  # Redireciona para a lista de sobremesas

    return render(request, 'adicionar_sobremesa.html')

def sobremesas_view(request):
    sobremesas = Sobremesa.objects.all()  # Recupera todas as sobremesas do banco de dados
    return render(request, 'sobremesas.html', {'sobremesas': sobremesas})
