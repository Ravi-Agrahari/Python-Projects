from flask import Flask, render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

# Configure SQLAlchemy to use SQLite database named todo.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

# Disable SQLAlchemy's modification tracking, as it's not needed in this application
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy database object
db = SQLAlchemy(app)

# Define Todo model representing the todo table in the database
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(400), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Representation of Todo object
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Create tables within the application context
with app.app_context():
    db.create_all()

# Route for homepage
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # If the request method is POST, it means the form is submitted
        
        # Retrieve values from the form
        title = request.form['title']
        desc = request.form['desc']

        # Create a new Todo object with the provided values
        todo = Todo(title=title, desc=desc)

        # Add the new Todo object to the session and commit the transaction
        db.session.add(todo)
        db.session.commit()

    # Retrieve all todos from the database
    allTodo = Todo.query.all()

    # Render the homepage template with allTodo passed to it
    return render_template('index.html', allTodo=allTodo)

 
@app.route('/delete/<int:sno>')
def delete(sno):  # Add sno parameter to the delete route
    # Retrieve the todo item with the given sno from the database
    del_todo = Todo.query.filter_by(sno=sno).first()

    # Check if the todo item exists
    if del_todo:
        # If the todo item exists, delete it from the database
        db.session.delete(del_todo)
        db.session.commit()

    # Redirect to the homepage after deletion
    return redirect('/')


@app.route('/update/<int:sno>' , methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title 
        todo.desc = desc

        db.session.add(todo)
        db.session.commit()

        return redirect('/')

    todo = Todo.query.filter_by(sno = sno).first()
    return render_template('update.html', todo = todo)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
