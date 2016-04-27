from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy

import hackbright

app = Flask(__name__)

# sets up the database db
db = SQLAlchemy()

def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    db.app = app
    db.init_app(app)



@app.route("/student")
def get_student():
    """Show information about a student."""

    # gets information from student_search form
    github = request.args.get('github')
    first, last, github = hackbright.get_student_by_github(github)


    rows = hackbright.get_grades_by_github(github)


    # directs to student_info page
    return render_template("student_info.html", 
                            first=first,
                            last=last,
                            github=github,
                            rows=rows)


@app.route('/')
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")



@app.route('/add-a-student')
def add_student_form():
    """Show form for adding a student."""

    return render_template("student_add.html")



@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    # gathers information from student_add form
    first_name = request.args.get('first')
    last_name = request.args.get('last')
    github = request.args.get('github')

    # creates query
    QUERY = """
    INSERT INTO Students 
    VALUES (:first_name, :last_name, :github)
    """
    
    # executes query
    db.session.execute(QUERY, {'first_name': first_name, 
                                'last_name': last_name, 
                                'github': github})
    # commits add to db
    db.session.commit()

    # directs to student_info page
    return render_template("student_info.html", 
                            first=first_name,
                            last=last_name,
                            github=github)

@app.route('/project')
def list_project_info():
    """Gets information about a project"""

    project_title = request.args.get('title')

    print "/n/n/n/n" + project_title

    title, description, max_grade = hackbright.get_project_by_title(project_title)

    return render_template("project_info.html",
                            title=title,
                            description=description,
                            max_grade=max_grade)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
