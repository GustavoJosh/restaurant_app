# services/__init__.py
from database import db
from models.stock import Ingredient
from models.menu import Recipe
from models.modifications import OrderItemModification

def update_stock(order_item):
    """Update stock based on an order item and its modifications"""
    
    # Get all modifications for this order item
    mods = OrderItemModification.query.filter_by(order_item_id=order_item.id).all()
    
    # Track modifications by type
    removal_ids = []  # Ingredients to skip
    extra_quantities = {}  # Additional quantities for ingredients
    substitutions = {}  # Map of original → replacement
    
    # Process all modifications
    for mod in mods:
        if mod.modification_type == "remove":
            # Skip this ingredient when processing
            removal_ids.append(mod.ingredient_id)
        
        elif mod.modification_type == "add":
            # Add extra quantity to this ingredient
            if mod.ingredient_id in extra_quantities:
                extra_quantities[mod.ingredient_id] += mod.quantity
            else:
                extra_quantities[mod.ingredient_id] = mod.quantity
                
        elif mod.modification_type == "substitute":
            # Remove original and add replacement
            removal_ids.append(mod.ingredient_id)
            substitutions[mod.ingredient_id] = {
                "replacement_id": mod.replacement_ingredient_id,
                "quantity": mod.quantity
            }
    
    # Process the standard recipe ingredients
    recipes = Recipe.query.filter_by(menu_item_id=order_item.menu_item_id).all()
    
    for recipe in recipes:
        ingredient_id = recipe.ingredient_id
        
        # Skip ingredients marked for removal
        if ingredient_id in removal_ids:
            # If it's a substitution, process the replacement
            if ingredient_id in substitutions:
                sub = substitutions[ingredient_id]
                replacement_id = sub["replacement_id"]
                replacement_quantity = sub["quantity"] * recipe.quantity_used  # Scale by recipe amount
                
                replacement_ingredient = Ingredient.query.get(replacement_id)
                if replacement_ingredient:
                    replacement_ingredient.total_quantity -= replacement_quantity * order_item.quantity
            
            # Skip the original ingredient
            continue
            
        # Process standard ingredient (not removed or substituted)
        ingredient = Ingredient.query.get(ingredient_id)
        if ingredient:
            # Start with recipe quantity
            use_quantity = recipe.quantity_used
            
            # Add any extras from modifications
            if ingredient_id in extra_quantities:
                use_quantity += extra_quantities[ingredient_id]
                # Remove from extras to avoid double-counting
                del extra_quantities[ingredient_id]
                
            # Update ingredient stock
            ingredient.total_quantity -= use_quantity * order_item.quantity
    
    # Process any remaining extra quantities (ingredients not in the original recipe)
    for ingredient_id, quantity in extra_quantities.items():
        ingredient = Ingredient.query.get(ingredient_id)
        if ingredient:
            ingredient.total_quantity -= quantity * order_item.quantity
    
    # Save all changes
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

