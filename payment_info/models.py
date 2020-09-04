from django.db import models


class CardDetail(models.Model):
    number = models.CharField(max_length=30, blank=None, primary_key=True)
    Month_CHOICES = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
        ("11", "11"),
        ("12", "12")
    )
    expirationMonth = models.IntegerField(blank=None, choices=Month_CHOICES)
    expirationYear = models.IntegerField(blank=None)
    cvv = models.IntegerField(blank=None)
    card_choices = (
        ("debitcard", "debitcard"),
        ("creditcard", "creditcard")

    )
    type = models.CharField(max_length=50, blank=None, choices=card_choices)
    amount = models.IntegerField(default=None)
    currency = models.CharField(max_length=10, default=None)
    authorization_code = models.CharField(max_length=12, default=None)


class Result(models.Model):
    response = models.CharField(max_length=1000)
    status_code = models.IntegerField()




