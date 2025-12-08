from datetime import datetime
from flask import current_app, url_for
from app import db
from app.models import PaymentStatus
from app.models.payment import MomoPayment, PaymentMethod, Payment
import requests, uuid

from app.utils import momo_sign

class PaymentStrategy:
    def process(self, order, **kwargs):
        raise NotImplementedError

class MomoStrategy(PaymentStrategy):
    def process(self, order, **kwargs):
        redirect_url = url_for('customer.momo_return', _external=True)
        ipn_url = url_for('customer.momo_return', _external=True)

        result = send_momo_request(order, redirect_url, ipn_url)

        if result.get("error"):
            raise Exception(f"Lỗi MoMo: {result.get('error')}")

        payment = MomoPayment(
            order_id=order.id,
            amount=order.total_amount,
            status=PaymentStatus.PENDING,
            request_id=result.get("requestId"),
            pay_url=result.get("payUrl")
        )

        return payment

class CashStrategy(PaymentStrategy):
    def process(self, order, **kwargs):
        pass

def process_order_payment(order, strategy: PaymentStrategy, **kwargs):
    payment = strategy.process(order, **kwargs)
    db.session.add(payment)
    db.session.commit()
    return payment

def send_momo_request(order, return_url, ipn_url):
    cfg = current_app.config

    partner_code = cfg.get("MOMO_PARTNER_CODE")
    access_key = cfg.get("MOMO_ACCESS_KEY")
    secret_key = cfg.get("MOMO_SECRET_KEY")
    endpoint = cfg.get("MOMO_ENDPOINT")
    request_type = cfg.get("MOMO_REQUEST_TYPE")

    timestamp = int(datetime.now().timestamp())
    momo_order_id = f"{order.id}_{timestamp}"
    request_id = str(uuid.uuid4())
    amount = str(int(order.total_amount))
    order_info = f"Thanh toan don hang #{order.id}"
    extra_data = ""

    raw_signature = (
        f"accessKey={access_key}"
        f"&amount={amount}"
        f"&extraData={extra_data}"
        f"&ipnUrl={ipn_url}"
        f"&orderId={momo_order_id}"
        f"&orderInfo={order_info}"
        f"&partnerCode={partner_code}"
        f"&redirectUrl={return_url}"
        f"&requestId={request_id}"
        f"&requestType={request_type}"
    )

    signature = momo_sign(secret_key, raw_signature)

    payload = {
        "partnerCode": partner_code,
        "partnerName": "CAFE",
        "storeId": "CAFERestaurant",
        "requestId": request_id,
        "amount": amount,
        "orderId": momo_order_id,
        "orderInfo": order_info,
        "redirectUrl": return_url,
        "ipnUrl": ipn_url,
        "lang": "vi",
        "extraData": extra_data,
        "requestType": request_type,
        "signature": signature,
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=20)
        res_json = response.json()

        if res_json.get("resultCode") == 0:
            return {
                "payUrl": res_json.get("payUrl"),
                "requestId": request_id,
                "error": None
            }
        else:
            return {
                "payUrl": None,
                "error": res_json.get("message")
            }
    except Exception as e:
        return {"payUrl": None, "error": str(e)}


def get_payment_by_id_and_method_and_status(id, method, status):
    return Payment.query.filter_by(order_id=id, method=method, status=status).first()