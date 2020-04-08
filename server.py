import peeweedbevolve
from flask import Flask, render_template, request, json, jsonify
from models import db, Transaction
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

@app.cli.command()
def migrate():
    db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/v1/transactions", methods=["GET", "POST"])
def transactions():
    if request.method == "GET":
        transactions = Transaction.select()
        transactions_array = []
        for transaction in transactions:
            transactions_array.append({'id': transaction.id, 'text': transaction.text, 'amount': transaction.amount})
        
        if transactions_array:
            response = {
                'success': True,
                'data': transactions_array
            }
            return jsonify(response), 200
        else:
            response = {
                'success': False,
                'error': 'Server Error'
            }
            return jsonify(response), 500
    elif request.method == "POST":
        text = request.json.get('text')
        amount = request.json.get('amount')

        transaction = Transaction(text=text, amount=amount)

        if transaction.save():
            response = {
                'success': True,
                'message': 'Transaction successfully created',
                'data': {'id': transaction.id, 'text': transaction.text, 'amount': transaction.amount}
            }
            return jsonify(response)
        else:
            response = {
                'success': False,
                'error': 'Server Error'
            }
            return jsonify(response)

if __name__ == "__main__":
    app.run()