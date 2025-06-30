# Estrategias de matching de usuarios
# Este archivo implementa diferentes algoritmos para encontrar usuarios similares
# Permite agregar nuevos algoritmos sin modificar el código existente

from abc import ABC, abstractmethod
from typing import List, Set
from .models import Recipe, User

class MatchingStrategy(ABC):
    """Interfaz abstracta para estrategias de matching de usuarios"""
    
    @abstractmethod
    def find_similar_users(self, user_ingredients: Set[str], all_recipes: List[Recipe]) -> Set[int]:
        """Encuentra usuarios similares basado en ingredientes"""
        pass

class IngredientOverlapStrategy(MatchingStrategy):
    """Estrategia: Usuarios similares basados en ingredientes en común"""
    
    def __init__(self, min_common_ingredients: int = 2):
        self.min_common_ingredients = min_common_ingredients
    
    def find_similar_users(self, user_ingredients: Set[str], all_recipes: List[Recipe]) -> Set[int]:
        """Encuentra usuarios con al menos N ingredientes en común"""
        matched_user_ids = set()
        
        for recipe in all_recipes:
            recipe_ingredients = set([i.strip().lower() for i in recipe.ingredients.split(',')])
            common_ingredients = user_ingredients & recipe_ingredients
            
            if len(common_ingredients) >= self.min_common_ingredients:
                matched_user_ids.add(recipe.author_id)
        
        return matched_user_ids

class CategoryMatchingStrategy(MatchingStrategy):
    """Estrategia: Usuarios similares basados en categorías de recetas"""
    
    def find_similar_users(self, user_ingredients: Set[str], all_recipes: List[Recipe]) -> Set[int]:
        """Encuentra usuarios que comparten categorías de recetas"""
        matched_user_ids = set()
        
        # Obtener categorías de las recetas del usuario actual
        user_categories = set()
        for recipe in all_recipes:
            if recipe.author_id in [r.author_id for r in all_recipes if any(ing in r.ingredients.lower() for ing in user_ingredients)]:
                user_categories.add(recipe.category)
        
        # Buscar usuarios con categorías similares
        for recipe in all_recipes:
            if recipe.category in user_categories:
                matched_user_ids.add(recipe.author_id)
        
        return matched_user_ids

class HybridMatchingStrategy(MatchingStrategy):
    """Estrategia híbrida: Combina ingredientes y categorías"""
    
    def __init__(self, ingredient_weight: float = 0.7, category_weight: float = 0.3):
        self.ingredient_strategy = IngredientOverlapStrategy(min_common_ingredients=1)
        self.category_strategy = CategoryMatchingStrategy()
        self.ingredient_weight = ingredient_weight
        self.category_weight = category_weight
    
    def find_similar_users(self, user_ingredients: Set[str], all_recipes: List[Recipe]) -> Set[int]:
        """Combina resultados de múltiples estrategias"""
        ingredient_matches = self.ingredient_strategy.find_similar_users(user_ingredients, all_recipes)
        category_matches = self.category_strategy.find_similar_users(user_ingredients, all_recipes)
        
        # Combinar resultados (usuarios que aparecen en ambas estrategias tienen mayor peso)
        hybrid_matches = ingredient_matches | category_matches
        return hybrid_matches

class MatchingStrategyFactory:
    """Factory para crear estrategias de matching"""
    
    @staticmethod
    def create_strategy(strategy_type: str, **kwargs) -> MatchingStrategy:
        """Crea una estrategia de matching basada en el tipo especificado"""
        if strategy_type == "ingredient_overlap":
            min_ingredients = kwargs.get('min_common_ingredients', 2)
            return IngredientOverlapStrategy(min_common_ingredients=min_ingredients)
        
        elif strategy_type == "category_matching":
            return CategoryMatchingStrategy()
        
        elif strategy_type == "hybrid":
            ingredient_weight = kwargs.get('ingredient_weight', 0.7)
            category_weight = kwargs.get('category_weight', 0.3)
            return HybridMatchingStrategy(ingredient_weight=ingredient_weight, category_weight=category_weight)
        
        else:
            # Estrategia por defecto
            return IngredientOverlapStrategy() 