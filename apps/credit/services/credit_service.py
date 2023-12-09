from apps.credit.models import Credit, CreditDescription
from utils.exceptions import NotFound


class CreditDescriptionService:
    model = CreditDescription

    def get_descriptions(self):
        return self.model.objects.all()

    def get_with_duration(self, duration):
        return self.model.objects.filter(duration_in_month=duration)

    def get_with_payment(self, payment):
        return self.model.objects.filter(payment_type=payment)

    def get_credit_rate(self, duration, payment):
        try:
            return float(self.model.objects.filter(duration_in_month=duration, payment_type=payment).first().rate_index)
        except Exception:
            raise NotFound("Not valid credit description")


class CreditService:
    model = Credit

    def get_descriptions(self):
        return self.model.objects.all()