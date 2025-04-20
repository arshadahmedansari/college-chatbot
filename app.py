from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from database import users, students_data, books, add_user, validate_user
from transformers import pipeline

app = Flask(__name__)
app.secret_key = 'secretkey'

# Load AI chatbot
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

# Static chatbot responses
chatbot_responses = {
    "hello": "Hey there! 😊 How can I help you today?",
    "hi": "Hi! 👋 Need any info about college or something else?",
    "how are you": "I'm just a bot, but I'm functioning perfectly! How about you?",
    "college timings": "IMS Noida generally runs from 9:00 AM to 5:00 PM, Monday to Saturday.",
    "library timing": "The library's open from 9:30 AM till 6:00 PM — a great place to read and chill.",
    "holiday": "Sundays, public holidays, and semester breaks are off. Check the academic calendar for details.",
    "canteen": "Yes! The canteen offers snacks, meals, tea, and cold coffee — students love it.",
    "hostel": "IMS offers separate hostels for boys and girls with 24/7 security, WiFi, and meals.",
    "departments": "We have departments like Computer Science, Management, Law, and Journalism.",
    "placement": "The placement cell is active. Companies like Infosys, Wipro, HCL visit for drives.",
    "principal": "Prof. Dr. Kulneet Suri is the Director of IMS Noida — an inspiring personality!",
    "contact": "Contact IMS Noida at +91-120-4798800 or email info@imsnoida.com.",
    "campus location": "The campus is in Sector-62, Noida, Uttar Pradesh – tech hub of NCR.",
    "website": "Visit the official site 👉 https://imsnoida.com.",
    "default": "Hmm, I’m not sure about that 🤔. Try asking about attendance, results, courses, etc."
}

@app.route('/')
def home():
    if 'username' in session:
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_user(username, password):
            session['username'] = username
            return redirect('/dashboard')
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        add_user(username, password)
        return redirect('/login')
    return render_template('signup.html')

from database import students_data, books

from flask import Flask, render_template, session, redirect, url_for
from database import students_data

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    student_info = students_data.get(username.title())

    if not student_info:
        return "Student data not found.", 404

    # 1. Average Attendance
    attendance_data = student_info.get('attendance', {})
    attendance_values = attendance_data.values()
    avg_attendance = sum([int(value.strip('%')) for value in attendance_values]) // len(attendance_values) if attendance_values else 0

    # 2. GPA Calculation
    grade_scale = {"A+": 10, "A": 9, "B+": 8, "B": 7, "C": 6}
    results = student_info.get('results', {})
    gpa_scores = [grade_scale.get(grade, 0) for grade in results.values()]
    gpa = round(sum(gpa_scores) / len(gpa_scores), 2) if gpa_scores else 0

    # 3. Books Issued
    books_issued = len(student_info.get('books', []))

    # 4. For Chart.js
    subjects = list(attendance_data.keys())
    percentages = [int(value.strip('%')) for value in attendance_data.values()]

    return render_template("dashboard.html",
                           username=username,
                           avg_attendance=f"{avg_attendance}%",
                           gpa=gpa,
                           books_issued=books_issued,
                           subjects=subjects,
                           percentages=percentages)


@app.route('/attendance')
def attendance():
    username = session.get('username')
    if not username or username not in students_data:
        return redirect('/login')

    data = students_data[username]
    attendance_data = data.get('attendance', {})
    
    # Convert attendance percentages from strings like "85%" to integers
    percentages = []
    for val in attendance_data.values():
        if val.endswith('%'):
            try:
                percentages.append(int(val.replace('%', '')))
            except:
                continue

    total_courses = len(attendance_data)
    overall = round(sum(percentages) / total_courses, 2) if total_courses > 0 else 0

    return render_template(
        'attendance.html',
        name=data.get('name', username),
        attendance=attendance_data,
        overall_attendance=overall
    )
