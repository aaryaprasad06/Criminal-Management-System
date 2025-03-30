from django.db import models
from django.utils import timezone

class Criminal(models.Model):
    criminal_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    fingerprint_id = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='criminal_photos/')
    status = models.CharField(max_length=20)  # Active, In Custody, Released, etc.
    created_at = models.DateTimeField(default=timezone.now)


class Crime(models.Model):
    crime_id = models.AutoField(primary_key=True)
    criminal = models.ForeignKey(Criminal, on_delete=models.CASCADE)
    crime_type = models.CharField(max_length=100)
    description = models.TextField()
    date_committed = models.DateField()
    location = models.CharField(max_length=200)
    victims = models.IntegerField(default=0)
    weapons_used = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20)  # Open, Closed, Under Investigation

class Arrest(models.Model):
    arrest_id = models.AutoField(primary_key=True)
    criminal = models.ForeignKey(Criminal, on_delete=models.CASCADE)
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)
    arrest_date = models.DateTimeField()
    arresting_officers = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    warrant_number = models.CharField(max_length=50, blank=True)

class CaseFile(models.Model):
    case_id = models.AutoField(primary_key=True)
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)
    file_number = models.CharField(max_length=50, unique=True)
    investigating_officer = models.CharField(max_length=100)
    evidence_details = models.TextField()
    witnesses = models.TextField(blank=True)
    court_dates = models.TextField(blank=True)
    status = models.CharField(max_length=20)  # Active, Closed, Pending