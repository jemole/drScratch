from django import forms

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
