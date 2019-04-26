from django.db import migrations
from django.conf import settings
import os.path
import csv
from django.core.files import File


def load_candidate_data(apps, schema_editor):
    """read a CSV file full of candidate info and insert them into the datatbase """

    Candidate = apps.get_model ('core', 'Candidate')
    datapath = os.path.join(settings.BASE_DIR, 'initial_data')
    datafile = os.path.join(datapath, 'candidate2.csv')
    with open (datafile) as file:
        reader= csv.DictReader(file)
        for row in reader:
            first_name = row['first_name']
            if Candidate.objects.filter(first_name=first_name).count():
                continue
            candidate = Candidate(
                first_name=row['first_name'],
                last_name=row['last_name'],
                party=row['party'],
                description=row['description'],
                image=row['image']




            )
            candidate.save()









class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [migrations.RunPython(load_candidate_data)]