def check_stock_for_item(menu_item_id, quantity, modifications=None):
    """Check if there's enough stock for an item with modifications"""
    
    if not modifications:
        modifications = []
    
    insufficient_stock = []
    
    # Track ingredient changes from modifications
    removal_ids = []
    extra_quantities = {}
    substitutions = {}
    
    # Process all modifications
    for mod in modifications:
        mod_type = mod.get("type")
        ingredient_id = mod.get("ingredient_id")
        
        if mod_type == "remove":
            removal_ids.append(ingredient_id)
        
        elif mod_type == "add":
            mod_quantity = mod.get("quantity", 1.0)
            if ingredient_id in extra_quantities:
                extra_quantities[ingredient_id] += mod_quantity
            else:
                extra_quantities[ingredient_id] = mod_quantity
                
        elif mod_type == "substitute":
            removal_ids.append(ingredient_id)
            substitutions[ingredient_id] = {
                "replacement_id": mod.get("replacement_id"),
                "quantity": mod.get("quantity", 1.0)
            }
    
    # Check stock for standard recipe ingredients
    recipes = Recipe.query.filter_by(menu_item_id=menu_item_id).all()
    
    for recipe in recipes:
        ingredient_id = recipe.ingredient_id
        
        # Skip ingredients marked for removal
        if ingredient_id in removal_ids:
            # But check replacement if this is a substitution
            if ingredient_id in substitutions:
                sub = substitutions[ingredient_id]
                replacement_id = sub["replacement_id"]
                replacement_quantity = sub["quantity"] * recipe.quantity_used * quantity
                
                replacement_ingredient = Ingredient.query.get(replacement_id)
                if replacement_ingredient and replacement_ingredient.total_quantity < replacement_quantity:
                    insufficient_stock.append({
                        "ingredient": replacement_ingredient.name,
                        "available": replacement_ingredient.total_quantity,
                        "required": replacement_quantity
                    })
            
            # Skip checking the original ingredient
            continue
            
        # Check standard ingredient (not removed or substituted)
        ingredient = Ingredient.query.get(ingredient_id)
        if ingredient:
            # Start with recipe quantity
            use_quantity = recipe.quantity_used
            
            # Add any extras from modifications
            if ingredient_id in extra_quantities:
                use_quantity += extra_quantities[ingredient_id]
                # Remove from extras to avoid double-counting
                del extra_quantities[ingredient_id]
            
            # Check if we have enough
            if ingredient.total_quantity < (use_quantity * quantity):
                insufficient_stock.append({
                    "ingredient": ingredient.name,
                    "available": ingredient.total_quantity,
                    "required": use_quantity * quantity
                })
    
    # Check stock for extra ingredients not in original recipe
    for ingredient_id, mod_quantity in extra_quantities.items():
        ingredient = Ingredient.query.get(ingredient_id)
        if ingredient:
            required_quantity = mod_quantity * quantity
            if ingredient.total_quantity < required_quantity:
                insufficient_stock.append({
                    "ingredient": ingredient.name,
                    "available": ingredient.total_quantity,
                    "required": required_quantity
                })
    
    # Return the stock check results
    return {
        "success": len(insufficient_stock) == 0,
        "details": insufficient_stock
    }        

def update_stock_with_modifications(order_item):
    """Update stock taking modifications into account"""
    from models.modifications import OrderItemModification
    from models.menu import Recipe
    from models.stock import Ingredient
    
    # Get all modifications for this order item
    mods = OrderItemModification.query.filter_by(order_item_id=order_item.id).all()
    
    # Create a map of ingredient modifications
    ingredient_adjustments = {}
    removal_ids = []
    substitution_map = {}  # Original -> replacement mapping
    
    for mod in mods:
        if mod.modification_type == "remove":
            # Track which ingredients to skip
            removal_ids.append(mod.ingredient_id)
        elif mod.modification_type == "add":
            # Track extra ingredients to add
            if mod.ingredient_id in ingredient_adjustments:
                ingredient_adjustments[mod.ingredient_id] += mod.quantity
            else:
                ingredient_adjustments[mod.ingredient_id] = mod.quantity
        elif mod.modification_type == "substitute":
            # Track ingredient substitutions
            removal_ids.append(mod.ingredient_id)
            substitution_map[mod.ingredient_id] = {
                "replacement_id": mod.replacement_ingredient_id,
                "quantity": mod.quantity
            }
    
    # Process regular recipe ingredients
    recipes = Recipe.query.filter_by(menu_item_id=order_item.menu_item_id).all()
    
    for recipe in recipes:
        ingredient_id = recipe.ingredient_id
        
        # Skip if this ingredient is removed or substituted
        if ingredient_id in removal_ids:
            # If it's a substitution, add the replacement ingredient
            if ingredient_id in substitution_map:
                replacement = substitution_map[ingredient_id]
                replacement_id = replacement["replacement_id"]
                replacement_quantity = replacement["quantity"] * recipe.quantity_used
                
                # Decrease stock for replacement ingredient
                replacement_ingredient = Ingredient.query.get(replacement_id)
                if replacement_ingredient:
                    replacement_ingredient.total_quantity -= replacement_quantity * order_item.quantity
            
            # Skip the original ingredient
            continue
        
        # Process normal ingredient
        ingredient = Ingredient.query.get(ingredient_id)
        if ingredient:
            # Calculate how much to use based on recipe
            use_quantity = recipe.quantity_used
            
            # Add any extra quantities from "add" modifications
            if ingredient_id in ingredient_adjustments:
                use_quantity += ingredient_adjustments[ingredient_id]
                # Remove from adjustments to avoid double counting
                del ingredient_adjustments[ingredient_id]
            
            # Decrease the stock
            ingredient.total_quantity -= use_quantity * order_item.quantity
    
    # Process any remaining "add" modifications (extras not in original recipe)
    for ingredient_id, extra_quantity in ingredient_adjustments.items():
        ingredient = Ingredient.query.get(ingredient_id)
        if ingredient:
            ingredient.total_quantity -= extra_quantity * order_item.quantity
    
    # Commit all changes
    db.session.commit()

