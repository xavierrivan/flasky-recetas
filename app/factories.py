# Factories para crear entidades
# Este archivo implementa factories para crear diferentes tipos de recetas y usuarios
# Permite crear objetos de forma flexible sin especificar sus clases exactas

from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import Recipe, User
from . import db

class RecipeFactory:
    """Factory para crear diferentes tipos de recetas"""
    
    @staticmethod
    def create_recipe(recipe_type: str, **kwargs) -> Recipe:
        """Crea una receta basada en el tipo especificado"""
        
        if recipe_type == "basic":
            return RecipeFactory._create_basic_recipe(**kwargs)
        
        elif recipe_type == "detailed":
            return RecipeFactory._create_detailed_recipe(**kwargs)
        
        elif recipe_type == "quick":
            return RecipeFactory._create_quick_recipe(**kwargs)
        
        else:
            # Tipo por defecto
            return RecipeFactory._create_basic_recipe(**kwargs)
    
    @staticmethod
    def _create_basic_recipe(**kwargs) -> Recipe:
        """Crea una receta básica con campos mínimos"""
        return Recipe(
            title=kwargs.get('title', 'Receta sin título'),
            description=kwargs.get('description', ''),
            ingredients=kwargs.get('ingredients', ''),
            steps=kwargs.get('steps', ''),
            category=kwargs.get('category', 'General'),
            author=kwargs.get('author')
        )
    
    @staticmethod
    def _create_detailed_recipe(**kwargs) -> Recipe:
        """Crea una receta detallada con validaciones adicionales"""
        # Validar que todos los campos requeridos estén presentes
        required_fields = ['title', 'description', 'ingredients', 'steps', 'author']
        for field in required_fields:
            if field not in kwargs or not kwargs[field]:
                raise ValueError(f"Campo requerido '{field}' no proporcionado para receta detallada")
        
        return Recipe(
            title=kwargs['title'],
            description=kwargs['description'],
            ingredients=kwargs['ingredients'],
            steps=kwargs['steps'],
            category=kwargs.get('category', 'General'),
            author=kwargs['author']
        )
    
    @staticmethod
    def _create_quick_recipe(**kwargs) -> Recipe:
        """Crea una receta rápida con formato simplificado"""
        # Para recetas rápidas, combinar descripción y pasos
        combined_steps = f"{kwargs.get('description', '')}\n\nPasos:\n{kwargs.get('steps', '')}"
        
        return Recipe(
            title=kwargs.get('title', 'Receta Rápida'),
            description='Receta de preparación rápida',
            ingredients=kwargs.get('ingredients', ''),
            steps=combined_steps,
            category=kwargs.get('category', 'Rápida'),
            author=kwargs.get('author')
        )

class UserFactory:
    """Factory para crear diferentes tipos de usuarios"""
    
    @staticmethod
    def create_user(user_type: str, **kwargs) -> User:
        """Crea un usuario basado en el tipo especificado"""
        
        if user_type == "standard":
            return UserFactory._create_standard_user(**kwargs)
        
        elif user_type == "admin":
            return UserFactory._create_admin_user(**kwargs)
        
        elif user_type == "premium":
            return UserFactory._create_premium_user(**kwargs)
        
        else:
            # Tipo por defecto
            return UserFactory._create_standard_user(**kwargs)
    
    @staticmethod
    def _create_standard_user(**kwargs) -> User:
        """Crea un usuario estándar"""
        user = User(
            username=kwargs.get('username', 'usuario'),
            password_hash=kwargs.get('password_hash', '')
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def _create_admin_user(**kwargs) -> User:
        """Crea un usuario administrador (para futuras funcionalidades)"""
        user = User(
            username=kwargs.get('username', 'admin'),
            password_hash=kwargs.get('password_hash', '')
        )
        # Aquí se podrían agregar campos adicionales para administradores
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def _create_premium_user(**kwargs) -> User:
        """Crea un usuario premium (para futuras funcionalidades)"""
        user = User(
            username=kwargs.get('username', 'premium_user'),
            password_hash=kwargs.get('password_hash', '')
        )
        # Aquí se podrían agregar campos adicionales para usuarios premium
        db.session.add(user)
        db.session.commit()
        return user

class EntityFactory:
    """Factory principal que coordina la creación de diferentes entidades"""
    
    @staticmethod
    def create_entity(entity_type: str, **kwargs) -> Any:
        """Crea cualquier tipo de entidad usando el factory apropiado"""
        
        if entity_type.startswith('recipe'):
            recipe_type = entity_type.replace('recipe_', '')
            return RecipeFactory.create_recipe(recipe_type, **kwargs)
        
        elif entity_type.startswith('user'):
            user_type = entity_type.replace('user_', '')
            return UserFactory.create_user(user_type, **kwargs)
        
        else:
            raise ValueError(f"Tipo de entidad no soportado: {entity_type}") 