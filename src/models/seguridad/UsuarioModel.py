class Usuario():
    def __init__(self, id, id_persona, usuario, hash_password, password, activo, id_usuario_crea, fecha_crea, id_usuario_modifica, fecha_modifica) -> None:
        self.id = id
        self.id_persona = id_persona
        self.usuario = usuario
        self.hash_password = hash_password
        self.password = password
        self.activo = activo
        self.id_usuario_crea = id_usuario_crea
        self.fecha_crea = fecha_crea
        self.id_usuario_modifica = id_usuario_modifica
        self.fecha_modifica = fecha_modifica
