from flask import Flask, render_template, request, jsonify
import requests  # We'll use this to communicate with the local GPT4All API
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# URL of the local GPT4All API instance (make sure GPT4All is running locally)
GPT4ALL_API_URL = "http://localhost:4891/v1/chat/completions"

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        if not prompt:
            response_text = "Please provide a prompt."
        else:
            # Prepare the data to send to GPT4All API
            data = {
                "model": "Phi-3 Mini Instruct",  # Replace this with your actual model name
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 50,
                "temperature": 0.28
            }
            
            try:
                # Send a POST request to GPT4All API
                response = requests.post(GPT4ALL_API_URL, json=data)
                
                # Check if the response was successful
                if response.status_code == 200:
                    response_data = response.json()
                    response_text = response_data['choices'][0]['message']['content']
                else:
                    response_text = f"Error: {response.status_code}, {response.text}"
            except Exception as e:
                response_text = f"Error: {str(e)}"
    
    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)
