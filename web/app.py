from flask import Flask, render_template, request
from algorithms.scheduling import generate_schedule

app = Flask(__name__)

@app.route('/generate_schedule', methods=['POST'])
def generate_student_schedule():
    student_id = request.form['student_id']
    preferences = {
        'preferred_times': request.form.getlist('preferred_times'),
        'preferred_days': request.form.getlist('preferred_days')
    }

    final_schedule, unscheduled_courses = generate_schedule(student_id, preferences)

    return render_template('schedule.html', schedule=final_schedule, unscheduled=unscheduled_courses)

if __name__ == '__main__':
    app.run(debug=True)
