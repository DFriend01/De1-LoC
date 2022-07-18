from flask import (
    request, json, Flask, make_response, jsonify
)

passcode_valid = False

def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET','POST'])
    def test():
        """
        URL: localhost/

        POST Request
        ===========
            Prints the supplied string

            Body Data (Key: Datatype)
            ======================
            msg : string

            SUCCESS (200)
            =============
            Message was received and printed

            Response Data (Key : Datatype)
            ---------------------------
                msg : string
            
            BAD REQUEST (400)
            =================
            Information is missing in the body
        """
        global passcode_valid

        if request.method == "POST":
            message = request.json['msg']
            if (not message):
                data = {'message' : 'Missing information'}
                
                return jsonify(data), 400
            else:
                print(message)
                print(message['num1'])
                print(message['num2'])
                print(message['num3'])
                print(message['num4'])
                if (message['num1'] == 1 and message['num2'] == 2 and message['num3'] == 3 and message['num4'] == 4):
                    passcode_valid = True
                    return json.dumps({"msg": message}), 200
                else:
                    passcode_valid = False
                    return json.dumps({'message' : 'wrong passcode'}), 400
        
        elif request.method == 'GET':
            message = "Hello"
            print(message)
            if passcode_valid:
                res = make_response(message)
                res.status_code = 200
                passcode_valid = False
            else:
                res = make_response(message)
                res.status_code = 400
            res.mimetype = "text/plain"
            # res.charset = 'ascii'
            res.data = message
            print(res.headers)
            print(res)

            return res

    return app

if __name__ == "__main__":
    create_app()
    

