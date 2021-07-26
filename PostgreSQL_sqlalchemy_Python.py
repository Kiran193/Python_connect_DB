# $ pip install psycopg2-binary
# $ pip install flask-sqlalchemy
# $ pip install Flask-Migrate


######## In app.py 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/db_Test"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class CarsModel(db.Model):
    # __tablename__ = 'cars'
    __tablename__ = 'tbl_Test'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    department = db.Column(db.String())
    # doors = db.Column(db.Integer())

    def __init__(self, col_name, col_department):
        self.name = col_name
        self.department = col_department
        # self.doors = doors

    def __repr__(self):
        return f"< {self.name}>"

@app.route('/')
def hello():
    return {"hello": "world"}

@app.route('/cars', methods=['POST', 'GET'])
def handle_cars():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            print(data)
            new_car = CarsModel(col_name=data['name'], col_department=data['dept'])
            db.session.add(new_car)
            db.session.commit()
            # return {"message": f"car {new_car.name} has been created successfully."}
            return {"message": f"{new_car.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        cars = CarsModel.query.all()
        results = [
            {
                "name": car.name,
                "dept": car.department
            } for car in cars]

        return {"count": len(results), "cars": results}

@app.route('/cars/<car_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_car(car_id):
    car = CarsModel.query.get_or_404(car_id)

    if request.method == 'GET':
        response = {
            "name": car.name,
            "dept": car.department
        }
        return {"message": "success", "car": response}

    elif request.method == 'PUT':
        data = request.get_json()
        car.name = data['name']
        car.department = data['dept']
        db.session.add(car)
        db.session.commit()
        return {"message": f"car {car.name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(car)
        db.session.commit()
        return {"message": f"Car {car.name} successfully deleted."}


if __name__ == '__main__':
    app.run(debug=True)