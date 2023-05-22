from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Webpage


class WebpageForm(forms.ModelForm):
    class Meta:
        model = Webpage
        fields = ['title', 'content']
        widgets = {
            'content': CKEditorUploadingWidget(),
        }
