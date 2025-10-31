# voter_analytics/models.py
# auther: Chonghao Chen (alvenie@bu.edu), 10/31/2025
# description: The models.py file specific to the voter analytics app

from django.db import models
import csv
from datetime import datetime

# Create your models here.

class Voter(models.Model):
    # Personal Info
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    
    # Address Info
    street_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=200)
    apt_number = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    
    # Voter Info
    dob = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    party_affiliation = models.CharField(max_length=2) # e.g., 'D ', 'U ', 'R '
    precinct_number = models.CharField(max_length=10)
    
    # Election Participation
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    
    # Score
    voter_score = models.IntegerField()

    def __str__(self):
        """String representation of the Voter model."""
        return f"{self.first_name} {self.last_name} ({self.party_affiliation})"
    
# ... (at the end of voter_analytics/models.py)

def load_data(file_path='newton_voters.csv'):
    """
    Loads voter data from a CSV file into the Voter model.
    Assumes the CSV file is in the same directory as manage.py.
    """
    
    # Helper function to parse dates, returning None if invalid
    def parse_date(date_str):
        if not date_str:
            return None
        try:
            # Adjust the format '%m/%d/%Y' if your CSV is different
            return datetime.strptime(date_str, '%m/%d/%Y').date()
        except ValueError:
            return None

    # Helper function to parse 'X' into True
    def parse_bool(val):
        return val.strip().upper() == 'X'

    # Clear existing data to avoid duplicates on re-run
    print("Deleting old voter data...")
    Voter.objects.all().delete()

    print("Loading new data from CSV...")
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        voters_to_create = []
        for row in reader:
            voters_to_create.append(
                Voter(
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    street_number=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apt_number=row['Residential Address - Apartment Number'],
                    zip_code=row['Residential Address - Zip Code'],
                    dob=parse_date(row['Date of Birth']),
                    registration_date=parse_date(row['Date of Registration']),
                    party_affiliation=row['Party Affiliation'], # Stores 'U ', 'D ', etc.
                    precinct_number=row['Precinct Number'].strip(), # Use .strip() to clean whitespace,
                    
                    v20state=parse_bool(row['v20state']),
                    v21town=parse_bool(row['v21town']),
                    v21primary=parse_bool(row['v21primary']),
                    v22general=parse_bool(row['v22general']),
                    v23town=parse_bool(row['v23town']),
                    
                    voter_score=int(row['voter_score'])
                )
            )
        
        # Use bulk_create for much faster loading
        Voter.objects.bulk_create(voters_to_create)
        print(f"Successfully loaded {len(voters_to_create)} voters.")