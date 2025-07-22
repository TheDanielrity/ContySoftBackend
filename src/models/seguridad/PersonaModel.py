class Persona():
    def __init__(self, id, nombres, apellidos, telefono, email, id_tipo_persona, activo, id_usuario_crea, fecha_crea, id_usuario_modifica, fecha_modifica) -> None:
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono
        self.email = email
        self.id_tipo_persona = id_tipo_persona
        self.activo = activo
        self.id_usuario_crea = id_usuario_crea
        self.fecha_crea = fecha_crea
        self.id_usuario_modifica = id_usuario_modifica
        self.fecha_modifica = fecha_modifica