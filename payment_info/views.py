import datetime
import json
import random

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from payment_info.models import CardDetail, Result
from rest_framework.response import Response
import requests


class PaymentInfo(APIView):

    def post(self, request):
        try:
            data = request.data
            amount = int(data["amount"])
            currency = data["currency"]
            # codes = requests.get('https://openexchangerates.org/api/currencies.json')
            # codes = json.loads(codes.text)
            # if currency not in codes.keys():
            #     raise BaseException("Currency is not valid")
            card_type = data["type"]
            if card_type not in ["creditcard","debitcard"]:
                raise BaseException("Card Invalid")
            card = data["card"]
            number = card["number"]
            expiration_month = int(card["expirationMonth"])
            if expiration_month not in [i for i in range(1,13)]:
                raise BaseException("Month on the card is not valid")
            expiration_year = int(card["expirationYear"])
            d1 = datetime.date(expiration_year, expiration_month, 1)
            d2 = datetime.date.today()
            if d1 < d2:
                raise BaseException("Card expired")
            cvv = int(card["cvv"])
            authorization_code = "SDSD" + str(random.randint(10000000, 99999999))
            card_detail = CardDetail.objects.create(number=number, expirationMonth=expiration_month,
                                                    expirationYear=expiration_year, cvv=cvv, type=card_type,
                                                    amount=amount, currency=currency, authorization_code=authorization_code)
            card_detail.save()
            r = {"amount": str(amount), "currency": currency, "type": card_type, "card": {"number": number},
                 "status": "success", "authorization_code": authorization_code,
                 "time": datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")}
            result = Result.objects.create(response=str(r), status_code=200)
            result.save()
            return Response(r, status=200)

        except BaseException as e:
            r = {"Message": "API authentication failed", "Error": str(e)}
            result = Result.objects.create(response=str(r), status_code=status.HTTP_403_FORBIDDEN)
            result.save()
            return Response(r, status=status.HTTP_403_FORBIDDEN,
                            headers=None)
        except Exception as e:
            r = {"Message": "API authentication failed", "Error": str(e)}
            result = Result.objects.create(response=str(r), status_code=status.HTTP_403_FORBIDDEN)
            result.save()
            return Response(r, status=status.HTTP_403_FORBIDDEN,
                            headers=None)



