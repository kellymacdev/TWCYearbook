import gspread
from google.oauth2.service_account import Credentials
from django.core.management.base import BaseCommand
from network.models import Graduate  # change to your model path
import csv

COLUMN_MAPPING = {
            "Name and surname": 'name',
            "Maiden name if relevant": 'maiden_name',
            "Pronouns": 'pronouns',
            "Current city": 'city',
            "What industry are you in? ": 'industry',
            "What have you been up to in the past 10 years? (general description, 500 character limit)": 'gen_description',
            "What things do you like to do now? (Hobbies etc.) ": 'hobbies',
            "What things does current you do that high school you would be shocked by?": 'q1',
            "What's your favourite thing about yourself?": 'q2',
            "What's something you're proud to have done in the past 10 years?": 'q3',
            "What's something you've learnt since high school?": 'q4',
            "What do you miss most about high school?": 'q5',
            "3 things you're grateful for?": 'q6',
            "What's your idea of a perfect weekend?": 'q7',
            "What's something you could speak about for hours?": 'q8',
            "What's your favourite song of the moment?": 'q9',
            "Leave a fun quote/life tip/piece of advice/saying/TV recommendation etc.": 'q10',
            "How can people contact you if they want to say hi? (Instagram, cellphone number, email etc.)": 'contact',
            "How many years did you spend schooling after 2015 (Uni, College etc.)?": 'school_years',
            "How many countries have you lived in in the past 10 years? (3 months +)": 'countries',
            "How many jobs have you worked?": 'jobs',
            "Have any tattoos?": 'tattoos',
            "Are you married?": 'married',
            "Had any babies?": 'babies',
            "For Zaza": 'for_zaza',
            "For Linda": 'for_linda'
        }


class Command(BaseCommand):
    help = 'Import students and their answers from Google Sheet'

    def handle(self, *args, **kwargs):
        with open('graduates.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                graduate_data = {}
                for csv_col, model_field in COLUMN_MAPPING.items():
                    value = row.get(csv_col, '').strip()

                    # Convert numeric fields
                    if model_field in ['school_years', 'countries', 'jobs', 'tattoos', 'babies']:
                        value = int(value) if value not in ['', None] else None

                    # Convert boolean field
                    if model_field == 'married':
                        value = True if value.lower() in ['yes', 'true', '1'] else False

                    graduate_data[model_field] = value

                graduate, created = Graduate.objects.update_or_create(
                    name=graduate_data['name'],  # unique key
                    defaults=graduate_data
                )

                if created:
                    print(f"Created: {graduate.name}")
                else:
                    print(f"Updated: {graduate.name}")

            print("CSV import finished!")