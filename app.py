from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

base_url = '/api/v1'

class Drink(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(80), unique=True, nullable=False)
    description: str = db.Column(db.String(240))

    def __repr__(self) -> str:
        return f"{self.name} - {self.description}"

@app.route('/')
def index() -> str:
    return 'Test Flask API home route'

@app.route(f'{base_url}/drinks', methods=['GET', 'POST'])
def handle_req() -> dict:
    if request.method == 'GET':
        drinks: list[Drink] = Drink.query.all()
        res = []
        for drink in drinks:
            entry = {
                'name': drink.name, 
                'description': drink.description
            }
            res.append(entry)
        return {
            "drinks": res
        }
    elif request.method == 'POST':
        drink: Drink = Drink(
            name=request.json['name'],
            description=request.json['description']
        )

        db.session.add(drink)
        db.session.commit()

        return {
            'id': drink.id
        }

@app.route(f'{base_url}/drinks/<id>', methods=['GET', 'DELETE'])
def get_drink(id) -> dict:
    
    drink: Drink or None = Drink.query.get_or_404(id)

    if request.method == 'GET':
        if drink is None:
            return { 
                'status': 'not found' 
            }
        else:
            return jsonify({
                'name': drink.name,
                'description': drink.description
            })
    elif request.method == 'DELETE':
        if drink is None:
            return { 
                'status': 'not found'
            }
        else:
            db.session.delete(drink)
            db.session.commit()
            return { 
                'status': 'success'
            }

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)