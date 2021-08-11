from django import forms


class VideoUrlForm(forms.Form):
    video_url = forms.URLField(label='', label_suffix="", max_length=500,
    widget=forms.TextInput(attrs={'placeholder': 'Cole o Link do Video Aqui...'}))

