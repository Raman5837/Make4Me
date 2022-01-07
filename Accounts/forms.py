from phonenumber_field.modelfields import PhoneNumberField
from django import forms
from .models import Account, UserProfile


class SignupForm(forms.ModelForm):

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password'}))
    confirmPassword = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Re-Enter Your Password'}))
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)
    phone_numer = PhoneNumberField()

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'phone_number', 'email', 'password']

    # to check password == confirmPassword or not ?

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        confirmPassword = cleaned_data.get('confirmPassword')

        if len(password) < 8:
            raise forms.ValidationError(
                'Password Must Be At Least 8 Characters.')

        if password != confirmPassword:
            raise forms.ValidationError(
                'Password And Confirm Password Does Not Match!')

    # function to apply custom attrs (css styles and all) to all of the fields of SignUp Form
    def __init__(self, *args, **kwargs):

        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your E-mail Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Your Phone Number'

        # to apply custom css in all of the fields
        # for field in self.fields:
        #     self.fields[field].widget.attrs['class'] = 'Your CSS Styling Name'


class UserAccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'gender']


class UserProfileForm(forms.ModelForm):

    profilePicture = forms.ImageField(required=False, error_messages={
                                      'invalid': ("Image Files Only")}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ['addressLine_1', 'addressLine_2',
                  'profilePicture', 'city', 'state', 'pincode', 'country']
