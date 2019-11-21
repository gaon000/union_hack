from flask import Flask
from flask_restful import Resource, Api, reqparse
import pymongo

conn = pymongo.MongoClient("localhost",27017)
db = conn.hack
collection_rgb = db.rgb
collection_humi = db.humi
collection_temp = db.temp
collection_gas = db.gas
collection_lev = db.lev
collection_illum = db.illum
collection_bright = db.bright

app = Flask(__name__)
api = Api(app)

class set_data(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("humidity",type=float)
        parser.add_argument("temp",type=float)
        parser.add_argument("gas",type=int)
        parser.add_argument("illum",type=int)
        parser.add_argument("lev",type=int)
        parser.add_argument("red",type=int)
        parser.add_argument("green",type=int)
        parser.add_argument("blue",type=int)
        parser.add_argument("bright",float)
        args = parser.parse_args()
        if args['humidity']:
            collection_humi.insert({"humidity":args['humidity']})
        if args['temp']:
            collection_temp.insert({"temp":args['temp']})
        if args['gas']:
            collection_gas.insert({"gas":args['gas']})
        if args['illum']:
            collection_illum.insert({"illum":args['illum']})
        if args['lev']:
            collection_lev.insert({"lev":args['lev']})
        if args['red'] and args['blue'] and args['green']:
            collection_rgb.insert({"red":args['red'],"green":args['green'],"blue":args['blue']})
        if args['bright']:
            bright = float(args['bright'])/1000
            collection_bright.insert({'bright':bright})
        print(args['humidity'],args['gas'],args['lev'])

        return 1

class rgb(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("red", type=int)
        parser.add_argument("green",type=int)
        parser.add_argument("blue",type=int)
        parser.add_argument("bright",type=float)
        args = parser.parse_args()
        print(args['red'])
    def get(self):
        return {"red":collection_rgb.find()[collection_rgb.count()-1]['red'],"green":collection_rgb.find()[collection_rgb.count()-1]['green'],"blue":collection_rgb.find()[collection_rgb.count()-1]['blue'],"bright":collection_bright.find()[collection_bright.count()-1]['bright']}

class illum(Resource):
    def get(self):
        return {"illum":collection_illum.find()[collection_illum.count()-1]['illum']}

class gas(Resource):
    def get(self):
        return {"gas":collection_gas.find()[collection_gas.count()-1]['gas']}

class lev(Resource):
    def get(self):
        return {"lev":collection_lev.find()[collection_lev.count()-1]['lev']}

class temp(Resource):
    def get(self):
        return {"temp":collection_temp.find()[collection_temp.count()-1]['temp']}

class humidity(Resource):
    def get(self):
        return {"humidity":collection_humi.find()[collection_humi.count()-1]['humidity']}
    



class test(Resource):
    def get(self):
        return 'test'


api.add_resource(set_data, '/set_data')
api.add_resource(test, '/')
api.add_resource(rgb, '/light')
api.add_resource(illum,'/illum')
api.add_resource(temp,'/temp')
api.add_resource(gas,'/gas')
api.add_resource(lev,'/lev')
api.add_resource(humidity,'/humidity')



if __name__ == '__main__':
	app.run(debug=True)
