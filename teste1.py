import pyotp

# A chave secreta gerada anteriormente (base32)
# A chave secreta gerada no login é salva no banco de dados como `user.mfa_secret`
secret = "VBBJJVDCC22ZSZC5VJIDMUU5U3OP3JGP"  # Use a chave secreta gerada para o seu usuário

# Criando um objeto TOTP com a chave secreta
totp = pyotp.TOTP(secret)

# Gerando o código TOTP atual
code = totp.now()
print(f"Código gerado: {code}")

# Validando o código (se você quiser testar se o código funciona)
is_valid = totp.verify(code)
print(f"Código válido? {is_valid}")
