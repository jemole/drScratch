from django import forms
from models import Organization, OrganizationHash

class UploadFileForm(forms.Form):
	filename = forms.CharField(max_length=50)

class UserForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50)

class NewUserForm(forms.Form):
	nickname = forms.CharField(max_length=50)
	emailUser = forms.CharField(max_length=50)
	passUser = forms.CharField(max_length=50)



class UrlForm(forms.Form):
	urlProject = forms.CharField(max_length=80)

class UpdateForm(forms.Form):
	newPass = forms.CharField(max_length=50)
	newEmail = forms.CharField(max_length=50)
#	choiceAvatar = forms.ChoiceField(choices=AVATAR_CHOICES, widget=forms.RadioSelect()

class TeacherForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)  
    hashkey = forms.CharField(max_length=50)
    #classroom = forms.CharField(max_length=50)


class OrganizationForm(forms.ModelForm):   
    
    class Meta:
        model = Organization    
    #name = forms.CharField(max_length=50)
    #email = forms.CharField(max_length=50)  
    #password = forms.CharField(max_length=50)
    #hashkey = forms.CharField(max_length=50)

class OrganizationHashForm(forms.ModelForm):
   
    class Meta:
        model = OrganizationHash
