from django import forms

class EmailSearchForm(forms.Form):
    """
    Form for searching emails.
    """
    sender_email = forms.CharField(
        label="Sender Email (or other participant)",
        max_length=255,
        required=True,
        help_text="e.g., sender@example.com"
    )
    date_sent = forms.DateField(
        label="Date Sent",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        help_text="e.g., YYYY-MM-DD"
    )
    email_excerpt = forms.CharField(
        label="Email Excerpt (optional, for content search)",
        max_length=500,
        required=False,
        help_text="A phrase or keyword from the email body/subject."
    )