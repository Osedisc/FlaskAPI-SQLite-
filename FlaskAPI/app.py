from flask import Flask
from flask_restful import Api,Resource,abort,reqparse,marshal_with,fields
from flask_sqlalchemy import SQLAlchemy



db=SQLAlchemy()
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"
db.init_app(app)
api=Api(app)



class CityModel(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String[100],nullable=False)
    temp=db.Column(db.String, nullable=False)
    weather=db.Column(db.String, nullable=False)
    people=db.Column(db.String, nullable=False)

    def __repr__(self):
        return "city(name={name},temp={temp},weather={weather},people={people})"

with app.app_context():
    db.create_all()

city_add_args=reqparse.RequestParser()
city_add_args.add_argument("name",type=str,required=True,help="Must be string")
city_add_args.add_argument("temp",type=str,required=True,help="Must be string")
city_add_args.add_argument("weather",type=str,required=True, help="Must be string")
city_add_args.add_argument("people",type=str,required=True, help="Must be string")

city_update_args=reqparse.RequestParser()
city_update_args.add_argument("name",type=str,help="Must be string")
city_update_args.add_argument("temp",type=str,help="Must be string")
city_update_args.add_argument("weather",type=str, help="Must be string")
city_update_args.add_argument("people",type=str, help="Must be string")


resource_field={
    "id":fields.Integer,
    "name":fields.String,
    "temp":fields.String,
    "weather":fields.String,
    "people":fields.String
}




class WeatherCity(Resource):
    @marshal_with(resource_field)
    def get(self,city_id):
        result = CityModel.query.filter_by(id=city_id).first()
        if not result:
            abort(404, message="Province not found")
        return result
    
    @marshal_with(resource_field)
    def post(self,city_id):
        result = CityModel.query.filter_by(id=city_id).first()
        if result:
            abort(404, message="id already exists")
        args=city_add_args.parse_args()
        city=CityModel(id=city_id,name=args["name"],temp=args["temp"],weather=args["weather"],people=args["people"])
        db.session.add(city)
        db.session.commit()
        return city,201
    
    @marshal_with(resource_field)
    def patch(self,city_id):
        args=city_update_args.parse_args()
        result = CityModel.query.filter_by(id=city_id).first()
        if not result:
            abort(404,message="Province not found")
        if args["name"]:
            result.name = args["name"]
        if args["temp"]:
            result.temp = args["temp"]
        if args["weather"]:
            result.weather = args["weather"]
        if args["people"]:
            result.people = args["people"]

        db.session.commit()
        return result,201


        

api.add_resource(WeatherCity,"/weather/<int:city_id>")

if __name__ == '__main__':
    app.run(debug=True)