from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Comment, Rating, Recipe, User
from app.extensions import db


recipes_bp = Blueprint("recipes", __name__)


@recipes_bp.route("/", methods=["GET"])
def get_recipes():
    try:
        recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
        return jsonify([recipe.to_dict() for recipe in recipes]), 200
    except Exception:
        return (jsonify({"error": "An error occurred while retrieving recipes."}), 500)


@recipes_bp.route("/<int:id>", methods=["GET"])
def get_recipe(id):
    try:
        recipe = Recipe.query.get(id)

        if recipe is None:
            return jsonify({"error": "Recipe not found"}), 404

        return jsonify(recipe.to_dict())

    except Exception:
        return (
            jsonify({"error": "An error occured while retrieving the recipe."}),
            500,
        )


@recipes_bp.route("/<int:id>/comments", methods=["GET"])
def get_comments(id):
    try:
        recipe = Recipe.query.get(id)

        if recipe is None:
            return jsonify({"error": "Recipe not found"}), 404

        comments = Comment.query.filter_by(recipe_id=id)
        return jsonify([comment.to_dict() for comment in comments]), 200
    except Exception:
        return jsonify({"error": "An error occured while retrieving comments"}), 500


@recipes_bp.route("/", methods=["POST"])
@jwt_required()
def create_recipe():
    try:
        data = request.get_json()

        if (
            not data.get("name")
            or not data.get("ingredients")
            or not data.get("steps")
            or not data.get("prep_time")
        ):
            return jsonify({"error": "Missing required fields"}), 400

        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        new_recipe = Recipe(
            name=data["name"],
            ingredients=data["ingredients"],
            steps=data["steps"],
            prep_time=data["prep_time"],
            user=user,
        )

        db.session.add(new_recipe)
        db.session.commit()

        return jsonify(new_recipe.to_dict()), 201

    except Exception:
        return (
            jsonify(
                {
                    "error": "an error occured while creating the recipe",
                }
            ),
            500,
        )


@recipes_bp.route("/<int:id>/ratings", methods=["POST"])
@jwt_required()
def rate_recipe(id):
    try:
        recipe = Recipe.query.get(id)

        if recipe is None:
            return jsonify({"error": "Recipe not found"}), 404

        data = request.get_json()
        rating = data.get("rating")

        if not rating:
            return jsonify({"error": "Missing required fields"}), 400

        if int(rating) < 0 or int(rating) > 5:
            return jsonify({"error": "Rate value invalid"}), 400

        user_id = get_jwt_identity()

        rating = Rating(
            recipe_id=id,
            user_id=int(user_id),
            rating=data["rating"],
        )

        db.session.add(rating)
        db.session.commit()

        return jsonify({"message": "Rating successfully submitted"}), 201

    except Exception:
        return jsonify({"error": "An error occured while rating the recipe"}), 500


@recipes_bp.route("/<int:id>/comments", methods=["POST"])
@jwt_required()
def comment_recipe(id):
    try:
        data = request.get_json()
        comment = data.get("comment", "").strip()

        if not comment:
            return jsonify({"error": "Missing required fields"}), 400

        user_id = get_jwt_identity()

        comment = Comment(
            recipe_id=id,
            user_id=int(user_id),
            comment=data["comment"],
        )

        db.session.add(comment)
        db.session.commit()

        return jsonify({"message": "Comment submitted successfully"}), 201
    except Exception:
        return (
            jsonify({"error": "An error occured while commenting to the recipe"}),
            500,
        )


@recipes_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_recipe(id):
    try:
        updated_recipe = request.get_json()

        if (
            not updated_recipe.get("name")
            or not updated_recipe.get("ingredients")
            or not updated_recipe.get("steps")
            or not updated_recipe.get("prep_time")
        ):
            return jsonify({"error": "Missing required fields"}), 400

        recipe = Recipe.query.get(id)

        if recipe is None:
            return jsonify({"error": "Recipe not found"}), 404

        user_id = get_jwt_identity()

        if str(recipe.user_id) != user_id:
            return (
                jsonify({"error": "You do not have permission to edit this recipe"}),
                403,
            )

        recipe.name = updated_recipe["name"]
        recipe.ingredients = updated_recipe["ingredients"]
        recipe.steps = updated_recipe["steps"]
        recipe.prep_time = updated_recipe["prep_time"]

        db.session.commit()

        return jsonify(recipe.to_dict()), 200

    except Exception:
        return (
            jsonify(
                {
                    "error": "an error occured while updating the recipe",
                }
            ),
            500,
        )


@recipes_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_recipe(id):
    try:
        recipe = Recipe.query.get(id)

        if recipe is None:
            return jsonify({"error": "Recipe not found"}), 404

        user_id = get_jwt_identity()

        if str(recipe.user_id) != user_id:
            return (
                jsonify({"error": "You do not have permission to delete this recipe"}),
                403,
            )

        db.session.delete(recipe)
        db.session.commit()

        return jsonify({"message": "Recipe has been deleted successfully"}), 200

    except Exception:
        return (jsonify({"error": "An error occured while deleting recipe"}), 500)
