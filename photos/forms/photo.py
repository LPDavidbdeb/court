from django import forms
from ..models import Photo, PhotoType

class PhotoUploadForm(forms.Form):
    """
    A dedicated form for uploading a single photo and editing its key metadata.
    """
    file = forms.ImageField(
        label="Photo File",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    photo_type = forms.ModelChoiceField(
        queryset=PhotoType.objects.all(),
        required=False,
        label="Photo Type",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    artist = forms.CharField(
        max_length=255,
        required=False,
        label="Artist / Photographer",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    datetime_original = forms.DateTimeField(
        required=True,
        label="Date/Time Taken",
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        help_text="If the photo has no date, this will be injected into the new file."
    )
    gps_latitude = forms.FloatField(
        required=False,
        label="GPS Latitude",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    gps_longitude = forms.FloatField(
        required=False,
        label="GPS Longitude",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )

class PhotoForm(forms.ModelForm):
    """
    A form for the standard Create and Update views for a single photo.
    """
    class Meta:
        model = Photo
        fields = ['file', 'photo_type', 'datetime_original', 'file_name']
        widgets = {
            'photo_type': forms.Select(attrs={'class': 'form-select'}),
            'datetime_original': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'file_name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class PhotoProcessingForm(forms.Form):
    """
    A form to select a processing mode, a source directory, and an optional photo type.
    """
    PROCESSING_CHOICES = [
        ('add_by_path', 'Add New Photos (by File Path, Non-Destructive)'),
        ('add_by_timestamp', 'Add New Photos (Check for Timestamp Duplicates)'),
        ('add_interactive', 'Add New Photos (Interactive, Manual Date Entry)'),
        ('clean', 'Clean Install (Deletes All Existing Photos)'),
    ]

    processing_mode = forms.ChoiceField(
        choices=PROCESSING_CHOICES,
        initial='add_by_path',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Processing Mode"
    )
    source_directory = forms.CharField(
        label="Source Directory Path",
        max_length=500,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '/path/to/your/photos'}),
        help_text="Enter the full, absolute path to the directory on the server containing the photos to process."
    )
    photo_type = forms.ModelChoiceField(
        queryset=PhotoType.objects.all(),
        required=False,
        label="Assign Photo Type (Optional)",
        help_text="Select a type to assign to all imported photos."
    )
