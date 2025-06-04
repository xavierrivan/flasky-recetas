import os
from app import create_app, db
from app.models import User, Recipe, SimilarUser
from flask_migrate import Migrate

app = create_app('development')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Recipe=Recipe)


@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized.')

# Consider adding a command to create a test user if needed
# @app.cli.command()
# @click.argument('username')
# @click.argument('password')
# def create_user(username, password):
#     user = User(username=username, password=password)
#     db.session.add(user)
#     db.session.commit()
#     print(f'User {username} created.')

@app.cli.command()
def update_similar_users():
    """Normaliza ingredientes y actualiza relaciones de usuarios similares para todos los usuarios."""
    print('Normalizando ingredientes...')
    # Normalizar ingredientes de todas las recetas
    for recipe in Recipe.query.all():
        ingredientes = [i.strip().lower() for i in recipe.ingredients.split(',') if i.strip()]
        ingredientes = sorted(set(ingredientes))
        recipe.ingredients = ', '.join(ingredientes)
    db.session.commit()
    print('Ingredientes normalizados.')

    print('Eliminando relaciones previas...')
    SimilarUser.query.delete()
    db.session.commit()
    print('Relaciones previas eliminadas.')

    print('Calculando nuevas relaciones de gustos similares...')
    users = User.query.all()
    for user in users:
        user_recipes = Recipe.query.filter_by(author_id=user.id).all()
        user_ings = set()
        for r in user_recipes:
            user_ings.update([i.strip().lower() for i in r.ingredients.split(',') if i.strip()])
        if not user_ings:
            continue
        # Buscar otros usuarios con al menos 2 ingredientes en común
        for other in users:
            if other.id == user.id:
                continue
            other_recipes = Recipe.query.filter_by(author_id=other.id).all()
            other_ings = set()
            for r in other_recipes:
                other_ings.update([i.strip().lower() for i in r.ingredients.split(',') if i.strip()])
            if len(user_ings & other_ings) >= 2:
                if not SimilarUser.query.filter_by(user_id=user.id, similar_user_id=other.id).first():
                    db.session.add(SimilarUser(user_id=user.id, similar_user_id=other.id))
    db.session.commit()
    print('Relaciones de gustos similares actualizadas.')

if __name__ == '__main__':
    app.run(debug=True)
