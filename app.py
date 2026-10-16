"""
AI Learning & Study Assistant
Developed by: Shahid Bilal, Owais Qayoom, Musaib Reyaz
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'datasets')
CHARTS_DIR = os.path.join(BASE_DIR, 'static', 'charts')

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(CHARTS_DIR, exist_ok=True)


# ---------------------------------------------------------------
# Default Courses Data (Auto-populates if CSV is missing)
# ---------------------------------------------------------------
DEFAULT_COURSES = [
    {
        "course_id": 1,
        "course_name": "Python Programming",
        "subject": "Python",
        "description": "Python is a high-level, easy-to-learn language. Covers variables, data types, loops, functions, lists, dictionaries, OOP, and file handling.",
        "topics": "Introduction;Variables & Types;Loops;Functions;Lists & Dicts;File Handling;OOP"
    },
    {
        "course_id": 2,
        "course_name": "NumPy for Numerical Computing",
        "subject": "NumPy",
        "description": "Fundamental library for scientific computing. Learn multi-dimensional arrays, matrix operations, broadcasting, and statistical math.",
        "topics": "NumPy Arrays;Array Indexing;Math Operations;Broadcasting;Statistical Functions;Random Numbers"
    },
    {
        "course_id": 3,
        "course_name": "Pandas Data Analysis",
        "subject": "Pandas",
        "description": "Powerful library for data analysis and manipulation. Covers Series, DataFrames, reading CSVs, data cleaning, filtering, and grouping.",
        "topics": "Series & DataFrames;Reading CSV;Filtering Data;Handling Missing Data;GroupBy Operations;Data Aggregation"
    },
    {
        "course_id": 4,
        "course_name": "Matplotlib Data Visualization",
        "subject": "Matplotlib",
        "description": "Create professional charts and plots in Python. Learn line plots, bar charts, scatter plots, histograms, and figure customization.",
        "topics": "Line Plots;Bar Charts;Scatter Plots;Histograms;Subplots;Labels & Titles;Saving Figures"
    },
    {
        "course_id": 5,
        "course_name": "Seaborn Statistical Charts",
        "subject": "Seaborn",
        "description": "High-level statistical visualization library built on Matplotlib. Create attractive heatmaps, box plots, violin plots, and bar plots.",
        "topics": "Distribution Plots;Box & Violin Plots;Bar Plots;Heatmaps;Pair Plots;Color Palettes"
    },
    {
        "course_id": 6,
        "course_name": "Flask Web Development",
        "subject": "Flask",
        "description": "Lightweight Python web framework. Learn URL routing, Jinja2 templates, form handling, POST requests, and building web apps.",
        "topics": "Routing;Jinja2 Templates;HTML Forms;GET & POST;Static Files;Template Inheritance"
    },
    {
        "course_id": 7,
        "course_name": "HTML5 Web Structure",
        "subject": "HTML",
        "description": "The foundation of web development. Learn tags, headings, paragraphs, lists, links, images, tables, semantic elements, and modern forms.",
        "topics": "Document Structure;Headings & Paragraphs;Links & Images;Lists & Tables;Forms & Inputs;Semantic HTML"
    },
    {
        "course_id": 8,
        "course_name": "CSS3 Styling & Responsive Design",
        "subject": "CSS",
        "description": "Style modern web pages. Master selectors, box model, flexbox, grid, keyframe animations, transitions, and mobile-responsive media queries.",
        "topics": "Selectors & Colors;Box Model;Flexbox;CSS Grid;Animations;Media Queries;Responsive Design"
    },
    {
        "course_id": 9,
        "course_name": "JavaScript Fundamentals",
        "subject": "JavaScript",
        "description": "The programming language of the web. Learn variables, arrow functions, DOM manipulation, events, arrays, objects, and ES6+ features.",
        "topics": "Variables (let, const);Functions;DOM Manipulation;Events;Arrays & Objects;ES6 Features;Async JS"
    },
    {
        "course_id": 10,
        "course_name": "C Programming Language",
        "subject": "C",
        "description": "High-performance general-purpose language. Master variables, pointers, dynamic memory allocation, structures, and low-level system code.",
        "topics": "Syntax & Data Types;Operators;Control Statements;Functions;Pointers;Structures;File I/O"
    },
    {
        "course_id": 11,
        "course_name": "C++ Object-Oriented Programming",
        "subject": "C++",
        "description": "Powerful language for system software and game development. Learn classes, objects, inheritance, polymorphism, templates, and STL.",
        "topics": "Classes & Objects;Constructors;Inheritance;Polymorphism;Encapsulation;Templates;STL Library"
    },
    {
        "course_id": 12,
        "course_name": "Java Core Programming",
        "subject": "Java",
        "description": "Platform-independent object-oriented language. Learn JVM basics, OOP concepts, exception handling, collections framework, and multithreading.",
        "topics": "Java Basics;OOP Concepts;Inheritance;Interfaces;Exception Handling;Collections Framework;Multithreading"
    },
    {
        "course_id": 13,
        "course_name": "Database Management & SQL",
        "subject": "SQL",
        "description": "Master relational databases. Learn table creation, SELECT queries, WHERE filters, JOIN operations, GROUP BY aggregations, and normalization.",
        "topics": "Database Basics;CREATE & INSERT;SELECT & WHERE;JOINs;GROUP BY;Subqueries;Normalization"
    },
    {
        "course_id": 14,
        "course_name": "Data Structures & Algorithms (DSA)",
        "subject": "DSA",
        "description": "Core computer science fundamentals. Learn arrays, linked lists, stacks, queues, trees, graphs, sorting, searching, and Big-O notation.",
        "topics": "Arrays & Strings;Linked Lists;Stacks & Queues;Trees & Graphs;Sorting & Searching;Big-O Analysis"
    },
    {
        "course_id": 15,
        "course_name": "Object-Oriented Programming (OOP)",
        "subject": "OOP",
        "description": "Master the four pillars of OOP: Encapsulation, Inheritance, Polymorphism, and Abstraction to write clean, reusable, modular software.",
        "topics": "Encapsulation;Inheritance;Polymorphism;Abstraction;Classes & Objects;Interfaces;Design Principles"
    },
    {
        "course_id": 16,
        "course_name": "Operating Systems (OS)",
        "subject": "OS",
        "description": "Understand how computers manage resources. Covers processes, threads, CPU scheduling algorithms, memory management, virtual memory, and deadlocks.",
        "topics": "Processes & Threads;CPU Scheduling;Memory Management;Virtual Memory;File Systems;Deadlocks;Linux Basics"
    },
    {
        "course_id": 17,
        "course_name": "Computer Networks",
        "subject": "Networking",
        "description": "Learn how computers communicate. Covers OSI 7-layer model, TCP/IP, IP addressing, DNS, HTTP/HTTPS protocols, routers, switches, and network security.",
        "topics": "OSI 7 Layers;TCP/IP Model;IP Addressing;HTTP & DNS;Routers & Switches;Network Protocols;Security Basics"
    },
    {
        "course_id": 18,
        "course_name": "Artificial Intelligence & Machine Learning",
        "subject": "AI",
        "description": "Introduction to AI and machine learning. Covers supervised vs unsupervised learning, neural networks, computer vision, NLP, and real-world AI applications.",
        "topics": "What is AI;Machine Learning Types;Supervised Learning;Unsupervised Learning;Neural Networks;NLP Basics"
    },
    {
        "course_id": 19,
        "course_name": "Cybersecurity Fundamentals",
        "subject": "Cybersecurity",
        "description": "Protect systems and data from attacks. Covers CIA triad, malware, phishing, firewalls, encryption, authentication, and ethical hacking basics.",
        "topics": "CIA Triad;Threats & Malware;Encryption;Firewalls;2FA Authentication;Ethical Hacking;Best Practices"
    },
    {
        "course_id": 20,
        "course_name": "Software Engineering & Git",
        "subject": "Software Engineering",
        "description": "Professional development practices. Learn SDLC models, Agile/Scrum methodologies, software testing, Git version control, and GitHub workflows.",
        "topics": "SDLC Models;Agile & Scrum;Git Basics;Branching & Merging;GitHub;Software Testing;Code Quality"
    }
]


def load_courses():
    """Load courses from CSV. If missing, auto-create it from DEFAULT_COURSES."""
    filepath = os.path.join(DATASET_DIR, 'courses.csv')
    try:
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            if not df.empty and 'course_name' in df.columns:
                return df
        # If missing or empty, create default
        df = pd.DataFrame(DEFAULT_COURSES)
        df.to_csv(filepath, index=False)
        return df
    except Exception:
        return pd.DataFrame(DEFAULT_COURSES)


def load_csv(filename, required_columns=None):
    filepath = os.path.join(DATASET_DIR, filename)
    try:
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            if required_columns:
                for col in required_columns:
                    if col not in df.columns:
                        df[col] = ''
            return df
        else:
            if required_columns:
                return pd.DataFrame(columns=required_columns)
            return pd.DataFrame()
    except Exception:
        if required_columns:
            return pd.DataFrame(columns=required_columns)
        return pd.DataFrame()


def load_notes():
    return load_csv('notes.csv', ['note_id', 'course_id', 'subject', 'topic', 'title', 'content'])


def load_quizzes():
    return load_csv('quizzes.csv', ['question_id', 'subject', 'topic', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer'])


def load_performance():
    return load_csv('performance.csv', ['attempt_id', 'student_label', 'subject', 'quiz_date', 'total_questions', 'correct_answers', 'score_percentage'])


def load_study_support():
    return load_csv('study_support.csv', ['support_id', 'topic', 'keywords', 'question', 'answer'])


def save_quiz_result(student_label, subject, total_questions, correct_answers, score_percentage):
    performance_df = load_performance()
    if len(performance_df) > 0 and 'attempt_id' in performance_df.columns:
        try:
            max_id = int(pd.to_numeric(performance_df['attempt_id'], errors='coerce').max())
        except Exception:
            max_id = 0
        new_id = max_id + 1
    else:
        new_id = 1

    new_record = pd.DataFrame([{
        'attempt_id': new_id,
        'student_label': student_label,
        'subject': subject,
        'quiz_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'score_percentage': score_percentage
    }])

    updated_df = pd.concat([performance_df, new_record], ignore_index=True)
    filepath = os.path.join(DATASET_DIR, 'performance.csv')
    updated_df.to_csv(filepath, index=False)


def generate_performance_charts():
    charts = {'scores_chart': False, 'subject_chart': False}
    performance_df = load_performance()

    if performance_df.empty:
        return charts

    performance_df['score_percentage'] = pd.to_numeric(performance_df['score_percentage'], errors='coerce')
    performance_df = performance_df.dropna(subset=['score_percentage'])

    if performance_df.empty:
        return charts

    try:
        scores_array = np.array(performance_df['score_percentage'].values, dtype=float)
        attempts = np.arange(1, len(scores_array) + 1)
        avg_score = np.mean(scores_array)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(attempts, scores_array, marker='o', color='#2563EB', linewidth=2.5, markersize=9, label='Score (%)')
        ax.axhline(y=avg_score, color='#EF4444', linestyle='--', linewidth=1.5, label='Average ({:.1f}%)'.format(avg_score))
        ax.fill_between(attempts, scores_array, alpha=0.15, color='#2563EB')
        ax.set_xlabel('Quiz Attempt', fontsize=12, fontweight='bold')
        ax.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
        ax.set_title('Quiz Scores Across Attempts', fontsize=14, fontweight='bold', color='#1E3A8A')
        ax.set_ylim(0, 105)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(CHARTS_DIR, 'scores_chart.png'), dpi=120, facecolor='white')
        plt.close(fig)
        charts['scores_chart'] = True
    except Exception:
        charts['scores_chart'] = False

    try:
        subject_stats = performance_df.groupby('subject')['score_percentage'].mean().reset_index()
        subject_stats.columns = ['Subject', 'Average']

        if not subject_stats.empty:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(data=subject_stats, x='Subject', y='Average', palette='Blues_d', ax=ax, edgecolor='#1E3A8A')
            ax.set_xlabel('Subject', fontsize=12, fontweight='bold')
            ax.set_ylabel('Average Score (%)', fontsize=12, fontweight='bold')
            ax.set_title('Average Performance by Subject', fontsize=14, fontweight='bold', color='#1E3A8A')
            ax.set_ylim(0, 105)
            plt.xticks(rotation=20, ha='right')
            ax.grid(True, axis='y', alpha=0.3)
            fig.tight_layout()
            fig.savefig(os.path.join(CHARTS_DIR, 'subject_chart.png'), dpi=120, facecolor='white')
            plt.close(fig)
            charts['subject_chart'] = True
    except Exception:
        charts['subject_chart'] = False

    return charts


def calculate_performance_stats():
    stats = {
        'total_quizzes': 0,
        'average_score': 0.0,
        'highest_score': 0.0,
        'lowest_score': 0.0,
        'total_correct': 0,
        'total_questions_answered': 0,
        'subject_stats': [],
        'recent_results': [],
        'has_data': False,
        'is_sample': False
    }

    performance_df = load_performance()
    if performance_df.empty:
        return stats

    performance_df['score_percentage'] = pd.to_numeric(performance_df['score_percentage'], errors='coerce')
    performance_df['correct_answers'] = pd.to_numeric(performance_df['correct_answers'], errors='coerce')
    performance_df['total_questions'] = pd.to_numeric(performance_df['total_questions'], errors='coerce')

    valid_df = performance_df.dropna(subset=['score_percentage'])
    if valid_df.empty:
        return stats

    scores_np = np.array(valid_df['score_percentage'].values, dtype=float)
    correct_np = np.array(valid_df['correct_answers'].fillna(0).values, dtype=float)
    total_q_np = np.array(valid_df['total_questions'].fillna(0).values, dtype=float)

    stats['total_quizzes'] = int(len(scores_np))
    stats['average_score'] = float(np.mean(scores_np))
    stats['highest_score'] = float(np.max(scores_np))
    stats['lowest_score'] = float(np.min(scores_np))
    stats['total_correct'] = int(np.sum(correct_np))
    stats['total_questions_answered'] = int(np.sum(total_q_np))
    stats['has_data'] = True

    if 'student_label' in valid_df.columns:
        sample_count = valid_df['student_label'].astype(str).str.contains('Sample', case=False, na=False).sum()
        if sample_count == len(valid_df):
            stats['is_sample'] = True

    if 'subject' in valid_df.columns:
        subject_groups = valid_df.groupby('subject')['score_percentage']
        for subject_name, group_scores in subject_groups:
            arr = np.array(group_scores.values, dtype=float)
            stats['subject_stats'].append({
                'subject': subject_name,
                'average': float(np.mean(arr)),
                'highest': float(np.max(arr)),
                'lowest': float(np.min(arr)),
                'attempts': int(len(arr))
            })

    recent = valid_df.tail(6).iloc[::-1]
    for _, row in recent.iterrows():
        stats['recent_results'].append({
            'subject': row.get('subject', 'N/A'),
            'date': row.get('quiz_date', 'N/A'),
            'score': row.get('score_percentage', 0),
            'correct': row.get('correct_answers', 0),
            'total': row.get('total_questions', 0),
            'label': row.get('student_label', 'Anonymous')
        })

    return stats


def find_study_answer(user_question):
    if not user_question or user_question.strip() == '':
        return {'answer': 'Please enter a question so I can help you.', 'topic': 'No Input', 'matched': False}

    support_df = load_study_support()
    if support_df.empty:
        return {'answer': 'Study support database unavailable.', 'topic': 'System', 'matched': False}

    question_lower = user_question.lower().strip()
    question_words = question_lower.replace('?', '').replace('!', '').replace('.', '').split()

    best_match = None
    best_score = 0

    for _, row in support_df.iterrows():
        keywords_str = str(row.get('keywords', ''))
        keywords_list = [kw.strip().lower() for kw in keywords_str.split(',') if kw.strip()]

        match_score = 0
        for keyword in keywords_list:
            if ' ' in keyword:
                if keyword in question_lower:
                    match_score += 3
            else:
                if keyword in question_words:
                    match_score += 2
                elif keyword in question_lower:
                    match_score += 1

        topic = str(row.get('topic', '')).lower()
        if topic and topic in question_lower:
            match_score += 2

        if match_score > best_score:
            best_score = match_score
            best_match = row

    if best_match is not None and best_score >= 2:
        return {'answer': str(best_match.get('answer', 'No answer available.')), 'topic': str(best_match.get('topic', 'General')), 'matched': True}
    else:
        return {'answer': 'I could not find a specific answer. Try asking about Python, NumPy, Pandas, Matplotlib, Seaborn, Flask, HTML, CSS, C, C++, Java, JavaScript, SQL, Data Structures, Algorithms, OOP, Networking, Operating Systems, AI, or Cybersecurity.', 'topic': 'No Match Found', 'matched': False}


# ===============================================================
# FLASK ROUTES
# ===============================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/courses')
def courses():
    courses_df = load_courses()
    courses_list = []
    for _, row in courses_df.iterrows():
        topics_str = str(row.get('topics', ''))
        topics_list = [t.strip() for t in topics_str.split(';') if t.strip()]
        courses_list.append({
            'course_id': row.get('course_id', ''),
            'course_name': row.get('course_name', 'Untitled'),
            'subject': row.get('subject', 'General'),
            'description': row.get('description', 'No description available.'),
            'topics': topics_list
        })
    return render_template('courses.html', courses=courses_list)


@app.route('/notes')
def notes():
    notes_df = load_notes()
    subject_filter = request.args.get('subject', '')

    all_notes_df = load_notes()
    subjects = []
    if not all_notes_df.empty and 'subject' in all_notes_df.columns:
        subjects = sorted(all_notes_df['subject'].dropna().unique().tolist())

    if subject_filter and not notes_df.empty:
        filtered_df = notes_df[notes_df['subject'].str.lower() == subject_filter.lower()]
        if not filtered_df.empty:
            notes_df = filtered_df

    notes_list = []
    for _, row in notes_df.iterrows():
        notes_list.append({
            'note_id': row.get('note_id', ''),
            'subject': row.get('subject', 'General'),
            'topic': row.get('topic', ''),
            'title': row.get('title', 'Untitled'),
            'content': str(row.get('content', 'No content.'))
        })

    return render_template('notes.html', notes=notes_list, subjects=subjects, current_subject=subject_filter)


@app.route('/quizzes')
def quizzes():
    quizzes_df = load_quizzes()
    subject_filter = request.args.get('subject', '')

    subjects = []
    if not quizzes_df.empty and 'subject' in quizzes_df.columns:
        subjects = sorted(quizzes_df['subject'].dropna().unique().tolist())

    if subject_filter and not quizzes_df.empty:
        filtered_df = quizzes_df[quizzes_df['subject'].str.lower() == subject_filter.lower()]
        if not filtered_df.empty:
            quizzes_df = filtered_df

    questions = []
    for _, row in quizzes_df.iterrows():
        questions.append({
            'question_id': row.get('question_id', ''),
            'subject': row.get('subject', ''),
            'topic': row.get('topic', ''),
            'question': row.get('question', ''),
            'option_a': row.get('option_a', ''),
            'option_b': row.get('option_b', ''),
            'option_c': row.get('option_c', ''),
            'option_d': row.get('option_d', '')
        })

    return render_template('quizzes.html', questions=questions, subjects=subjects, current_subject=subject_filter)


@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    quizzes_df = load_quizzes()
    if quizzes_df.empty:
        return render_template('quiz_result.html', score=0, total=0, percentage=0, correct_count=0, incorrect_count=0, results=[], subject='General', student_label='Anonymous', error='No quiz questions found.')

    student_label = request.form.get('student_label', '').strip()
    if not student_label:
        student_label = 'Anonymous Student'

    quiz_subject = request.form.get('quiz_subject', 'General')

    if quiz_subject and quiz_subject != 'General':
        subject_df = quizzes_df[quizzes_df['subject'].str.lower() == quiz_subject.lower()]
        if not subject_df.empty:
            quizzes_df = subject_df

    total_questions = 0
    correct_count = 0
    results = []

    for _, row in quizzes_df.iterrows():
        q_id = str(row.get('question_id', ''))
        correct_answer = str(row.get('correct_answer', '')).strip().upper()
        submitted_answer = request.form.get('question_' + q_id, '').strip().upper()

        if not correct_answer:
            continue

        total_questions += 1
        is_correct = (submitted_answer == correct_answer)
        if is_correct:
            correct_count += 1

        results.append({
            'question': row.get('question', ''),
            'submitted': submitted_answer if submitted_answer else 'Not Answered',
            'correct': correct_answer,
            'is_correct': is_correct
        })

    incorrect_count = total_questions - correct_count
    percentage = round((correct_count / total_questions) * 100, 1) if total_questions > 0 else 0.0

    if total_questions > 0:
        save_quiz_result(student_label, quiz_subject, total_questions, correct_count, percentage)

    return render_template('quiz_result.html', score=correct_count, total=total_questions, percentage=percentage, correct_count=correct_count, incorrect_count=incorrect_count, results=results, subject=quiz_subject, student_label=student_label, error=None)


@app.route('/performance')
def performance():
    stats = calculate_performance_stats()
    charts = generate_performance_charts()
    return render_template('performance.html', stats=stats, charts=charts)


@app.route('/ai_support', methods=['GET', 'POST'])
def ai_support():
    answer_data = None
    user_question = ''
    if request.method == 'POST':
        user_question = request.form.get('question', '').strip()
        answer_data = find_study_answer(user_question)
    return render_template('ai_support.html', answer=answer_data, question=user_question)


if __name__ == '__main__':
    # Make sure default datasets exist on launch
    load_courses()
    app.run(debug=True, port=5000)