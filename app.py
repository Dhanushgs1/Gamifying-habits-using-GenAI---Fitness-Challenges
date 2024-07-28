from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in days

    def __repr__(self):
        return f'<Challenge {self.name}>'

@app.route('/')
def index():
    challenges = Challenge.query.all()
    return render_template('index.html', challenges=challenges)

@app.route('/add', methods=['POST'])
def add_challenge():
    name = request.form.get('name')
    description = request.form.get('description')
    duration = request.form.get('duration')

    if not name or not description or not duration:
        flash('All fields are required!', 'error')
        return redirect(url_for('index'))

    new_challenge = Challenge(name=name, description=description, duration=int(duration))
    db.session.add(new_challenge)
    db.session.commit()

    flash('Challenge added successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
