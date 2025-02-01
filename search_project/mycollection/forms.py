from django import forms
from .models import MyCollection
from .models import CollectionCategory

class MyCollectionForm(forms.ModelForm):
    collection_category = forms.ModelChoiceField(
        queryset=CollectionCategory.objects.all(),
        empty_label="分類なし",
        required=False,
        blank=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'コレクション名'})
    )
    image_path = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = MyCollection
        fields = (
            'name',
            'description',
            'get_date',
            'price',
            'collection_category',
            'image_path',
            'memo',
        )
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'コレクション説明（詳細情報）'}),
            'get_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '価格', 'min': 0}),
            'memo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'メモ'})
        }