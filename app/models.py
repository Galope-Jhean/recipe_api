from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    ratings = db.relationship("Rating", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Rating(db.Model):
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "recipe_id": self.recipe_id,
            "user_id": self.user_id,
            "rating": self.rating,
            "created_at": self.created_at,
        }


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "recipe_id": self.recipe_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "created_at": self.created_at,
        }


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.JSON, nullable=False)
    steps = db.Column(db.JSON, nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref="recipes", lazy=True)
    ratings = db.relationship("Rating", backref="recipe", lazy=True)
    comments = db.relationship("Comment", backref="recipe", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients,
            "steps": self.steps,
            "prep_time": self.prep_time,
            "user_id": self.user_id,
        }
