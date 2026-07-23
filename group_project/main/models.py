from django.db import models

YES_NO_SCORE = [
    (1, "Yes"),
    (0, "No"),
]


class Prediction(models.Model):

    GENDER_CHOICES = [
        ("m", "Male"),
        ("f", "Female"),
    ]

    YES_NO = [
        ("yes", "Yes"),
        ("no", "No"),
    ]

    ETHNICITY_CHOICES = [
        ("?", "?"),
        ("White-European", "White-European"),
        ("Middle Eastern ", "Middle Eastern"),
        ("Pasifika", "Pasifika"),
        ("Black", "Black"),
        ("Others", "Others"),
        ("Hispanic", "Hispanic"),
        ("Asian", "Asian"),
        ("Turkish", "Turkish"),
        ("South Asian", "South Asian"),
        ("Latino", "Latino"),
        ("others", "others"),
    ]

    AGE_DESC_CHOICES = [
        ("18 and more", "18 and more"),
    ]

    RELATION_CHOICES = [
        ("Self", "Self"),
        ("Parent", "Parent"),
        ("Relative", "Relative"),
        ("Health care professional", "Health Care Professional"),
        ("Others", "Others"),
        ("?", "Unknown"),
    ]

    A1_Score = models.IntegerField(choices=YES_NO_SCORE)
    A2_Score = models.IntegerField(choices=YES_NO_SCORE)
    A3_Score = models.IntegerField(choices=YES_NO_SCORE)
    A4_Score = models.IntegerField(choices=YES_NO_SCORE)
    A5_Score = models.IntegerField(choices=YES_NO_SCORE)
    A6_Score = models.IntegerField(choices=YES_NO_SCORE)
    A7_Score = models.IntegerField(choices=YES_NO_SCORE)
    A8_Score = models.IntegerField(choices=YES_NO_SCORE)
    A9_Score = models.IntegerField(choices=YES_NO_SCORE)
    A10_Score = models.IntegerField(choices=YES_NO_SCORE)

    age = models.FloatField()

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    ethnicity = models.CharField(
        max_length=100,
        choices=ETHNICITY_CHOICES
    )

    jaundice = models.CharField(max_length=3, choices=YES_NO)

    austim = models.CharField(max_length=3, choices=YES_NO)

    contry_of_res = models.CharField(max_length=100)

    used_app_before = models.CharField(max_length=3, choices=YES_NO)

    result = models.FloatField()

    age_desc = models.CharField(
        max_length=50,
        choices=AGE_DESC_CHOICES,
        default="18 and more"
    )

    relation = models.CharField(
        max_length=100,
        choices=RELATION_CHOICES
    )

    prediction = models.CharField(max_length=30, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prediction