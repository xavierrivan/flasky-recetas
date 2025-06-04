from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from . import main
from .. import db
from ..models import User, Recipe, SimilarUser
from werkzeug.security import generate_password_hash, check_password_hash

# Registro de usuario
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.')
            return redirect(url_for('.register'))
        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect(url_for('.login'))
    return render_template('register.html')

# Login de usuario
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
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
    recipes = Recipe.query.order_by(Recipe.timestamp.desc()).all()
    users = User.query.order_by(User.username.asc()).all()
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
        recipe = Recipe(
            title=title,
            description=description,
            ingredients=ingredients,
            steps=steps,
            category=category,
            author=current_user
        )
        db.session.add(recipe)
        db.session.commit()

        # --- AUTOMATCH DE USUARIOS SIMILARES POR INGREDIENTES ---
        # Limpiar relaciones previas del usuario actual
        SimilarUser.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        # Obtener todas las recetas de otros usuarios
        all_recipes = Recipe.query.filter(Recipe.author_id != current_user.id).all()
        new_ingredients = set([i.strip().lower() for i in ingredients.split(',')])
        matched_user_ids = set()
        for r in all_recipes:
            other_ingredients = set([i.strip().lower() for i in r.ingredients.split(',')])
            # Si hay al menos 2 ingredientes en común, se considera similar
            if len(new_ingredients & other_ingredients) >= 2:
                matched_user_ids.add(r.author_id)
        # Crear relaciones bidireccionales
        for uid in matched_user_ids:
            if not SimilarUser.query.filter_by(user_id=current_user.id, similar_user_id=uid).first():
                db.session.add(SimilarUser(user_id=current_user.id, similar_user_id=uid))
            if not SimilarUser.query.filter_by(user_id=uid, similar_user_id=current_user.id).first():
                db.session.add(SimilarUser(user_id=uid, similar_user_id=current_user.id))
        db.session.commit()
        flash('Receta publicada exitosamente. Se han actualizado tus usuarios similares.')
        return redirect(url_for('.index'))
    return render_template('new_recipe.html')

# Ver receta
@main.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)

@main.route('/category/<category>')
def category(category):
    recipes = Recipe.query.filter_by(category=category).order_by(Recipe.timestamp.desc()).all()
    return render_template('category.html', recipes=recipes, category=category)

# Perfil de usuario
@main.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    # Obtener usuarios similares en ambos sentidos
    similar_ids_1 = [rel.similar_user_id for rel in SimilarUser.query.filter_by(user_id=user_id).all()]
    similar_ids_2 = [rel.user_id for rel in SimilarUser.query.filter_by(similar_user_id=user_id).all()]
    all_similar_ids = set(similar_ids_1 + similar_ids_2)
    all_similar_ids.discard(user_id)  # Evitar que el usuario se vea a sí mismo
    similar_users = User.query.filter(User.id.in_(all_similar_ids)).all() if all_similar_ids else []
    return render_template('user_profile.html', user=user, similar_users=similar_users)

@main.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author_id != current_user.id:
        flash('No tienes permiso para eliminar esta receta.')
        return redirect(url_for('.index'))
    db.session.delete(recipe)
    db.session.commit()
    flash('Receta eliminada exitosamente.')
    return redirect(url_for('.index'))

# Editar receta
@main.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author_id != current_user.id:
        flash('No tienes permiso para editar esta receta.')
        return redirect(url_for('.index'))
    if request.method == 'POST':
        recipe.title = request.form['title']
        recipe.description = request.form['description']
        recipe.ingredients = request.form['ingredients']
        recipe.steps = request.form['steps']
        recipe.category = request.form['category']
        db.session.commit()

        # --- AUTOMATCH DE USUARIOS SIMILARES POR INGREDIENTES (al editar) ---
        SimilarUser.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        all_recipes = Recipe.query.filter(Recipe.author_id != current_user.id).all()
        new_ingredients = set([i.strip().lower() for i in recipe.ingredients.split(',')])
        matched_user_ids = set()
        for r in all_recipes:
            other_ingredients = set([i.strip().lower() for i in r.ingredients.split(',')])
            if len(new_ingredients & other_ingredients) >= 2:
                matched_user_ids.add(r.author_id)
        for uid in matched_user_ids:
            if not SimilarUser.query.filter_by(user_id=current_user.id, similar_user_id=uid).first():
                db.session.add(SimilarUser(user_id=current_user.id, similar_user_id=uid))
            if not SimilarUser.query.filter_by(user_id=uid, similar_user_id=current_user.id).first():
                db.session.add(SimilarUser(user_id=uid, similar_user_id=current_user.id))
        db.session.commit()
        flash('Receta actualizada exitosamente. Se han actualizado tus usuarios similares.')
        return redirect(url_for('.recipe_detail', recipe_id=recipe.id))
    return render_template('edit_recipe.html', recipe=recipe)
