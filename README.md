# Demo app requirements

Here are the requirments for braintree: 
Use Cases: 
- user wants to buy one product in USD 
- user wants to buy one product in EUR 
- user wants to buy one product with a quantity of 2 or more in USD 
- user cancels the buying process 
- user able to buy extra product on thank you page without submitting credit card info again 
- user enter a different mail and/or address information on the payment service provider site 
- refunds the sales order completely 
- refund the sales order partially

Requirements: 
- please implement every use case from above 
- use flask as a web framework 
- unit tests needed 
- you can use the offical SDK or a well supported opensource SDK if there is one. If not, please build one first. 
- the HTML part should be very minimalistic. No theme required. But you can use one if you want. 
- you can use any DB you want if you need one. MongoDB would be nice. 


Deliverables: 
- I need a process diagram how the communication with the payment method provider works (you can link the original picture/page if there is one) 
- instructions on how to run the project locally 
- deployment instructions



# Braintree Flask Example
[![Build Status](https://travis-ci.org/braintree/braintree_flask_example.svg?branch=master)](https://travis-ci.org/braintree/braintree_flask_example)

An example Braintree integration for python in the Flask framework.

## Setup Instructions

1. Install requirements:
  ```sh
  pip install -r requirements.txt
  ```

2. Copy the contents of `example.env` into a new file named `.env` and fill in your Braintree API credentials. Credentials can be found by navigating to Account > My User > View Authorizations in the Braintree Control Panel. Full instructions can be [found on our support site](https://articles.braintreepayments.com/control-panel/important-gateway-credentials#api-credentials).

3. Start server:
  ```sh
  python app.py
  ```

## Deploying to Heroku

You can deploy this app directly to Heroku to see the app live. Skip the setup instructions above and click the button below. This will walk you through getting this app up and running on Heroku in minutes.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/braintree/braintree_flask_example&env[BT_ENVIRONMENT]=sandbox)

## Running tests

Unit tests do not make API calls to Braintree and do not require Braintree credentials. You can run this project's unit tests by calling `python test_app.py` on the command line.

## Testing Transactions

Sandbox transactions must be made with [sample credit card numbers](https://developers.braintreepayments.com/reference/general/testing/python#credit-card-numbers), and the response of a `Transaction.sale()` call is dependent on the [amount of the transaction](https://developers.braintreepayments.com/reference/general/testing/python#test-amounts).

## Pro Tips

- The `application.cfg.example` contains an `APP_SECRET_KEY` setting. Even in development you should [generate your own custom secret key for your app](http://flask.pocoo.org/docs/0.10/quickstart/#sessions).

## Help

 * Found a bug? Have a suggestion for improvement? Want to tell us we're awesome? [Submit an issue](https://github.com/braintree/braintree_flask_example/issues)
 * Trouble with your integration? Contact [Braintree Support](https://support.braintreepayments.com/) / support@braintreepayments.com
 * Want to contribute? [Submit a pull request](https://help.github.com/articles/creating-a-pull-request)

## Disclaimer

This code is provided as is and is only intended to be used for illustration purposes. This code is not production-ready and is not meant to be used in a production environment. This repository is to be used as a tool to help merchants learn how to integrate with Braintree. Any use of this repository or any of its code in a production environment is highly discouraged.
