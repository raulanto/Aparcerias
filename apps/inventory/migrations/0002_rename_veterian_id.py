from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicalcheckup',
            old_name='veterian_id',
            new_name='veterinarian_id',
        ),
    ]
