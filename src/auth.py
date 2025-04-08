def validar_usuario(login_digitado: str, df_usuarios) -> bool:
    logins_validos = df_usuarios["Login"].astype(str).str.strip().tolist()
    return login_digitado.strip().zfill(11) in logins_validos