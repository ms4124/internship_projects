from flask import Flask, request, render_template
from ollama_client import query_ollama

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    prompt = ""
    response = ""
    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        print("PROMPT >", prompt)
        if prompt.strip():
            try:
                response = query_ollama(prompt)
                print("RESPONSE <", response[:300], "...")
            except Exception as e:
                response = f"Error calling Ollama: {e}"
                print("ERROR <", e)
    return render_template("index.html", prompt=prompt, response=response)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
