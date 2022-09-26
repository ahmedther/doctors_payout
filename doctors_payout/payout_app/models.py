from django.db import models


class DoctorProfile(models.Model):
    doctors_group_choice = [
        ("A", "GROUP A"),
        ("B", "GROUP B"),
        ("C", "GROUP C"),
        ("D", "GROUP D"),
        ("E", "GROUP E"),
    ]

    doctor_status_choice = [
        ("ACTIVE", "DOCTOR IS CURRENTLY WORKING WITH THE ORGANIZATION"),
        ("QUITTED", "DOCTOR HAS LEFT THE ORGANIZATION"),
    ]

    doctors_pr_number = models.CharField(max_length=255, null=True)
    doctors_name = models.CharField(max_length=255, null=True)
    doctors_group = models.CharField(max_length=255, choices=doctors_group_choice)
    doctor_status = models.CharField(max_length=255, choices=doctor_status_choice)

    def __str__(self):

        return self.doctors_name + " - " + self.doctors_pr_number


class Transplant(models.Model):
    doctors_name = models.OneToOneField(DoctorProfile, on_delete=models.CASCADE)
    doctors_share = models.FloatField(null=True)
    doctors_department = models.CharField(max_length=255, null=True)

    def __str__(self):

        return (
            self.doctors_name.doctors_name
            + " - "
            + str(self.doctors_share)
            + " - "
            + self.doctors_department
        )
