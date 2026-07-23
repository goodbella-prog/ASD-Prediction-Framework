import os
import pandas as pd
from django import forms
from .models import Prediction


class PredictionForm(forms.ModelForm):

    contry_of_res = forms.ChoiceField(
        choices=[],
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    class Meta:
        model = Prediction

        exclude = [
            "prediction",
            "created_at",
        ]

        widgets = {

            "age_desc": forms.HiddenInput(),

            "age": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Age"
            }),


            "ethnicity": forms.Select(attrs={
                "class": "form-select"
            }),

            "gender": forms.Select(attrs={
                "class": "form-select"
            }),

            "relation": forms.Select(attrs={
                "class": "form-select"
            }),

            "jaundice": forms.Select(attrs={
                "class": "form-select"
            }),

            "austim": forms.Select(attrs={
                "class": "form-select"
            }),

            "used_app_before": forms.Select(attrs={
                "class": "form-select"
            }),

            "A1_Score": forms.Select(attrs={
                "class": "form-select"
            }),

            "A2_Score": forms.Select(attrs={
                "class": "form-select"
            }),

            "A3_Score": forms.Select(attrs={
                "class": "form-select"
            }),

            "A4_Score": forms.Select(attrs={
                "class": "form-select"
            }),

            "A5_Score": forms.Select(attrs={
                "class": "form-select"
            }),

            "A6_Score": forms.Select(attrs={
                "class": "form-select"
            }),

            "A7_Score": forms.Select(attrs={
                "class": "form-select"
            }),

            "A8_Score": forms.Select(attrs={
                "class": "form-select"
            }),

            "A9_Score": forms.Select(attrs={
                "class": "form-select"
            }),

            "A10_Score": forms.Select(attrs={
                "class": "form-select"
            }),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["age_desc"].initial = "18 and more"
        csv_path = os.path.join(
            os.path.dirname(__file__),
            "ml",
            "train.csv"
        )

        # Load country list from CSV and populate choices
        try:
            df = pd.read_csv(csv_path, sep="\t")
        except Exception:
            # fallback to comma separator
            df = pd.read_csv(csv_path)

        countries = sorted(
            df["contry_of_res"].dropna().unique()
        )

        self.fields["contry_of_res"].choices = [
            ("", "Select Country")
        ] + [
            (country, country) for country in countries
        ]
       