from flask import Flask, render_template, request, redirect, url_for, jsonify
from google import genai

app = Flask(__name__)
ai_enabled = False  # toggle variable

# Gemini API key
client = genai.Client(api_key="AIzaSyA8gUMPVGVA3rjMkd2iMSxkqbxo-vX9gnA")

@app.route('/')
def home():
    return render_template('index.html', ai_enabled=ai_enabled)

@app.route('/toggle_ai')
def toggle_ai():
    global ai_enabled
    ai_enabled = not ai_enabled
    return redirect(url_for('home'))

@app.route('/submit', methods=['POST'])
def submit():
    student_class = request.form['student_class']
    subject = request.form['subject']
    style = request.form['style']

    # You can now use these variables for future processing
    return render_template('index.html', ai_enabled=ai_enabled,
                           student_class=student_class, subject=subject, style=style)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data.get("query", "")
    student_class = data.get("student_class", "unknown")
    subject = data.get("subject", "general")
    style = data.get("style", "simple")

    prompt = f"""
    You are VidyaAI++, a helpful AI tutor for students from government schools.
    Student is from Class {student_class}, learning {subject}, and prefers a {style} learning style.
    They asked: "{query}"
    Please explain in a clear, simple, friendly tone like a school teacher talking to a child.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Sorry, something went wrong: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