@app.route('/results', methods=['GET'])
def results():
    # Retrieve the username from session (assumed to be logged in)
    username = session.get('username')
    
    # Fetch student data from the database (replace this with your actual database access code)
    student_data = students_data.get(username)  # Example: `students_data` can be a dictionary or fetched from your database
    
    if not student_data:
        return redirect(url_for('login'))  # Redirect to login if no student data is found

    # Grade scale used to calculate GPA
    grade_scale = {"A+": 10, "A": 9, "B+": 8, "B": 7, "C": 6}
    
    # Retrieve results from student data (this should be a dictionary of subject: grade pairs)
    results = student_data.get('results', {})
    
    # GPA Calculation using the grade scale
    gpa_scores = [grade_scale.get(grade, 0) for grade in results.values()]  # Convert grades to GPA points
    gpa = round(sum(gpa_scores) / len(gpa_scores), 2) if gpa_scores else 0  # Average GPA if grades exist, else 0
    
    # Render the results page with student's information, results, and calculated GPA
    return render_template('results.html', 
                           name=student_data['name'], 
                           results=results, 
                           total_gpa=gpa)

@app.route('/courses')
def courses():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    data = students_data.get(username)
    if not data:
        return "Student data not found", 404

    name = data.get('name', 'Student')
    courses = data.get('courses', [])

    return render_template('courses.html', name=name, courses=courses)

@app.route('/books')
def books_page():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    return render_template('books.html', books=books)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect('/login')
    bot_response = "Hi! How can I assist you today?"
    user_message = None
    if request.method == 'POST':
        user_message = request.form['message']
        bot_response = chatbot_responses.get(user_message.lower(), chatbot_responses['default'])
    return render_template('chat.html', bot_response=bot_response, user_message=user_message)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    if 'username' not in session:
        return jsonify({"response": "You need to log in first."})

    data = request.get_json()
    message = data.get("message", "")
    if not message:
        return jsonify({"response": "Please type something first."})

    username = session['username']
    student = students_data.get(username, {})
    msg = message.lower().strip()

    # 1. Static response check
    if msg in chatbot_responses:
        return jsonify({"response": chatbot_responses[msg]})

    # 2. Dynamic keyword check
    if any(kw in msg for kw in ["attendance", "my attendance", "show attendance", "what is my attendance"]):
        attendance = student.get("attendance", {})
        if attendance:
            response = "📊 Your attendance:\n" + "\n".join([f"{k}: {v}" for k, v in attendance.items()])
        else:
            response = "No attendance data available."
        return jsonify({"response": response})

    if any(kw in msg for kw in ["result", "results", "my result", "show marks", "marks", "what is my result"]):
        results = student.get("results", {})
        if results:
            response = "📄 Your results:\n" + "\n".join([f"{k}: {v}" for k, v in results.items()])
        else:
            response = "No result data found."
        return jsonify({"response": response})

    if any(kw in msg for kw in ["courses", "subjects", "enrolled", "my courses", "what courses"]):
        courses = student.get("courses", [])
        if courses:
            response = "📚 You are enrolled in:\n" + ", ".join(courses)
        else:
            response = "No courses enrolled currently."
        return jsonify({"response": response})

    if any(kw in msg for kw in ["books", "book list", "available books", "show books"]):
        if books:
            response = "📘 Available books:\n" + "\n".join(f"- {book}" for book in books)
        else:
            response = "No books available right now."
        return jsonify({"response": response})

    # 3. Fallback AI-generated response
    try:
        prompt = f"You are a helpful assistant for IMS Noida. The student is already logged in. " \
                 f"Answer this question: \"{message}\" without asking for ID."
        generated = chatbot(prompt, max_length=150, num_return_sequences=1)[0]['generated_text']
        ai_reply = generated.replace(prompt, '').strip()
        return jsonify({"response": ai_reply if ai_reply else chatbot_responses["default"]})
    except Exception as e:
        print(f"AI error: {e}")
        return jsonify({"response": "Sorry, something went wrong. Try again later."})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

