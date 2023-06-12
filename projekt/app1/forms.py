# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Korisnik, Uloga, Predmet, Upis

class KorisnikRegistrationForm(UserCreationForm):
    uloga = forms.ModelChoiceField(queryset=Uloga.objects.all(), empty_label=None)
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    status = forms.ChoiceField(choices=Korisnik.STATUS)

    class Meta:
        model = Korisnik
        fields = ('username', 'email', 'password1', 'password2', 'uloga', 'status')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if 'email' in self.changed_data and Korisnik.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if 'username' in self.changed_data and Korisnik.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return username

    

class PredmetForm(forms.ModelForm):
    sem_redovni = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(1, 7)])
    sem_izvanredni = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(1, 9)])

    class Meta:
        model = Predmet
        fields = '__all__'

class EditStudentForm(KorisnikRegistrationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uloga'].disabled = True

class EditProfessorForm(KorisnikRegistrationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uloga'].disabled = True
        self.fields['status'].disabled = True

class UpisForm(forms.ModelForm):
    class Meta:
        model = Upis
        fields = ['predmet', 'status']
        widgets = {
            'predmet': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }
