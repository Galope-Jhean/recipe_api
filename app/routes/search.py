from flask import Blueprint, request, jsonify
from app.models import Recipe
from sqlalchemy import text
from app.extensions import db

search_bp = Blueprint("search", __name__)

@search_bp.route("/", methods=["GET"])
def search_recipes():
    try:
        query = request.args.get("q", "").strip().lower()
        if not query:
            return jsonify({"error": "Search query is required"}), 400

        sql = text("""
            SELECT DISTINCT r.id, r.name, r.ingredients
            FROM recipes r
            CROSS APPLY OPENJSON(r.ingredients) 
            WITH (ingredient NVARCHAR(100) '$.ingredient') AS ing
            WHERE r.name LIKE :query
            OR ing.ingredient LIKE :query
        """)
        
        results = db.session.execute(sql, {'query': f"%{query}%"})
        recipes = results.fetchall()

        if not recipes:
            return jsonify({"message": "No recipes found"}), 404

        recipes_data = [{
            "id": recipe.id,
            "name": recipe.name,
            "ingredients": recipe.ingredients
        } for recipe in recipes]

        return jsonify(recipes_data), 200
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
