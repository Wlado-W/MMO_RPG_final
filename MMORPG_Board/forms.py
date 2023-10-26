from django import forms
from .models import Post, Response

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        self.setup_labels()

    def setup_labels(self):
        pass

class PostForm(BaseForm):
    class Meta:
        model = Post
        widgets = {'title': forms.TextInput(attrs={'size': '100'})}
        fields = ('category', 'title', 'text',)

    def setup_labels(self):
        self.fields['category'].label = "Категория:"
        self.fields['title'].label = "Заголовок"
        self.fields['text'].label = "Текст объявления:"

class RespondForm(BaseForm):
    class Meta:
        model = Response
        fields = ('text',)

    def setup_labels(self):
        self.fields['text'].label = "Текст отклика:"

class ResponsesFilterForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(ResponsesFilterForm, self).__init__(*args, **kwargs)
        self.fields['title'] = forms.ModelChoiceField(
            label='Объявление',
            queryset=Post.objects.filter(author_id=user.id).order_by('-dateCreation').values_list('title', flat=True),
            empty_label="Все",
            required=False
        )
        self.fields['title'].label = "Объявление"
