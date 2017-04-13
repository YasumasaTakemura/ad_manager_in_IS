
from flask import Flask,jsonify
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}

api.add_resource(HelloWorld, "/")

# データベースに追加するコード例
@app.route("/p", methods=["POST"])
def p():
    return jsonify(data = {"hello": "post"})


if __name__ == "__main__":
    app.run(debug=True)



