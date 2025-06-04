# Flasky Recetas - Sistema de Compartir Recetas

Este proyecto es una aplicación web desarrollada con Flask que permite a los usuarios compartir recetas, encontrar usuarios con gustos similares y gestionar sus propias recetas.

## Características principales
- Registro e inicio de sesión de usuarios
- Publicación, visualización y eliminación de recetas
- Relación automática de usuarios con gustos similares según los ingredientes de sus recetas
- Interfaz moderna y fácil de usar
- Listado de usuarios y acceso a perfiles

## Requisitos
- Python 3.8+
- PostgreSQL
- (Recomendado) Entorno virtual Python

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd flasky-master
   ```

2. **Crea y activa un entorno virtual:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # En Windows

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos:**
   - Crea una base de datos PostgreSQL (por ejemplo, `flasky_db`).
   - Ajusta la cadena de conexión en `config.py` si es necesario.

5. **Inicializa la base de datos:**
   ```bash
   flask db upgrade
   flask init-db
   ```

6. **(Opcional) Normaliza ingredientes y relaciones:**
   ```bash
   flask update-similar-users
   ```

7. **Ejecuta la aplicación:**
   ```bash
   flask run
   ```

## Uso
- Accede a `http://localhost:5000` en tu navegador.
- Regístrate o inicia sesión con un usuario existente.
- Publica recetas, explora las de otros usuarios y elimina las tuyas si lo deseas.
- Visita el perfil de cualquier usuario para ver con quién tiene gustos similares.

## Funcionalidad de usuarios similares
- Cuando publicas una receta, el sistema compara los ingredientes con los de otros usuarios.
- Si tienes al menos 2 ingredientes en común con otro usuario, se crea una relación automática de gustos similares.
- Puedes ver estos usuarios en tu perfil.

## Comandos útiles
- `flask update-similar-users`: Normaliza los ingredientes de todas las recetas y actualiza las relaciones de gustos similares entre usuarios.
- `flask init-db`: Inicializa la base de datos.

## Notas de seguridad
- Las contraseñas se almacenan de forma segura usando hashes.
- No uses contraseñas en texto plano en la base de datos.

## Créditos
- Desarrollado por [Xavier Gordillo]
- Basado en Flask, SQLAlchemy y Bootstrap

