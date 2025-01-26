from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mercadopago
import os
import ssl
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# SSL context configuration
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('path/to/cert.pem', 'path/to/key.pem')


sdk = mercadopago.SDK("APP_USR-4064752143833964-012519-58b2a8dc21995e016c6fe024c3984958-96531112")

# Configure Mercado Pago credentials
#mp = mercadopago.SDK("APP_USR-4419840842819511-121317-8c522deb54aff8ea290465f557bcdf0b-96531112")

@app.route('/')
def checkout_page():
    return render_template('checkout.html')

@app.route('/process_payment', methods=['POST'])
def process_payment():
    payment_data = {
        "transaction_amount": float(request.form['transaction_amount']),
        "token": request.form['token'],
        "description": request.form['description'],
        "installments": int(request.form['installments']),
        "payment_method_id": request.form['payment_method_id'],
        "payer": {
            "email": request.form['email'],
            "identification": {
                "type": request.form['doc_type'],
                "number": request.form['doc_number']
            }
        }
    }

    payment_response = sdk.payment().create(payment_data)
    
    return jsonify(payment_response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)