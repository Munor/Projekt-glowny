from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SECRET_KEY'] = 'tajny_klucz_do_formularzy'
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))

@app.route('/')
def index():
    transactions = Transaction.query.order_by(Transaction.id.desc()).all()
    return render_template('index.html', transactions=transactions)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_transaction = Transaction(
            type=request.form['type'],
            category=request.form['category'],
            amount=float(request.form['amount']),
            description=request.form['description']
        )
        db.session.add(new_transaction)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)