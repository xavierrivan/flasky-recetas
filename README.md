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
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos:**
   - Crea una base de datos PostgreSQL
   - Ajusta la configuración de la base de datos según tus necesidades

5. **Inicializa la base de datos:**
   ```bash
   flask db upgrade
   flask init-db
   ```

6. **Ejecuta la aplicación:**
   ```bash
   flask run
   ```

## Uso
- Accede a la aplicación a través de tu navegador
- Regístrate o inicia sesión con un usuario existente
- Explora y comparte recetas con otros usuarios
- Gestiona tu perfil y tus recetas

## Funcionalidad de usuarios similares
- El sistema conecta automáticamente a usuarios con gustos similares
- Las relaciones se basan en los ingredientes de las recetas compartidas
- Puedes ver tus conexiones en tu perfil

## Comandos útiles
- `flask update-similar-users`: Actualiza las relaciones entre usuarios
- `flask init-db`: Inicializa la base de datos

## Notas de seguridad
- Las contraseñas se almacenan de forma segura
- Se implementan las mejores prácticas de seguridad web

## Créditos
- Desarrollado por [Xavier Gordillo]
- Basado en Flask, SQLAlchemy y Bootstrap

## Despliegue

La aplicación está diseñada para ser desplegada en cualquier plataforma de hosting que soporte aplicaciones Python/Flask. Algunas opciones populares incluyen:

- Plataformas PaaS (Platform as a Service)
- Servidores VPS
- Servicios de hosting especializados en Python

### Consideraciones para el despliegue

1. **Variables de entorno:**
   - Configura las variables de entorno necesarias para el entorno de producción
   - Asegúrate de tener una base de datos PostgreSQL configurada

2. **Base de datos:**
   - Utiliza una base de datos PostgreSQL en producción
   - Configura las credenciales de forma segura

3. **Servidor web:**
   - Se recomienda usar Gunicorn como servidor WSGI
   - Configura un servidor web como Nginx como proxy inverso

4. **Seguridad:**
   - Implementa HTTPS
   - Configura correctamente los headers de seguridad
   - Mantén las dependencias actualizadas

Para más información sobre el despliegue, consulta la documentación de tu plataforma de hosting preferida.

