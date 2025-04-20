users = {}
books = []

students_data = {
    'Arshad': {
        'name': 'Arshad',
        'attendance': {'Math': '85%', 'Science': '90%'},
        'results': {'Math': 'A', 'Science': 'B+'},
        'courses': ['B.Tech CSE', 'AI/ML'],
    },
    'Ashish': {
        'name': 'Ashish',
        'attendance': {'Python': '95%', 'Java': '88%'},
        'results': {'Python': 'A+', 'Java': 'A'},
        'courses': ['B.Tech IT', 'Cloud Computing'],
    },
    'Ashu': {
        'name': 'Ashu',
        'attendance': {'Data Structures': '78%', 'OS': '82%'},
        'results': {'Data Structures': 'B+', 'OS': 'A'},
        'courses': ['BCA', 'Cyber Security'],
    },
    'Anjali': {
        'name': 'Anjali',
        'attendance': {'AI': '92%', 'ML': '89%'},
        'results': {'AI': 'A', 'ML': 'A+'},
        'courses': ['B.Tech CSE', 'AI/ML'],
    },
    'Karan': {
        'name': 'Karan',
        'attendance': {'DBMS': '80%', 'Networks': '84%'},
        'results': {'DBMS': 'B', 'Networks': 'B+'},
        'courses': ['BCA', 'Data Science'],
    },
    'Pooja': {
        'name': 'Pooja',
        'attendance': {'HTML': '98%', 'CSS': '95%'},
        'results': {'HTML': 'A+', 'CSS': 'A+'},
        'courses': ['BCA', 'Web Development'],
    },
    'Amit': {
        'name': 'Amit',
        'attendance': {'Maths': '87%', 'Statistics': '90%'},
        'results': {'Maths': 'A', 'Statistics': 'A'},
        'courses': ['B.Sc Mathematics', 'Data Analytics'],
    },
    'Nisha': {
        'name': 'Nisha',
        'attendance': {'AI': '91%', 'Deep Learning': '89%'},
        'results': {'AI': 'A', 'Deep Learning': 'A+'},
        'courses': ['M.Tech CSE', 'AI/ML'],
    },
    'Vikram': {
        'name': 'Vikram',
        'attendance': {'Cloud': '88%', 'Big Data': '86%'},
        'results': {'Cloud': 'A', 'Big Data': 'B+'},
        'courses': ['MCA', 'Cloud Computing'],
    },
    'Simran': {
        'name': 'Simran',
        'attendance': {'Cyber Law': '93%', 'Ethical Hacking': '89%'},
        'results': {'Cyber Law': 'A+', 'Ethical Hacking': 'A'},
        'courses': ['B.Tech IT', 'Cyber Security'],
    },
    'Farhan': {
        'name': 'Farhan',
        'attendance': {'Python': '85%', 'Data Science': '88%'},
        'results': {'Python': 'A', 'Data Science': 'A+'},
        'courses': ['B.Sc CS', 'Data Science'],
    }
}

def add_user(username, password):
    users[username] = password
    students_data[username] = {
        'name': username.title(),
        'attendance': {'Math': '75%', 'Science': '80%'},
        'results': {'Math': 'B', 'Science': 'B+'},
        'courses': ['BCA', 'AI Foundation'],
    }

def validate_user(username, password):
    return users.get(username) == password
