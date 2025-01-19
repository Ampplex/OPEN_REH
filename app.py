# from methods import print_responses
from flask import Flask, request
from flask_cors import CORS, cross_origin
from OpenAI_layer2 import filter_resp
 
app = Flask(__name__)
PORT = 5050 

cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route("/submit", methods=["POST"])
def submit():
    try:
        # final_response = print_responses()
        prompt = request.form['prompt']
        user_param = request.form['param']
        output = filter_resp(prompt, user_param)
        return {
            "response": output
        }
    except Exception as e:
        return {
            "error": str(e)
        }

if __name__ == "__main__":
    print(f"Server is runnihng at http://localhost:{PORT}")
    app.run(debug=True, host='0.0.0.0', port=PORT)