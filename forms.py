"""Form definitions for Family Tree application."""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError, Regexp
from models.user import User


class RegistrationForm(FlaskForm):
    """User registration form."""
    
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=80, message='Username must be between 3 and 80 characters'),
            Regexp('^[a-zA-Z0-9_.-]+$', message='Username can only contain letters, numbers, underscores, dots, and dashes')
        ]
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Invalid email address')
        ]
    )
    
    first_name = StringField(
        'First Name',
        validators=[
            Optional(),
            Length(max=100)
        ]
    )
    
    last_name = StringField(
        'Last Name',
        validators=[
            Optional(),
            Length(max=100)
        ]
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required'),
            Length(min=6, max=120, message='Password must be between 6 and 120 characters')
        ]
    )
    
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message='Please confirm your password'),
            EqualTo('password', message='Passwords must match')
        ]
    )
    
    submit = SubmitField('Register')
    
    def validate_username(self, field):
        """Check if username already exists."""
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Username already exists')
    
    def validate_email(self, field):
        """Check if email already exists."""
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Email already registered')


class LoginForm(FlaskForm):
    """User login form."""
    
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required')
        ]
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required')
        ]
    )
    
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class FamilyMemberForm(FlaskForm):
    """Form for adding/editing family members."""
    
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(message='First name is required'),
            Length(min=1, max=100, message='First name must be between 1 and 100 characters')
        ]
    )
    
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(message='Last name is required'),
            Length(min=1, max=100, message='Last name must be between 1 and 100 characters')
        ]
    )
    
    gender = SelectField(
        'Gender',
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        validators=[DataRequired(message='Gender is required')]
    )
    
    dob = DateField(
        'Date of Birth',
        validators=[Optional()],
        format='%Y-%m-%d'
    )
    
    email = StringField(
        'Email',
        validators=[
            Optional(),
            Email(message='Invalid email address')
        ]
    )
    
    phone = StringField(
        'Phone',
        validators=[
            Optional(),
            Length(max=20, message='Phone must be less than 20 characters'),
            Regexp(r'^[\d\s\-\(\)\+]*$', message='Phone contains invalid characters')
        ]
    )
    
    address = TextAreaField(
        'Address',
        validators=[Optional()]
    )
    
    biography = TextAreaField(
        'Biography',
        validators=[Optional()]
    )
    
    father_id = SelectField(
        'Father',
        choices=[],
        validators=[Optional()]
    )
    
    mother_id = SelectField(
        'Mother',
        choices=[],
        validators=[Optional()]
    )
    
    spouse_id = SelectField(
        'Spouse',
        choices=[],
        validators=[Optional()]
    )
    
    submit = SubmitField('Save Member')


class PhotoUploadForm(FlaskForm):
    """Form for uploading family member photos."""
    
    photo = FileField(
        'Photo',
        validators=[
            DataRequired(message='Please select a photo'),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message='Only image files are allowed')
        ]
    )
    
    submit = SubmitField('Upload Photo')


class SearchForm(FlaskForm):
    """Form for searching family members."""
    
    query = StringField(
        'Search',
        validators=[
            DataRequired(message='Please enter a search term'),
            Length(min=1, max=100, message='Search term must be between 1 and 100 characters')
        ]
    )
    
    submit = SubmitField('Search')


class UpdateProfileForm(FlaskForm):
    """Form for updating user profile."""
    
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=80, message='Username must be between 3 and 80 characters')
        ]
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Invalid email address')
        ]
    )
    
    first_name = StringField(
        'First Name',
        validators=[
            Optional(),
            Length(max=100, message='First name must be less than 100 characters')
        ]
    )
    
    last_name = StringField(
        'Last Name',
        validators=[
            Optional(),
            Length(max=100, message='Last name must be less than 100 characters')
        ]
    )
    
    submit = SubmitField('Update Profile')
    
    def validate_username(self, field):
        """Check if username already exists (excluding current user)."""
        from flask_login import current_user
        
        if field.data != current_user.username:
            user = User.query.filter_by(username=field.data).first()
            if user:
                raise ValidationError('Username already exists')
    
    def validate_email(self, field):
        """Check if email already exists (excluding current user)."""
        from flask_login import current_user
        
        if field.data != current_user.email:
            user = User.query.filter_by(email=field.data).first()
            if user:
                raise ValidationError('Email already registered')


class ChangePasswordForm(FlaskForm):
    """Form for changing user password."""
    
    current_password = PasswordField(
        'Current Password',
        validators=[
            DataRequired(message='Please enter your current password')
        ]
    )
    
    new_password = PasswordField(
        'New Password',
        validators=[
            DataRequired(message='Please enter a new password'),
            Length(min=6, max=120, message='Password must be between 6 and 120 characters')
        ]
    )
    
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(message='Please confirm your new password'),
            EqualTo('new_password', message='Passwords must match')
        ]
    )
    
    submit = SubmitField('Change Password')
    
    def validate_current_password(self, field):
        """Verify current password is correct."""
        from flask_login import current_user
        
        if not current_user.check_password(field.data):
            raise ValidationError('Current password is incorrect')


class AdvancedSearchForm(FlaskForm):
    """Form for advanced family member search."""
    
    first_name = StringField(
        'First Name',
        validators=[Optional()]
    )
    
    last_name = StringField(
        'Last Name',
        validators=[Optional()]
    )
    
    gender = SelectField(
        'Gender',
        choices=[
            ('', 'Any'),
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        validators=[Optional()]
    )
    
    email = StringField(
        'Email',
        validators=[Optional()]
    )
    
    phone = StringField(
        'Phone',
        validators=[Optional()]
    )
    
    submit = SubmitField('Search')


class BulkImportForm(FlaskForm):
    """Form for bulk importing family members."""
    
    csv_file = FileField(
        'CSV File',
        validators=[
            DataRequired(message='Please select a CSV file'),
            FileAllowed(['csv', 'txt'], message='Only CSV files are allowed')
        ]
    )
    
    submit = SubmitField('Import Members')


class ExportForm(FlaskForm):
    """Form for exporting family tree."""
    
    export_format = SelectField(
        'Export Format',
        choices=[
            ('csv', 'CSV (Spreadsheet)'),
            ('json', 'JSON (Data)'),
            ('pdf', 'PDF (Document)')
        ],
        validators=[DataRequired(message='Please select export format')]
    )
    
    include_photos = BooleanField('Include Photos', default=False)
    include_relationships = BooleanField('Include Relationships', default=True)
    
    submit = SubmitField('Export Family Tree')
