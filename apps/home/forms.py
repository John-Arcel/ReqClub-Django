
from django import forms
from .models import RunPost


class RunPostForm(forms.ModelForm):

    class Meta:
        model = RunPost

        fields = [
            "title",
            "run_type",
            "description",
            "venue_name",
            "route_distance_km",
            "target_pace",
            "date",
            "start_time",
            "max_runners",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "e.g. Sunday Morning Run"
            }),

            "run_type": forms.Select(attrs={
                "class": "form-input"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-input",
                "rows": 4,
                "placeholder": "Describe your running meetup..."
            }),

            "venue_name": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Meeting location"
            }),

            "route_distance_km": forms.NumberInput(attrs={
                "class": "form-input",
                "step": "0.1",
                "min": "0.1"
            }),

            "target_pace": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "e.g. 6:30/km or Easy Pace"
            }),

            "date": forms.DateInput(attrs={
                "class": "form-input",
                "type": "date"
            }),

            "start_time": forms.TimeInput(attrs={
                "class": "form-input",
                "type": "time"
            }),

            "max_runners": forms.NumberInput(attrs={
                "class": "form-input",
                "min": "1"
            }),
        }
