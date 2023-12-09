from apps.credit.models import Credit, CreditDescription


class CreditDescriptionService:
    model = CreditDescription

    def get_descriptions(self):
        return self.model.objects.all()


class CreditService:
    model = Credit

    def get_descriptions(self):
        return self.model.objects.all()