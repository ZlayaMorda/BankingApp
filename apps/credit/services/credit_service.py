from apps.credit.models import Credit, CreditDescription


class CreditDescriptionService:
    model = CreditDescription

    def get_descriptions(self):
        return self.model.objects.all()

    def get_with_duration(self, duration):
        return self.model.objects.filter(duration_in_month=duration)

    def get_with_payment(self, payment):
        return self.model.objects.filter(payment_type=payment)


class CreditService:
    model = Credit

    def get_descriptions(self):
        return self.model.objects.all()