from django import forms
from ....learning_paths.models import LearningPath
from careers.models import Career, Skill, LearningResource

class LearningPathFilterForm(forms.Form):
    """Form for filtering learning paths"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Search learning paths...'
            }
        )
    )
    
    career = forms.ChoiceField(
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    
    def __init__(self, *args, **kwargs):
        careers = kwargs.pop('careers', [])
        super().__init__(*args, **kwargs)
        
        # Add empty choice
        career_choices = [('', 'All Careers')]
        # Add careers from database
        career_choices.extend([(c.id, c.name) for c in careers])
        self.fields['career'].choices = career_choices

class PathNoteForm(forms.Form):
    """Form for adding notes to a learning path step"""
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add your notes about this step here...'
            }
        )
    )

class PathShareForm(forms.ModelForm):
    """Form for sharing a learning path publicly"""
    class Meta:
        model = LearningPath
        fields = ['is_public']
        widgets = {
            'is_public': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            )
        }
        labels = {
            'is_public': 'Share this learning path publicly'
        }

class CareerSelectionForm(forms.Form):
    """Form for selecting a career to generate a learning path"""
    career_id = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    
    def __init__(self, *args, **kwargs):
        careers = kwargs.pop('careers', [])
        super().__init__(*args, **kwargs)
        
        # Convert careers to choices for the dropdown
        career_choices = [(career.id, career.name) for career in careers]
        self.fields['career_id'].choices = career_choices

class CustomPathForm(forms.ModelForm):
    """Form for creating a custom learning path"""
    class Meta:
        model = LearningPath
        fields = ['title', 'description', 'career', 'duration_weeks']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'career': forms.Select(attrs={'class': 'form-select'}),
            'duration_weeks': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }