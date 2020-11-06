from django import forms
from catalog_app.models import Product, Category, Variation, ProductReview


# SIZES=(
#     ('small','small'),
#     ('medium','medium'),
# )
# COLOR=(
#     ('white','white'),
#     ('yellow','yellow'),
#     ('black','black'),
# )
class ProductAddToCartForm(forms.Form):
    """ form class to add items to the shopping cart """
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size': '2', 'value': '1', 'class': 'quantity'}),
                                  error_messages={
                                      'invalid': 'Please enter a valid quantity.'},
                                  min_value=1)
    product_slug = forms.CharField(widget=forms.HiddenInput())
    # size=forms.ChoiceField(choices=SIZES, initial='medium')
    # color=forms.ChoiceField(choices=COLOR, initial='white')

    def __init__(self, request=None, *args, **kwargs):
        """ override the default so we can set the request """
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    def clean(self):
        """ custom validation to check for presence of cookies in customer's browser """
        if self.request:
            # used to check cookie existence:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies must be enabled.")
        return self.cleaned_data


class ProductReviewForm(forms.ModelForm):
    """ Form class to submit a new ProductReview instance """
    class Meta:
        model = ProductReview
        exclude = ('user','product', 'is_approved')