from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    @staticmethod
    def _normalize_name(self, name):
        return name.lower()

    @staticmethod
    def _normalize_identifier(self, passport_identifier):
        return passport_identifier.upper()

    def _create_user(self, email, password, first_name, last_name, passport_identifier, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        if not password:
            raise ValueError("The Password must be set")
        if not first_name:
            raise ValueError("The First Name must be set")
        if not last_name:
            raise ValueError("The Last Name must be set")
        if not passport_identifier:
            raise ValueError("The Passport Identifier must be set")

        email = self.normalize_email(email)
        first_name = self._normalize_name(first_name)
        last_name = self._normalize_name(last_name)
        passport_identifier = self._normalize_identifier(passport_identifier)
        user = self.model(email=email, first_name=first_name, last_name=last_name,
                          passport_identifier=passport_identifier, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, first_name, last_name, passport_identifier, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'user')

        return self._create_user(email, password, first_name, last_name, passport_identifier, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, passport_identifier, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, first_name, last_name, passport_identifier, **extra_fields)
