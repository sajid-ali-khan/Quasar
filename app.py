# quiz_generator.py
from flask import Flask, request, jsonify
import google.generativeai as genai
import json

# Initialize Gemini API
genai.configure(api_key="AIzaSyBVzjgDKS1V0R18V8hwKrSi_P42aR1cIhQ")
model = genai.GenerativeModel("gemini-2.0-flash")

app = Flask(__name__)

import json

def generate_questions(skill, level, goal):
    prompt = f"""You are an expert in personalized learning assessment. Given a user’s interested skill, self-assessed level, and learning goal, generate 10 insightful multiple-choice questions to evaluate their understanding of the subject in json format.

            Each question should:
            
            Be relevant to the skill and level.
            Cover key concepts necessary for achieving the user's goal.
            Vary in difficulty while aligning with the user's self-assessed level.
            Not include answers—only questions and multiple-choice options.
            Have exactly four options per question.
            frame the questions such That generated options must be under 5 words
            Here is the user’s input:
            
              "interested_skill": "{skill}",
              "self_assessed_level": "{level}",
              "goal": "{goal}"
"""

    response = model.generate_content(prompt)

    # Debug: Print raw response
    print("Raw Response:", response.text)

    # Remove triple backticks if present
    clean_response = response.text.strip("```json").strip("```").strip()

    try:
        data = json.loads(clean_response)  # Parse cleaned JSON
        return data
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        return {"error": "Invalid response format"}





# quiz_evaluator.py
@app.route('/evaluate_quiz', methods=['POST'])
def evaluate_quiz():
    data = request.get_json()
    questions_and_answers = data.get("questions_and_answers", [])

    prompt = f"Evaluate the following quiz responses and provide a score with explanations: {json.dumps(questions_and_answers)}"
    response = model.generate_content(prompt)
    evaluation = json.loads(response.text)

    return jsonify(evaluation)


# path_generator.py
@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()
    interested_skill = data.get("interested_skill")
    self_assessed_level = data.get("self_assessed_level")
    goal = data.get("goal")

    if not interested_skill:
        return jsonify({"error": "Missing required field: interested_skill"}), 400

    questions = generate_questions(interested_skill, self_assessed_level, goal)
    return jsonify({"skill": interested_skill, "questions": questions})



if __name__ == '__main__':
    app.run(debug=True)