from django import forms
from .models import UserRegister


class SignupForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password'
        })
    )

    class Meta:

        model = UserRegister

        fields = ['name', 'email', 'mobile', 'password']

        widgets = {

            'name': forms.TextInput(attrs={
                'placeholder': 'Enter Full Name'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter Email'
            }),

            'mobile': forms.TextInput(attrs={
                'placeholder': 'Enter Mobile Number'
            }),

        }


class LoginForm(forms.Form):

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput()
    )


from django import forms
from .models import Paint

class PaintForm(forms.ModelForm):

    class Meta:
        model = Paint
        fields = [ 'image', 'price', 'category']

        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
    
        }

