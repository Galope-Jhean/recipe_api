from flask import Blueprint, request, jsonify
from app.models import Recipe
from sqlalchemy import text
from app.extensions import db
import json

suggest_bp = Blueprint("suggest", __name__)

@suggest_bp.route("/", methods=["POST"])
def suggest_recipes():
    try:
        ingredients_list = request.json.get("ingredients", [])
        
        if not ingredients_list:
            return jsonify({"error": "Ingredients list is required"}), 400

        ingredients_list = [ingredient.strip().lower() for ingredient in ingredients_list]

        placeholders = [f":ingredient_{i}" for i in range(len(ingredients_list))]

        bind_params = {f"ingredient_{i}": ingredient for i, ingredient in enumerate(ingredients_list)}

        sql = text(f"""
            SELECT DISTINCT r.id, r.name, r.ingredients
            FROM recipes r
            CROSS APPLY OPENJSON(r.ingredients) 
            WITH (ingredient NVARCHAR(100) '$.ingredient') AS ing
            WHERE ing.ingredient IN ({', '.join(placeholders)})
        """)

        results = db.session.execute(sql, bind_params)
        recipes = results.fetchall()

        if not recipes:
            return jsonify({"message": "No recipes found for the provided ingredients"}), 404

        recipes_data = []
        for recipe in recipes:
            recipe_data = {
                "id": recipe.id,
                "name": recipe.name,
                "ingredients": json.loads(recipe.ingredients)  
            }
            recipes_data.append(recipe_data)

        return jsonify(recipes_data), 200
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
