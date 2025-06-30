from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from . import main
from .. import db
from ..models import User, Recipe, SimilarUser
from werkzeug.security import generate_password_hash, check_password_hash
# Importar servicios para separar responsabilidades
from ..services import UserService, RecipeService, SimilarityService
# Importar estrategias de matching
from ..strategies import MatchingStrategyFactory
# Importar factories para crear entidades
from ..factories import RecipeFactory, UserFactory

# Registro de usuario
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if UserService.get_user_by_username(username):
            flash('El nombre de usuario ya existe.')
            return redirect(url_for('.register'))
        # Usar Factory para crear usuario
        user = UserFactory.create_user("standard", username=username, password_hash=generate_password_hash(password))
        flash('Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect(url_for('.login'))
    return render_template('register.html')

# Login de usuario
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Usar servicio para obtener usuario
        user = UserService.get_user_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('.index'))
        flash('Usuario o contraseña incorrectos.')
    return render_template('login.html')

# Logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada.')
    return redirect(url_for('.login'))

# Página principal: lista de recetas
@main.route('/')
def index():
    # Usar servicios para obtener datos
    recipes = RecipeService.get_all_recipes()
    users = UserService.get_all_users()
    return render_template('index.html', recipes=recipes, users=users)

# Crear receta
@main.route('/new_recipe', methods=['GET', 'POST'])
@login_required
def new_recipe():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        ingredients = request.form['ingredients']
        steps = request.form['steps']
        category = request.form['category']
        
        # Usar Factory para crear receta
        recipe = RecipeFactory.create_recipe("basic", 
                                           title=title,
                                           description=description,
                                           ingredients=ingredients,
                                           steps=steps,
                                           category=category,
                                           author=current_user)
        db.session.add(recipe)
        db.session.commit()

        # Usar estrategia de matching para encontrar usuarios similares
        # Limpiar relaciones previas del usuario actual
        SimilarityService.clear_user_similarities(current_user.id)
        
        # Obtener todas las recetas de otros usuarios
        all_recipes = RecipeService.get_other_users_recipes(current_user.id)
        new_ingredients = set([i.strip().lower() for i in ingredients.split(',')])
        
        # Usar Factory para crear estrategia de matching
        strategy = MatchingStrategyFactory.create_strategy("ingredient_overlap", min_common_ingredients=2)
        matched_user_ids = strategy.find_similar_users(new_ingredients, all_recipes)
        
        # Crear relaciones bidireccionales usando servicios
        for uid in matched_user_ids:
            SimilarityService.create_similarity_relationship(current_user.id, uid)
        
        db.session.commit()
        flash('Receta publicada exitosamente. Se han actualizado tus usuarios similares.')
        return redirect(url_for('.index'))
    return render_template('new_recipe.html')

# Ver receta
@main.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    # Usar servicio para obtener receta
    recipe = RecipeService.get_recipe_by_id(recipe_id)
    if not recipe:
        from flask import abort
        abort(404)
    return render_template('recipe_detail.html', recipe=recipe)

@main.route('/category/<category>')
def category(category):
    # Usar servicio para obtener recetas por categoría
    recipes = RecipeService.get_recipes_by_category(category)
    return render_template('category.html', recipes=recipes, category=category)

# Perfil de usuario
@main.route('/user/<int:user_id>')
def user_profile(user_id):
    # Usar servicios para obtener datos
    user = UserService.get_user_by_id(user_id)
    if not user:
        from flask import abort
        abort(404)
    
    # Usar servicio para obtener usuarios similares
    similar_users = SimilarityService.get_similar_users(user_id)
    return render_template('user_profile.html', user=user, similar_users=similar_users)

@main.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    # Usar servicio para obtener y eliminar receta
    recipe = RecipeService.get_recipe_by_id(recipe_id)
    if not recipe:
        from flask import abort
        abort(404)
    if recipe.author_id != current_user.id:
        flash('No tienes permiso para eliminar esta receta.')
        return redirect(url_for('.index'))
    RecipeService.delete_recipe(recipe)
    flash('Receta eliminada exitosamente.')
    return redirect(url_for('.index'))

# Editar receta
@main.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    # Usar servicio para obtener receta
    recipe = RecipeService.get_recipe_by_id(recipe_id)
    if not recipe:
        from flask import abort
        abort(404)
    if recipe.author_id != current_user.id:
        flash('No tienes permiso para editar esta receta.')
        return redirect(url_for('.index'))
    if request.method == 'POST':
        # Usar servicio para actualizar receta
        RecipeService.update_recipe(recipe, 
                                  title=request.form['title'],
                                  description=request.form['description'],
                                  ingredients=request.form['ingredients'],
                                  steps=request.form['steps'],
                                  category=request.form['category'])

        # Usar estrategia de matching para encontrar usuarios similares
        SimilarityService.clear_user_similarities(current_user.id)
        all_recipes = RecipeService.get_other_users_recipes(current_user.id)
        new_ingredients = set([i.strip().lower() for i in recipe.ingredients.split(',')])
        
        # Usar Factory para crear estrategia de matching
        strategy = MatchingStrategyFactory.create_strategy("ingredient_overlap", min_common_ingredients=2)
        matched_user_ids = strategy.find_similar_users(new_ingredients, all_recipes)
        
        # Crear relaciones bidireccionales usando servicios
        for uid in matched_user_ids:
            SimilarityService.create_similarity_relationship(current_user.id, uid)
        
        db.session.commit()
        flash('Receta actualizada exitosamente. Se han actualizado tus usuarios similares.')
        return redirect(url_for('.recipe_detail', recipe_id=recipe.id))
    return render_template('edit_recipe.html', recipe=recipe)
