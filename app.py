from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# DATABASE MODEL
class Attack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    technique_id = db.Column(db.String(20), nullable=False)
    tactic = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# HOME PAGE
@app.route('/')
def index():
    attacks = Attack.query.order_by(Attack.date.desc()).all()
    return render_template('index.html', attacks=attacks)

# ADD ATTACK
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        attack = Attack(
            title=request.form['title'],
            technique_id=request.form['technique_id'],
            tactic=request.form['tactic'],
            severity=request.form['severity'],
            description=request.form['description']
        )
        db.session.add(attack)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html')

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    attacks = Attack.query.all()

    total = len(attacks)
    high = len([a for a in attacks if a.severity == "High"])
    medium = len([a for a in attacks if a.severity == "Medium"])
    low = len([a for a in attacks if a.severity == "Low"])

    return render_template("dashboard.html",
                           total=total,
                           high=high,
                           medium=medium,
                           low=low)

# CREATE DB + RUN
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
