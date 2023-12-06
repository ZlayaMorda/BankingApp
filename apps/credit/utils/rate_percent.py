from apps.credit.services.credit_service import CreditDescriptionService
from apps.credit.services.third_party_api import CreditAPI


class RatePercent:
    third_party_api = CreditAPI()
    service_credit_description = CreditDescriptionService()

    def calculate_rate_percent(self, duration, payment):
        last_refinancing_rate = self.third_party_api.get_last_refinancing_rate()
        credit_rate = self.service_credit_description.get_credit_rate(duration, payment)
        return round(last_refinancing_rate * credit_rate / 100, 2)
