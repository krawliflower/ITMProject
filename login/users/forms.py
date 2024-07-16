from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from blog.models import Incident

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    username = forms.CharField(max_length = 20, help_text = "Maximum of 20 characters.")
    
    ROLE_CHOICES = [
        ('tutor', 'Tutor'),
        ('tutee', 'Tutee'),
    ]
    
    role = forms.ChoiceField(choices = ROLE_CHOICES, widget = forms.RadioSelect)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'role', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("An account is already associated with this email.")
        return email

class TutorForm(forms.Form):
    subject_choices = [
        ('MATH 31.1', 'MATH 31.1'),
        ('LAS 21', 'LAS 21'),
        ('MATH 31.2', 'MATH 31.2'),
        ('DECSC 22', 'DECSC 22'),
        ('ITMGT 25.03', 'ITMGT 25.03'),
        ('MATH 31.3', 'MATH 31.3'),
        ('ACCT 115', 'ACCT 115'),
        ('LLAW 113', 'LLAW 113'),
        ('MATH 70.1', 'MATH 70.1'),
        ('ECON 110', 'ECON 110'),
        ('ACCT 125', 'ACCT 125'),
        ('LLAW 115', 'LLAW 115'),
        ('MATH 61.2', 'MATH 61.2'),
        ('DECSC 25', 'DECSC 25'),
        ('ECON 121', 'ECON 121'),
        ('FINN 115', 'FINN 115'),
        ('QUANT 121', 'QUANT 121'),
        ('QUANT 162', 'QUANT 162'),
        ('LAS 111', 'LAS 111'),
        ('MKTG 111', 'MKTG 111'),
        ('QUANT 163', 'QUANT 163'),
        ('LAS 123', 'LAS 123'),
        ('QUANT 192', 'QUANT 192'),
        ('LAS 120', 'LAS 120'),
        ('LAS 140', 'LAS 140'),
        ('OPMAN 125', 'OPMAN 125'),
        ('QUANT 164', 'QUANT 164'),
        ('QUANT 199', 'QUANT 199'),
        ('LAS 197.10', 'LAS 197.10'),
    ]
    subject = forms.MultipleChoiceField(
        choices = subject_choices,
        widget = forms.CheckboxSelectMultiple,
        help_text = "Select all that apply."
    )
    facebook_username = forms.CharField(max_length=50)
    contact_number = forms.CharField(max_length=50)

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['title', 'description', 'location', 'pictures']

class IncidentUpdateForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['title', 'description', 'location', 'pictures']

    def __init__(self, *args, **kwargs):
        initial_picture = kwargs.pop('initial_picture', None)
        super().__init__(*args, **kwargs)
        self.initial_picture = initial_picture

    def clean_pictures(self):
        if self.cleaned_data['pictures'] != self.initial_picture:
            self.instance.custom_picture_update_method(self.initial_picture)
        return self.cleaned_data['pictures']