from django import forms
from django.contrib.auth.hashers import make_password

from patient.models import Patient

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        )
    password_2 = forms.CharField(
        widget=forms.PasswordInput, 
        label="Confirm Password", 
        required=True, 
        error_messages={'required': 'Please confirm your password'})

    class Meta:
        model = Patient
        fields = (
            "username",
            "email",
            "age",
            "gender",
            "height",
            "weight",
            "health_condition_notes",
            "password",
        )

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password != password_2:
            self.add_error("password", "Passwords don't match")
        return cleaned_data

    def save(self, commit=True):
        patient = super(RegisterForm, self).save(commit=False)
        patient.set_password(self.data["password"])
        patient.save()
        return patient

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Patient
        fields = ("email", "password")

    def is_valid(self) -> bool:
        patient = Patient.objects.filter(email=self.data['email']).first()
        if patient:
            if patient.check_password(self.data['password']):
                return True
            else:
                self.add_error("password", "Wrong password")
                return False
        else:
            self.add_error("email", "User doesn't exist")
            return False