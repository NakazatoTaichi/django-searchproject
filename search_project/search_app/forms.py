from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
        label='検索キーワード',
        max_length=100,  # CharField で max_length が有効です
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '検索したいキーワードを入力'})
    )