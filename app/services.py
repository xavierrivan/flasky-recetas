# Servicios de la aplicación
# Este archivo contiene servicios especializados para separar la lógica de negocio de las vistas

from typing import List, Set
from .models import User, Recipe, SimilarUser
from . import db

class UserService:
    """Servicio responsable únicamente de operaciones relacionadas con usuarios"""
    
    @staticmethod
    def create_user(username: str, password_hash: str) -> User:
        """Crea un nuevo usuario"""
        user = User(username=username, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_username(username: str) -> User:
        """Obtiene un usuario por su nombre de usuario"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """Obtiene un usuario por su ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_all_users() -> List[User]:
        """Obtiene todos los usuarios ordenados por nombre"""
        return User.query.order_by(User.username.asc()).all()

class RecipeService:
    """Servicio responsable únicamente de operaciones relacionadas con recetas"""
    
    @staticmethod
    def create_recipe(title: str, description: str, ingredients: str, 
                     steps: str, category: str, author: User) -> Recipe:
        """Crea una nueva receta"""
        recipe = Recipe(
            title=title,
            description=description,
            ingredients=ingredients,
            steps=steps,
            category=category,
            author=author
        )
        db.session.add(recipe)
        db.session.commit()
        return recipe
    
    @staticmethod
    def get_recipe_by_id(recipe_id: int) -> Recipe:
        """Obtiene una receta por su ID"""
        return Recipe.query.get(recipe_id)
    
    @staticmethod
    def get_all_recipes() -> List[Recipe]:
        """Obtiene todas las recetas ordenadas por fecha"""
        return Recipe.query.order_by(Recipe.timestamp.desc()).all()
    
    @staticmethod
    def get_recipes_by_category(category: str) -> List[Recipe]:
        """Obtiene recetas por categoría"""
        return Recipe.query.filter_by(category=category).order_by(Recipe.timestamp.desc()).all()
    
    @staticmethod
    def update_recipe(recipe: Recipe, title: str, description: str, 
                     ingredients: str, steps: str, category: str) -> Recipe:
        """Actualiza una receta existente"""
        recipe.title = title
        recipe.description = description
        recipe.ingredients = ingredients
        recipe.steps = steps
        recipe.category = category
        db.session.commit()
        return recipe
    
    @staticmethod
    def delete_recipe(recipe: Recipe) -> None:
        """Elimina una receta"""
        db.session.delete(recipe)
        db.session.commit()
    
    @staticmethod
    def get_other_users_recipes(user_id: int) -> List[Recipe]:
        """Obtiene recetas de otros usuarios (excluyendo al usuario especificado)"""
        return Recipe.query.filter(Recipe.author_id != user_id).all()

class SimilarityService:
    """Servicio responsable únicamente de operaciones relacionadas con usuarios similares"""
    
    @staticmethod
    def clear_user_similarities(user_id: int) -> None:
        """Limpia las relaciones de similitud de un usuario"""
        SimilarUser.query.filter_by(user_id=user_id).delete()
        db.session.commit()
    
    @staticmethod
    def create_similarity_relationship(user_id: int, similar_user_id: int) -> None:
        """Crea una relación de similitud bidireccional entre usuarios"""
        # Verificar que no exista ya la relación
        if not SimilarUser.query.filter_by(user_id=user_id, similar_user_id=similar_user_id).first():
            db.session.add(SimilarUser(user_id=user_id, similar_user_id=similar_user_id))
        
        if not SimilarUser.query.filter_by(user_id=similar_user_id, similar_user_id=user_id).first():
            db.session.add(SimilarUser(user_id=similar_user_id, similar_user_id=user_id))
    
    @staticmethod
    def get_similar_users(user_id: int) -> List[User]:
        """Obtiene usuarios similares para un usuario dado"""
        # Obtener usuarios similares en ambos sentidos
        similar_ids_1 = [rel.similar_user_id for rel in SimilarUser.query.filter_by(user_id=user_id).all()]
        similar_ids_2 = [rel.user_id for rel in SimilarUser.query.filter_by(similar_user_id=user_id).all()]
        all_similar_ids = set(similar_ids_1 + similar_ids_2)
        all_similar_ids.discard(user_id)  # Evitar que el usuario se vea a sí mismo
        
        return User.query.filter(User.id.in_(all_similar_ids)).all() if all_similar_ids else [] 