from cars_shop import forms
from django import forms 
from django.db.models import fields
from cars_shop.models import Comment


class CommentForm(forms.ModelForm):
    class Meta: 
        model = Comment
        fields = ('name', 'email', 'number')