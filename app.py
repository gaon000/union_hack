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
            collection_illum.insert({'illum':bright})
        print(args['lev'])


class graph_illum(Resource):
    def get(self):
        return {"illum_graph":[collection_illum.find()[collection_illum.count()-1]['illum']*100,collection_illum.find()[collection_illum.count()-2]['illum']*100,collection_illum.find()[collection_illum.count()-3]['illum']*100,collection_illum.find()[collection_illum.count()-4]['illum']*100,collection_illum.find()[collection_illum.count()-5]['illum']*100,collection_illum.find()[collection_illum.count()-6]['illum']*100,collection_illum.find()[collection_illum.count()-7]['illum']*100,collection_illum.find()[collection_illum.count()-8]['illum']*100,collection_illum.find()[collection_illum.count()-9]['illum']*100,collection_illum.find()[collection_illum.count()-10]['illum']*100]}

class graph_humi(Resource):
    def get(self):
        return {"humi_graph":[collection_humi.find()[collection_humi.count()-1]['humidity'],collection_humi.find()[collection_humi.count()-2]['humidity'],collection_humi.find()[collection_humi.count()-3]['humidity'],collection_humi.find()[collection_humi.count()-4]['humidity'],collection_humi.find()[collection_humi.count()-5]['humidity'],collection_humi.find()[collection_humi.count()-6]['humidity'],collection_humi.find()[collection_humi.count()-7]['humidity'],collection_humi.find()[collection_humi.count()-8]['humidity'],collection_humi.find()[collection_humi.count()-9]['humidity'],collection_humi.find()[collection_humi.count()-10]['humidity']]}

class graph_gas(Resource):
    def get(self):
        return {"gas_graph":[collection_gas.find()[collection_gas.count()-1]['gas'],collection_gas.find()[collection_gas.count()-2]['gas'],collection_gas.find()[collection_gas.count()-3]['gas'],collection_gas.find()[collection_gas.count()-4]['gas'],collection_gas.find()[collection_gas.count()-5]['gas'],collection_gas.find()[collection_gas.count()-6]['gas'],collection_gas.find()[collection_gas.count()-7]['gas'],collection_gas.find()[collection_gas.count()-8]['gas'],collection_gas.find()[collection_gas.count()-9]['gas'],collection_gas.find()[collection_gas.count()-10]['gas']]}

class graph_temp(Resource):
    def get(self):
        
        # return {"temp":collection_temp.find()[collection_temp.count()-1]['temp']}
        return {"temp_graph":[collection_temp.find()[collection_temp.count()-1]['temp'],collection_temp.find()[collection_temp.count()-2]['temp'],collection_temp.find()[collection_temp.count()-3]['temp'],collection_temp.find()[collection_temp.count()-4]['temp'],collection_temp.find()[collection_temp.count()-5]['temp'],collection_temp.find()[collection_temp.count()-6]['temp'],collection_temp.find()[collection_temp.count()-7]['temp'],collection_temp.find()[collection_temp.count()-8]['temp'],collection_temp.find()[collection_temp.count()-9]['temp'],collection_temp.find()[collection_temp.count()-10]['temp']]}

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
        return {"red":collection_rgb.find()[collection_rgb.count()-1]['red'],"green":collection_rgb.find()[collection_rgb.count()-1]['green'],"blue":collection_rgb.find()[collection_rgb.count()-1]['blue'],"illum":1-collection_illum.find()[collection_illum.count()-1]['illum']}

class bright(Resource):
    def get(self):
        return {"bright":collection_bright.find()[collection_bright.count()-1]['bright']}

class get_data(Resource):
    def get(self):
        return {"illum":collection_illum.find()[collection_illum.count()-1]['illum'],"gas":collection_gas.find()[collection_gas.count()-1]['gas'],"temp":collection_temp.find()[collection_temp.count()-1]['temp'],"humidity":collection_humi.find()[collection_humi.count()-1]['humidity']}

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
api.add_resource(get_data,'/get_data')
api.add_resource(graph_illum,'/gpi')
api.add_resource(graph_humi,'/gph')
api.add_resource(graph_gas,'/gpg')
api.add_resource(graph_temp,'/gpt')
api.add_resource(bright,'/bright')

if __name__ == '__main__':
	app.run(debug=True)
