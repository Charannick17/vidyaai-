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

    prompt = f"""
    You are VidyaAI++, an AI tutor for underprivileged students in government schools.

    Please generate a course outline for:
    - Class: {student_class}
    - Subject: {subject}
    - Learning Style: {style}

    Output exactly 8 modules. For each module, give:
    - A short title (e.g., "Module 1: Numbers and Counting")

    Format like:
    Module 1: Title
    Module 2: Title
    (Repeat for all 8 modules)
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        raw_output = response.text

        lines = [line.strip() for line in raw_output.split('\n') if line.strip()]
        modules = []
        for line in lines:
            if ":" in line:
                parts = line.split(":", 1)
                title = parts[1].strip()
                modules.append({"title": title})

    except Exception as e:
        modules = [{"title": "Error: " + str(e)}]

    return render_template('generated.html', ai_enabled=ai_enabled,
                           student_class=student_class, subject=subject, style=style, modules=modules)

@app.route('/subtopic', methods=['GET'])
def subtopic_page():
    subtopic = request.args.get('subtopic')
    subject = request.args.get('subject')
    student_class = request.args.get('student_class')
    style = request.args.get('style')
    language = request.args.get('language', 'English')

    prompt = f"""
You are VidyaAI++, an AI tutor. Based on the module title \"{subtopic}\" for class {student_class}, subject {subject}, and learning style {style}, generate exactly 5 subtopics and 1 final quiz. Use this format:

Subtopic 1: ...
Subtopic 2: ...
Subtopic 3: ...
Subtopic 4: ...
Subtopic 5: ...
Final Quiz: ...

Do not include any additional text or explanations.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        subtopic_content = response.text

        lines = [line.strip() for line in subtopic_content.split('\n') if line.strip()]
        subtopics = []
        quiz = []
        is_quiz = False

        for line in lines:
            if line.lower().startswith("final quiz") or line.lower().startswith("quiz"):
                is_quiz = True
                continue

            if not is_quiz:
                if "subtopic" in line.lower():
                    subtopics.append(line)
            else:
                quiz.append(line)

        if not subtopics and not quiz:
            subtopics = [line for line in lines if not line.lower().startswith("final quiz") and "?" not in line]
            quiz = [line for line in lines if "?" in line or any(op in line for op in ["a)", "b)", "c)", "d)"])]

    except Exception as e:
        subtopics = [f"Error: {str(e)}"]
        quiz = []

    return render_template('subtopic.html', subtopic=subtopic, subject=subject,
                           student_class=student_class, style=style,
                           subtopics=subtopics, quiz=quiz, language=language,
                           ai_enabled=ai_enabled)

@app.route('/learn')
def learn():
    subtopic = request.args.get('subtopic')
    subject = request.args.get('subject')
    student_class = request.args.get('student_class')
    style = request.args.get('style')
    language = request.args.get('language')

    explanation = "Loading explanation..."
    example = "Loading example..."

    # Generate a comprehensive lesson content
    prompt = f"""
    You are VidyaAI++, an AI tutor for underprivileged school students.
    Your job is to create a full, engaging lesson for:
    - Subtopic: {subtopic}
    - Subject: {subject}
    - Class: {student_class}
    - Learning Style: {style}
    - Language: {language}

    The content should include:
    1. A detailed, easy-to-understand definition and explanation of the topic.
    2. Multiple key concepts related to the topic (minimum 5), each with explanations.
    3. At least one relatable example per concept to help students understand in a fun and practical way.

    Format the output as:
    Explanation:
    <Detailed explanation with 5+ concepts>

    Example:
    <Clear, relatable examples>
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # Replace with the correct AI model you're using
            contents=prompt
        )
        content = response.text
        
        # Log the raw content returned by the AI model
        print("Raw AI Response:\n", content)

        # Directly use the entire content as the explanation and example
        explanation = content  # Display the entire response

    except Exception as e:
        explanation = f"Error: {str(e)}"

    return render_template('learn.html',
                           subtopic=subtopic,
                           subject=subject,
                           student_class=student_class,
                           style=style,
                           language=language,
                           explanation=explanation)




if __name__ == '__main__':
    app.run(debug=True)
