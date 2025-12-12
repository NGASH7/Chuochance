import datetime
from django.db import models
# Create your models here.
FAMILY_STATUS = (
    ('orphan', 'Total Orphan'),
    ('single_parent', 'Single Parent (Without Source of Income)'),
    ('partial_orphan', 'Partial Orphan (Mother/Father Alive) Without Source of Income'),
    ('both_parents', 'Both Parents Alive Without Source of Income'),
)

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
)

AWARD_STATUS = (
    ('pending', 'Pending'),
    ('awarded', 'Awarded'),
    ('not_awarded', 'Not Awarded'),
)


class Period(models.Model):
    """
    Model to store the application period
    -> year
    -> start_date
    -> end_date
    -> budget
    """
    year = models.IntegerField(default=datetime.date.today().year)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    budget = models.PositiveIntegerField()

    def __str__(self):
        return str(self.year)

    @property
    def successful_applicants_count(self):
        """
        Returns the count of the successful applicants
        """
        return self.application_set.filter(award_status='awarded').count()

    @property
    def unsuccessful_applicants_count(self):
        """
        Returns the count of the successful applicants
        """
        return self.application_set.filter(award_status='not_awarded').count()


class Level(models.Model):
    """
    Model to store the school level of the student
    -> name
    -> amount_allocated
    """
    name = models.CharField(max_length=100)
    amount_allocated = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Subcounty(models.Model):
    """
    Model to store subcounties
    -> name
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ward(models.Model):
    """
    Model to store wards
    -> county
    -> ward
    """
    subcounty = models.ForeignKey(Subcounty, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Application(models.Model):
    """
    Model to store applications
    -> full_name
    -> gender
    -> family_status
    -> death_cert_father
    -> death_cert_mother
    -> name_of_guardian
    -> contact_of_guardian
    -> disability_status
    -> disability_description
    -> level
    -> adm_number
    -> class_of_study
    -> subcounty
    -> ward
    -> award_status
    -> recommended
    -> submitted_at

    # Props
    -> score
    """
    user = models.ForeignKey(
        'users.User', related_name='applications', on_delete=models.SET_NULL, null=True, blank=True)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=120)
    id_number = models.CharField(
        max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    family_status = models.CharField(max_length=15, choices=FAMILY_STATUS)
    death_cert_father = models.FileField(
        null=True, blank=True, upload_to='death_certs/')
    death_cert_mother = models.FileField(
        null=True, blank=True, upload_to='death_certs/')
    name_of_guardian = models.CharField(max_length=120)
    contact_of_guardian = models.CharField(max_length=13)
    disability_status = models.BooleanField(default=False)
    disability_registration_number = models.CharField(
        max_length=20, null=True, blank=True)
    disability_description = models.CharField(
        max_length=200, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
    school_name = models.CharField(max_length=120, null=True)
    admission_number = models.CharField(max_length=30)
    class_of_study = models.PositiveSmallIntegerField()
    school_recommendation_letter = models.FileField(
        null=True, blank=True, upload_to='recommendations/')
    subcounty = models.ForeignKey(Subcounty, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    award_status = models.CharField(
        max_length=200, choices=AWARD_STATUS, default='pending')
    recommended = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.full_name)

    @property
    def score(self):
        """
        Determines the score for a given applicant
        """
        first_score, second_score, third_score = 0, 0, 0

        single_death_cert = self.death_cert_father or self.death_cert_mother

        if self.family_status == 'orphan' and self.death_cert_mother and self.death_cert_father:
            first_score = 4
        elif self.family_status == 'partial_orphan' and single_death_cert:
            first_score = 3
        elif self.family_status == 'single_parent':
            first_score = 2
        elif self.family_status == 'both_parents':
            first_score = 1
        else:
            first_score = 0

        if self.gender == 'M':
            second_score = 1
        elif self.gender == 'F':
            second_score = 2
        elif self.gender == 'O':
            second_score = 0
        else:
            second_score = 0

        if self.disability_status == True and self.disability_registration_number:
            third_score = 2
        elif self.disability_status == False:
            third_score = 1
        else:
            third_score = 0

        total_score = first_score + second_score + third_score
        return total_score

    def save(self, *args, **kwargs):
        """
        Overriding the save method
        """
        if self.score > 6:
            self.recommended = True

        super(Application, self).save(*args, **kwargs)
