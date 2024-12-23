from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "http://localhost:8080"}})

data = {
    "student_id": [1, 2, 3, 4, 5],
    "test_scores": [85, 90, 78, 92, 88],
    "questions_attempted": [40, 50, 38, 55, 45],
    "time_spent": [120, 150, 100, 160, 140],
    "future_scores": [88, 93, 80, 95, 90],
}

students_df = pd.DataFrame(data)

X = students_df[["test_scores", "questions_attempted", "time_spent"]]
y = students_df["future_scores"]
model = LinearRegression()
model.fit(X, y)

def analyze_performance(student_id):
    student = students_df[students_df['student_id'] == student_id]
    if student.empty:
        return None
    performance_score = (
        student['test_scores'].values[0] * 0.5 +
        student['questions_attempted'].values[0] * 0.3 +
        student['time_spent'].values[0] * 0.2
    )
    return round(performance_score / 100, 2)

def predict_future_success(test_scores, questions_attempted, time_spent):
    prediction = model.predict([[test_scores, questions_attempted, time_spent]])
    return round(prediction[0], 2)

@app.route('/api/performance', methods=['GET'])
def get_performance():
    student_id = request.args.get('student_id', type=int)
    if not student_id:
        return jsonify({"error": "Missing student_id parameter."}), 400

    performance = analyze_performance(student_id)
    if performance is None:
        return jsonify({"error": "Student not found."}), 404

    student = students_df[students_df['student_id'] == student_id]
    future_score = predict_future_success(
        student['test_scores'].values[0],
        student['questions_attempted'].values[0],
        student['time_spent'].values[0]
    )

    return jsonify({
        "student_id": student_id,
        "performance_score": performance,
        "predicted_future_score": future_score
    })

@app.route('/api/report', methods=['GET'])
def get_report():
    students_df['performance_score'] = students_df.apply(
        lambda row: analyze_performance(row['student_id']), axis=1
    )
    students_df['predicted_future_score'] = students_df.apply(
        lambda row: predict_future_success(
            row['test_scores'], row['questions_attempted'], row['time_spent']
        ), axis=1
    )
    return jsonify(students_df.to_dict(orient='records'))

@app.route('/api/add_student', methods=['POST'])
def add_student():
    data = request.json
    if not data or not all(k in data for k in ("student_id", "test_scores", "questions_attempted", "time_spent", "future_scores")):
        return jsonify({"error": "Missing or incomplete data."}), 400

    new_student = pd.DataFrame([data])
    global students_df
    students_df = pd.concat([students_df, new_student], ignore_index=True)

    return jsonify({"message": "Student added successfully."}), 201

@app.route('/api/update_student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    global students_df

    if student_id not in students_df['student_id'].values:
        return jsonify({"error": "Student not found."}), 404

    students_df.loc[students_df['student_id'] == student_id, list(data.keys())] = list(data.values())
    return jsonify({"message": "Student updated successfully."})

@app.route('/api/delete_student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students_df

    if student_id not in students_df['student_id'].values:
        return jsonify({"error": "Student not found."}), 404

    students_df = students_df[students_df['student_id'] != student_id]
    return jsonify({"message": "Student deleted successfully."})

@app.route('/api/visualize', methods=['GET'])
def visualize():
    import matplotlib.pyplot as plt
    import io
    import base64

    plt.figure(figsize=(10, 6))
    plt.scatter(students_df['student_id'], students_df['test_scores'], label='Test Scores', color='blue')
    plt.plot(students_df['student_id'], students_df['predicted_future_score'], label='Predicted Future Score', color='green')
    plt.xlabel('Student ID')
    plt.ylabel('Scores')
    plt.title('Student Performance Analysis')
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return jsonify({"plot_url": f"data:image/png;base64,{plot_url}"})

if __name__ == '__main__':
    app.run(debug=True)