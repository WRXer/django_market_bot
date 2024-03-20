import yookassa
from yookassa import Payment
import uuid
import os


yookassa.Configuration.account_id = os.getenv("ACCOUNT_ID")
yookassa.Configuration.secret_key = os.getenv("SECRET_KEY_YOOMONEY")

def create(amount, chat_id):
    id_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/TestWorkingToBot"
        },
        "capture": True,
        "metadata": {
            "chat_id": chat_id
        },
        "description": "Описание товара"
    }, id_key)

    return payment.confirmation.confirmation_url, payment.id


def check(payment_id):
    payment = Payment.find_one(payment_id)
    if payment.status == "succeeded":
        return payment.metadata
    else:
        return False
