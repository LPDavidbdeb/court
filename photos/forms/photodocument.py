from django import forms
from ..models import Photo, PhotoType, PhotoDocument

class PhotoDocumentSingleUploadForm(forms.Form):
    """
    A streamlined form to create a PhotoDocument from a single new image upload.
    """
    file = forms.ImageField(
        label="Photo File",
        help_text="Select the image file for the document.",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    title = forms.CharField(
        label="Document Title",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label="Description (Optional)",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    datetime_original = forms.DateTimeField(
        required=True,
        label="Document Date/Time",
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        help_text="The date and time the document was created, not when it was scanned."
    )

class PhotoDocumentForm(forms.ModelForm):
    """
    A form for creating and updating PhotoDocument objects by grouping existing photos.
    """
    try:
        document_photo_type = PhotoType.objects.get(name='Document')
        photos_queryset = Photo.objects.filter(photo_type=document_photo_type)
    except PhotoType.DoesNotExist:
        photos_queryset = Photo.objects.none()

    photos = forms.ModelMultipleChoiceField(
        queryset=photos_queryset,
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '10'}),
        required=True,
        help_text="Select one or more photos that have been marked with the 'Document' type."
    )

    class Meta:
        model = PhotoDocument
        fields = ['title', 'description', 'photos']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
