from flask import Flask, redirect, url_for, render_template, request, flash, session

import decimal
import os
from os.path import join, dirname
from dotenv import load_dotenv
import braintree

app = Flask(__name__)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app.secret_key = os.environ.get('APP_SECRET_KEY')

braintree.Configuration.configure(
    os.environ.get('BT_ENVIRONMENT'),
    os.environ.get('BT_MERCHANT_ID'),
    os.environ.get('BT_PUBLIC_KEY'),
    os.environ.get('BT_PRIVATE_KEY')
)

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

MERCHANT_ACCOUNTS = {
    'usd': "homyakovpp",
    'eu': "my_euro_id",
}


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('new_checkout'))


@app.route('/checkouts/new', methods=['GET'])
def new_checkout():
    client_token = braintree.ClientToken.generate()
    return render_template('checkouts/new.html', client_token=client_token)


@app.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    transaction = braintree.Transaction.find(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': ('Your test transaction has been successfully processed.'
                        'See the Braintree API response and try again.')
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': ('Your test transaction has a status of {}. See the Braintree'
                        ' API response and try again.').format(transaction.status)
        }

    return render_template('checkouts/show.html', transaction=transaction, result=result)


@app.route('/checkouts', methods=['POST'])
def create_checkout():
    curr = request.form['currency']
    price_key = 'price_' + curr
    price = decimal.Decimal(request.form[price_key])
    tx_amount = int(request.form['amount']) * price

    tx_data = {
        'amount': tx_amount,
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True,
            "store_in_vault_on_success": True
        },
        'merchant_account_id': MERCHANT_ACCOUNTS[curr]
    }

    if request.form.get("use_diff_bill_info"):
        tx_data["customer"] = {"email": request.form["email"]}
        tx_data["billing"] = {"street_address": request.form["address"]}
    result = braintree.Transaction.sale(tx_data)
    if result.is_success or result.transaction:
        session["payment_method_token"] = result.transaction.credit_card_details.token
        return redirect(url_for('show_checkout', transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors:
            flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('new_checkout'))


@app.route('/checkouts/one_more', methods=['POST'])
def create_checkout_more():
    price = request.form['price']
    result = braintree.Transaction.sale({
        'amount': price,
        'payment_method_token': session["payment_method_token"],
        'options': {
            "submit_for_settlement": True,
        },
    })
    if result.is_success or result.transaction:
        # session["payment_method_token"] = result.transaction.credit_card_details.token
        return redirect(url_for('show_checkout', transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors:
            flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('new_checkout'))


@app.route('/refund', methods=['POST'])
def refund():
    result = braintree.Transaction.refund(request.form["tx_id"])
    if result.is_success or result.transaction:
        # session["payment_method_token"] = result.transaction.credit_card_details.token
        return redirect(url_for('show_checkout', transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors:
            flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('new_checkout'))
    # result = {}
    # if transaction.status in TRANSACTION_SUCCESS_STATUSES:
    #     result = {
    #         'header': 'Sweet Success!',
    #         'icon': 'success',
    #         'message': ('Your test transaction has been successfully processed.'
    #                     'See the Braintree API response and try again.')
    #     }
    # else:
    #     result = {
    #         'header': 'Transaction Failed',
    #         'icon': 'fail',
    #         'message': ('Your test transaction has a status of {}. See the Braintree'
    #                     ' API response and try again.').format(transaction.status)
    #     }

    # return render_template('checkouts/show.html', transaction=transaction, result=result)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4567, debug=True)
