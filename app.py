from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =  'mssql+pyodbc://sa:Passw0rd@sqlserver:1433/recipe_db?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&ConnectionTimeout=60'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients,
            "steps": self.steps,
            "prep_time": self.prep_time
        }

@app.route('/')
def index(): 
    return jsonify({"test": "api working"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000) 
