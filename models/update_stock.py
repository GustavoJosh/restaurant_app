from models.stock import Ingredient
from models.menu import Recipe
from database import db

def update_stock(order_item):
    if order_item.selected_ingredients:
        #  Handle custom gorditas (user-selected ingredients)
        for ingredient_id in order_item.selected_ingredients:
            ingredient = Ingredient.query.get(ingredient_id)
            recipe = Recipe.query.filter_by(menu_item_id=order_item.menu_item_id, ingredient_id=ingredient_id).first()

            if recipe and ingredient:
                ingredient.total_quantity -= recipe.quantity_used * order_item.quantity
                db.session.commit()
    else:
        #  Handle standard menu items with predefined recipes
        recipes = Recipe.query.filter_by(menu_item_id=order_item.menu_item_id).all()
        
        for recipe in recipes:
            ingredient = Ingredient.query.get(recipe.ingredient_id)
            if ingredient:
                ingredient.total_quantity -= recipe.quantity_used * order_item.quantity
                db.session.commit()
