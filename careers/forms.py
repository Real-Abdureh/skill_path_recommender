from django import forms
from ....careers.models import Career, Skill, LearningResource

class CareerFilterForm(forms.Form):
    """Form for filtering careers"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Search careers...'
            }
        )
    )
    
    category = forms.ChoiceField(
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    
    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', [])
        super().__init__(*args, **kwargs)
        
        # Add empty choice
        category_choices = [('', 'All Categories')]
        # Add categories from database
        category_choices.extend([(c, c) for c in categories if c])
        self.fields['category'].choices = category_choices

class SkillFilterForm(forms.Form):
    """Form for filtering skills"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Search skills...'
            }
        )
    )
    
    category = forms.ChoiceField(
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    
    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', [])
        super().__init__(*args, **kwargs)
        
        # Add empty choice
        category_choices = [('', 'All Categories')]
        # Add categories from database
        category_choices.extend([(c, c) for c in categories if c])
        self.fields['category'].choices = category_choices

class ResourceFilterForm(forms.Form):
    """Form for filtering learning resources"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Search resources...'
            }
        )
    )
    
    resource_type = forms.ChoiceField(
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    
    difficulty = forms.ChoiceField(
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    
    is_free = forms.ChoiceField(
        required=False,
        choices=[('', 'Any'), ('true', 'Free Only'), ('false', 'Paid Only')],
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    
    def __init__(self, *args, **kwargs):
        resource_types = kwargs.pop('resource_types', [])
        difficulty_levels = kwargs.pop('difficulty_levels', [])
        super().__init__(*args, **kwargs)
        
        # Add empty choice for resource type
        type_choices = [('', 'All Types')]
        # Add resource types from model
        type_choices.extend(resource_types)
        self.fields['resource_type'].choices = type_choices
        
        # Add empty choice for difficulty
        difficulty_choices = [('', 'All Levels')]
        # Add difficulty levels from model
        difficulty_choices.extend(difficulty_levels)
        self.fields['difficulty'].choices = difficulty_choices

class UserSkillForm(forms.Form):
    """Form for adding a user skill"""
    skill_id = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    
    proficiency = forms.ChoiceField(
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert')
        ],
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    
    def __init__(self, *args, **kwargs):
        skills = kwargs.pop('skills', [])
        super().__init__(*args, **kwargs)
        
        # Convert skills to choices for the dropdown
        skill_choices = [(skill.id, skill.name) for skill in skills]
        self.fields['skill_id'].choices = skill_choices