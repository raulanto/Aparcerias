from django.contrib.auth.models import BaseUserManager


class SharecropperManager(BaseUserManager):
    """
    Manager que combina la creación de usuarios, el Soft Delete
    y el filtro base para multi-tenancy.
    """

    def get_queryset(self):
        # Aseguramos que las consultas por defecto no traigan eliminados lógicamente
        return super().get_queryset().filter(deleted_at__isnull=True)

    def create_user(self, email, legal_name, type, company=None, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico válido.")

        # Validamos que tenga empresa, A MENOS que sea un superusuario global
        if not company and not extra_fields.get('is_superuser'):
            raise ValueError("Un usuario regular debe estar vinculado a una Empresa (Tenant).")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            legal_name=legal_name,
            type=type,
            company=company,  # Actualizado al nombre en inglés
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, legal_name, type, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('state', 'Activo')  # Actualizado de 'estado' a 'state'

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        # Pasamos company=None, la validación en create_user ahora lo permitirá por ser superusuario
        return self.create_user(
            email=email,
            legal_name=legal_name,
            type=type,
            company=None,
            password=password,
            **extra_fields
        )