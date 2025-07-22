# ContySoftBackend

**ContySoftBackend** es una API desarrollada en Python utilizando Flask, diseñada como backend de un sistema orientado a la SUNAT. El proyecto implementa una arquitectura en N capas y está enfocado en el trabajo colaborativo entre desarrolladores internos.

## 🛠 Tecnologías Utilizadas

- **Lenguaje:** Python 3.x  
- **Framework:** Flask  
- **Base de Datos:** SQL Server  
- **Arquitectura:** N capas (Separación de responsabilidades en controladores, servicios, modelos y acceso a datos)  
- **Gestión de dependencias:** `requirements.txt`


## 🚀 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/TheDanielrity/ContySoftBackend.git
cd ContySoftBackend
```

2. Crea y activa un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala los requerimientos del proyecto:

```bash
pip install -r requirements.txt
```

4. Configura tu conexión a SQL Server dentro del archivo de configuración correspondiente (por ejemplo, `.env` o una clase `Config`).

## ▶️ Ejecución

Ejecuta la aplicación localmente con el siguiente comando:

```bash
python main.py
```

La aplicación se iniciará en el puerto configurado, por defecto suele ser `http://localhost:5000`.

## 👥 Uso y Alcance

Este proyecto está destinado exclusivamente para uso interno por parte de colaboradores del equipo de desarrollo. No está diseñado para ser desplegado en entornos públicos sin autenticación ni validación adecuada.

## 🤝 Contribuciones

Si deseas colaborar en este proyecto:

1. Realiza un fork del repositorio.
2. Crea una nueva rama: `git checkout -b feature/mi-aporte`.
3. Aplica tus cambios y haz commit: `git commit -m "Agrega nueva funcionalidad"`.
4. Envía un pull request con una descripción detallada.

## 📄 Licencia

Este proyecto es privado y no cuenta con una licencia pública.
