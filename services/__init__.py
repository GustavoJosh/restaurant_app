# services/__init__.py
from app import db
from models.stock import Ingredient
from models.menu import Recipe

def update_stock(order_item):
    if order_item.selected_ingredients:  
        for ingredient_id in order_item.selected_ingredients:
            ingredient = Ingredient.query.get(ingredient_id)
            recipe = Recipe.query.filter_by(menu_item_id=order_item.menu_item_id, ingredient_id=ingredient_id).first()

            if recipe and ingredient:
                ingredient.total_quantity -= recipe.quantity_used * order_item.quantity
                db.session.commit()
    else:
        recipes = Recipe.query.filter_by(menu_item_id=order_item.menu_item_id).all()
        for recipe in recipes:
            ingredient = Ingredient.query.get(recipe.ingredient_id)
            if ingredient:
                ingredient.total_quantity -= recipe.quantity_used * order_item.quantity
                db.session.commit()
                
def update_menu_item_stock(ingredient_id):
    try:
        ingredient = db.session.get(Ingredient, ingredient_id)
        if not ingredient:
            return
            
        recipes = Recipe.query.filter_by(ingredient_id=ingredient_id).all()
        for recipe in recipes:
            menu_item = recipe.menu_item
            quantity_used = recipe.quantity_used
            if quantity_used > 0:
                max_items = int(ingredient.total_quantity / quantity_used)
                menu_item.stock = max_items
                db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error updating menu item stock: {str(e)}")
