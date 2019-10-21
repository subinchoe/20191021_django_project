from django import forms
from .models import Question, Comment


class QuestionForm(forms.ModelForm):
    li = [
        ('식물', '식물'),
        ('동물', '동물'),
        ('영화', '영화'),
        ('음악', '음악'),
        ('드라마', '드라마'),
    ]
    kind = forms.CharField(widget =forms.Select(choices=li))
    
    class Meta:
        model = Question
        fields = ('kind', 'title', 'content',)


class CommentForm(forms.ModelForm):
    choices = [(1, '추천'), (2, '비추천')]
    pick = forms.ChoiceField(choices=choices , widget=forms.RadioSelect)
    class Meta:
        model = Comment
        fields = ('pick', 'content',)
