import peeweedbevolve
from flask import Flask, render_template, request, jsonify
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

@app.route("/api/v1/transactions", methods=["GET"])
def get_transactions():
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
    

    # query = Transaction.select()
    # data = [i for i in query]
    # if data:
    #     output = {
    #         'success': True,
    #         'data': data
    #     }
    #     res = jsonify(output)
    #     res.status_code = 200
    # else:
    #     output = {
    #         'success': False,
    #         'error': 'Server error'
    #     }
    #     res = jsonify(output)
    #     res.status_code = 404
    # return res

if __name__ == "__main__":
    app.run()