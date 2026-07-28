import os
import pandas as pd
from django import forms
from .models import Prediction


class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction

        exclude = [
            "prediction",
            "created_at",
        ]

        widgets = {
            "age": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your age"
            }),

            "gender": forms.Select(attrs={"class": "form-select"}),

            "ethnicity": forms.Select(attrs={"class": "form-select"}),

            "contry_of_res": forms.Select(attrs={
                "class": "form-select"
            }),

            "jaundice": forms.Select(attrs={"class": "form-select"}),

            "austim": forms.Select(attrs={"class": "form-select"}),

            "used_app_before": forms.Select(attrs={"class": "form-select"}),

            "relation": forms.Select(attrs={"class": "form-select"}),

            "result": forms.HiddenInput(),

            "age_desc": forms.HiddenInput(),

            "A1_Score": forms.RadioSelect(),
            "A2_Score": forms.RadioSelect(),
            "A3_Score": forms.RadioSelect(),
            "A4_Score": forms.RadioSelect(),
            "A5_Score": forms.RadioSelect(),
            "A6_Score": forms.RadioSelect(),
            "A7_Score": forms.RadioSelect(),
            "A8_Score": forms.RadioSelect(),
            "A9_Score": forms.RadioSelect(),
            "A10_Score": forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["age_desc"].initial = "18 and more"

        csv_path = os.path.join(
            os.path.dirname(__file__),
            "ml",
            "train.csv"
        )

        # Read CSV
        try:
            df = pd.read_csv(csv_path, sep=None, engine="python")
        except Exception as e:
            print(e)
            return


        countries = sorted(
            df.iloc[:, 16]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )
        

        country_choices = [
    ("", "Select Country")
] + [(c, c) for c in countries]

        self.fields["contry_of_res"].choices = country_choices
        self.fields["contry_of_res"].widget.choices = country_choices