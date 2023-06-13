from django import forms

from product.models import Product


class ProductCreationForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image']     # '__all__'

    def save(self, commit=True):
        new_product = Product.objects.create(
            name=self.cleaned_data.get('name'), # 사용자가 입력한 내용을 clean_name()하고 깨끗해진 값 가져오기
            price=self.cleaned_data.get('price'), # 사용자가 입력한 내용을 clean_price()하고 깨끗해진 값 가져오기
            image=self.cleaned_data.get('image')
        )
        return new_product


class ProductChangeForm(forms.ModelForm):
    name = forms.CharField(label='제품명', widget=forms.TextInput)
    price = forms.IntegerField(label='가격', widget=forms.NumberInput)
    class Meta:
        model = Product
        fields = ['name',  'price', 'image']   # '__all__'
