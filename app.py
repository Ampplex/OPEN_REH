from flask import Flask, request, jsonify
from flask_cors import CORS
from OpenAI_layer2 import filter_resp
 
app = Flask(__name__)
PORT = 5050 

# Update CORS configuration to allow requests from port 5173
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173"],  # Vite's default port
        "methods": ["POST", "OPTIONS", "GET"],
        "allow_headers": ["Content-Type"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

@app.route("/submit", methods=["POST", "OPTIONS"])
def submit():
    # Handle preflight request
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        return response

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        prompt = data.get('prompt')
        user_param = data.get('param')
        
        if not prompt or not user_param:
            return jsonify({"error": "Missing prompt or param"}), 400
            
        output = filter_resp(prompt, user_param)
        return jsonify({"response": output})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    print(f"Server is running at http://localhost:{PORT}")
    app.run(debug=True, host='0.0.0.0', port=PORT)