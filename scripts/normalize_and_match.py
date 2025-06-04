from app import create_app, db
from app.models import User, Recipe, SimilarUser

app = create_app('development')

with app.app_context():
    # Normalizar ingredientes: quitar espacios, minúsculas, ordenar y guardar en la receta
    for recipe in Recipe.query.all():
        ingredients = [i.strip().lower() for i in recipe.ingredients.replace('\n', ',').replace(';', ',').split(',') if i.strip()]
        ingredients = sorted(set(ingredients))
        recipe.ingredients = ', '.join(ingredients)
    db.session.commit()

    # Limpiar todas las relaciones previas
    SimilarUser.query.delete()
    db.session.commit()

    # Para cada usuario, buscar usuarios similares por ingredientes
    for user in User.query.all():
        user_recipes = Recipe.query.filter_by(author_id=user.id).all()
        user_ingredients = set()
        for r in user_recipes:
            user_ingredients.update([i.strip().lower() for i in r.ingredients.split(',') if i.strip()])
        if not user_ingredients:
            continue
        matched_user_ids = set()
        for other in User.query.filter(User.id != user.id).all():
            other_recipes = Recipe.query.filter_by(author_id=other.id).all()
            other_ingredients = set()
            for r in other_recipes:
                other_ingredients.update([i.strip().lower() for i in r.ingredients.split(',') if i.strip()])
            if len(user_ingredients & other_ingredients) >= 2:
                matched_user_ids.add(other.id)
        for uid in matched_user_ids:
            db.session.add(SimilarUser(user_id=user.id, similar_user_id=uid))
    db.session.commit()
    print('Ingredientes normalizados y relaciones de usuarios similares actualizadas.') 