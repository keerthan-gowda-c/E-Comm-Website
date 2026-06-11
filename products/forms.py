from django import forms

from .models import Product, ProductImage, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']
        widgets = {
            'title' : forms.TextInput(attrs = {
                'class' : 'form-control w-50 align-item-center',
                'placeholder' : 'Category Title'
            })
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title','desc','category','thumbnail','price','stock']
        widgets = {
            'title' : forms.TextInput(attrs = {
                'class' : 'form-control w-50 align-item-center',
                'placeholder' : 'Product Title'
            }),
            'desc' : forms.Textarea(attrs = {
                'class' : 'form-control w-50',
                'placeholder' : 'Description',
                'row' : '3'
            }),
            'category': forms.Select(attrs={   
                'class': 'form-control w-50',
            }),
            'thumbnail' : forms.ClearableFileInput(attrs = {
                'class' : 'form-control w-50',
                
            }),
            'price' : forms.TextInput(attrs = {
                'class' : 'form-control w-50',
                'placeholder' : 'Price'
            }),
            'stock' : forms.TextInput(attrs = {
                'class' : 'form-control w-50',
                'placeholder' : 'Stock'
            }),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['category'].empty_label = "Select Category"


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'caption']

        widgets = {
            'image' : forms.ClearableFileInput(attrs = {
                'class' : 'form-control',
                'placeholde' : 'Image'
            }),
            'caption' : forms.TextInput(attrs = {
                'class' : 'form-control',
                'placeholde' : 'Image Caption',
                
            })

        }
