from django.db import models
#import datetime
#from datetime import date

def get_overall_payment_amount():
    agg = Payment.objects.aggregate(models.Sum("amount"))
    return agg["amount__sum"]

def who_is_next():
    blame_user = None
    minimum = 99999
    for user in User.objects.all():
        if user.get_saldo() < minimum:
            minimum = user.get_saldo()
            blame_user = user
    return blame_user
        

class User(models.Model):
    name = models.CharField(max_length=100)

    def get_payment_amount(self):
        agg = Payment.objects.filter(from_user=self).aggregate(models.Sum("amount"))
        if agg["amount__sum"]==None:
            return 0
        else:
            return agg["amount__sum"]
    
    def get_debt_amount(self):
        sum = 0
        for payment in Payment.objects.filter(payment_for_user__user=self):
            sum += payment.amount / len(payment.payment_for_user_set.all())
        return sum

    def get_saldo(self):
        return self.get_payment_amount() - self.get_debt_amount()

    def __str__(self):
        return self.name


class Payment(models.Model):
    from_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    amount = models.FloatField()
    datetime = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def for_users(self):
        users = []
        for user_payment in self.payment_for_user_set.all():
            users.append(user_payment.user)

    def for_users_string(self):
        usernames = []
        for user_payment in self.payment_for_user_set.all():
            usernames.append(user_payment.user.name)
        return ", ".join(usernames)

    def __str__(self):
        return f"Payment from {self.from_user.name}, amount: {self.amount}, for: {self.for_users_string()}"


class Payment_For_User(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    payment = models.ForeignKey(to=Payment, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.payment}, for: {self.user.name}"
    

