from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

SKILLS = [
    "python","html","css","javascript","sql","git","flask","django","react","aws"
]

def extract_text(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text.lower()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['resume']

    if file:
        text = extract_text(file)

        found_skills = []

        for skill in SKILLS:
            if skill in text:
                found_skills.append(skill)

        score = len(found_skills) * 10

        suggestions = []

        if "python" not in found_skills:
            suggestions.append("Add Python skill")

        if "sql" not in found_skills:
            suggestions.append("Add SQL skill")

        if "git" not in found_skills:
            suggestions.append("Add Git skill")

        return render_template(
            'result.html',
            skills=found_skills,
            score=score,
            suggestions=suggestions
        )

if __name__ == '__main__':
    app.run(debug=True)
