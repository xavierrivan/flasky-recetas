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






## Mejoras Implementadas - Arquitectura y Organización

### Mejoras de Arquitectura:

#### 1. **Separación de Responsabilidades**
- **Archivo**: `app/services.py`
- **Cambio**: Se separó la lógica de negocio de las vistas en servicios especializados
- **Beneficio**: Cada servicio tiene una única responsabilidad (UserService, RecipeService, SimilarityService)
- **Marcas en código**: Comentarios explicativos en cada servicio

#### 2. **Sistema Extensible**
- **Archivo**: `app/strategies.py`
- **Cambio**: Sistema de matching extensible que permite agregar nuevas estrategias sin modificar código existente
- **Beneficio**: Se pueden agregar nuevos algoritmos de matching sin cambiar la lógica principal
- **Marcas en código**: Comentarios explicativos en cada estrategia

### Patrones de Organización Aplicados:

#### 1. **Estrategias de Matching**
- **Archivo**: `app/strategies.py`
- **Cambio**: Implementación de diferentes estrategias de matching de usuarios similares
- **Estrategias disponibles**:
  - `IngredientOverlapStrategy`: Matching por ingredientes en común
  - `CategoryMatchingStrategy`: Matching por categorías de recetas
  - `HybridMatchingStrategy`: Combinación de ambas estrategias
- **Beneficio**: Fácil intercambio de algoritmos de matching
- **Marcas en código**: Comentarios explicativos en cada estrategia

#### 2. **Factories para Creación de Entidades**
- **Archivo**: `app/factories.py`
- **Cambio**: Factories para crear diferentes tipos de recetas y usuarios
- **Tipos disponibles**:
  - Recetas: `basic`, `detailed`, `quick`
  - Usuarios: `standard`, `admin`, `premium`
- **Beneficio**: Creación flexible de objetos sin especificar clases exactas
- **Marcas en código**: Comentarios explicativos en cada factory

### Archivos Modificados:
- `app/services.py` - Nuevo archivo con servicios especializados
- `app/strategies.py` - Nuevo archivo con estrategias de matching
- `app/factories.py` - Nuevo archivo con factories
- `app/main/views.py` - Actualizado para usar los nuevos servicios y patrones

### Beneficios de las Mejoras:
1. **Mantenibilidad**: Código más organizado y fácil de mantener
2. **Extensibilidad**: Fácil agregar nuevas funcionalidades
3. **Testabilidad**: Servicios y estrategias pueden ser probados independientemente
4. **Reutilización**: Servicios pueden ser reutilizados en diferentes partes de la aplicación
5. **Flexibilidad**: Diferentes estrategias de matching pueden ser intercambiadas fácilmente

