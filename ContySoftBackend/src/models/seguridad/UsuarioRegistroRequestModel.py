class UsuarioRegistroRequest:
    def __init__(self, ruc, razon_social, tipo_persona, usuario_sol, password_sol, usuario, password, id_plan) -> None:
        self.ruc = ruc
        self.razon_social = razon_social
        self.tipo_persona = tipo_persona
        self.usuario_sol = usuario_sol
        self.password_sol = password_sol
        self.usuario = usuario
        self.password = password
        self.id_plan = id_plan