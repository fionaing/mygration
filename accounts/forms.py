from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe

# Customizes how errors w/ password/username are shown
class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert"> {e}</div>' for e in self]))

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            # remove help text for all fields
            self.fields[fieldname].help_text = None
            # bootstrap class that improves fields
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
