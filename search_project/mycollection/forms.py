from django import forms
from .models import MyCollection , CollectionCategory , CollectionTag

class CollectionSearchForm(forms.Form):
    collection_category = forms.ModelChoiceField(
        queryset=CollectionCategory.objects.none(),
        empty_label="分類なし",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['collection_category'].queryset = CollectionCategory.objects.filter(user=user)
class MyCollectionForm(forms.ModelForm):
    collection_category = forms.ModelChoiceField(
        queryset=CollectionCategory.objects.none(),
        empty_label="分類なし",
        required=False,
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
    tag = forms.ModelMultipleChoiceField(
        queryset=CollectionTag.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tag-checkbox-group'})
    )
    # ユーザーが登録したカテゴ・タグが表示されるようにする
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['collection_category'].queryset = CollectionCategory.objects.filter(user=user)
            self.fields['tag'].queryset = CollectionTag.objects.filter(user=user)
    class Meta:
        model = MyCollection
        fields = (
            'name',
            'description',
            'get_date',
            'price',
            'collection_category',
            'image_path',
            'tag',
            'memo',
        )
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'コレクション説明（詳細情報）'}),
            'get_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '価格', 'min': 0}),
            'memo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'メモ'})
        }


class CollectionCategoryForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'カテゴリ名'})
    )
    class Meta:
        model = CollectionCategory
        fields = (
            'name',
        )

class CollectionTagForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'タグ名'})
    )
    color_code = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
    )
    class Meta:
        model = CollectionTag
        fields = (
            'name',
            'color_code',
        )