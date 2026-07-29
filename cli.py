"""Flask CLI commands for Family Tree application."""

import click
from flask.cli import with_appcontext
from app import app, db
from models.user import User
from models.family import FamilyMember
from utils import create_backup, get_storage_usage


@app.cli.command()
@with_appcontext
def init_db():
    """Initialize the database."""
    click.echo('Initializing database...')
    db.create_all()
    click.echo('✓ Database initialized successfully')


@app.cli.command()
@with_appcontext
def reset_db():
    """Reset the database (WARNING: Deletes all data)."""
    if click.confirm('⚠️  This will delete all data. Are you sure?'):
        db.drop_all()
        db.create_all()
        click.echo('✓ Database reset successfully')
    else:
        click.echo('Reset cancelled')


@app.cli.command()
@with_appcontext
def create_user(username, email, password):
    """Create a new user account.
    
    Example: flask create-user john john@example.com secret123
    """
    # Check if user exists
    if User.query.filter_by(username=username).first():
        click.echo(f'✗ User "{username}" already exists')
        return
    
    if User.query.filter_by(email=email).first():
        click.echo(f'✗ Email "{email}" already registered')
        return
    
    # Create user
    user = User(username=username, email=email)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    click.echo(f'✓ User "{username}" created successfully')


@app.cli.command()
@with_appcontext
def list_users():
    """List all registered users."""
    users = User.query.all()
    
    if not users:
        click.echo('No users found')
        return
    
    click.echo('\nRegistered Users:')
    click.echo('─' * 60)
    
    for user in users:
        member_count = FamilyMember.query.filter_by(user_id=user.id).count()
        click.echo(f'{user.username:<20} {user.email:<30} Members: {member_count}')


@app.cli.command()
@with_appcontext
def delete_user(username):
    """Delete a user account and all their data.
    
    Example: flask delete-user john
    """
    user = User.query.filter_by(username=username).first()
    
    if not user:
        click.echo(f'✗ User "{username}" not found')
        return
    
    if click.confirm(f'⚠️  Delete user "{username}" and all their data?'):
        member_count = FamilyMember.query.filter_by(user_id=user.id).count()
        
        # Delete family members and photos
        for member in FamilyMember.query.filter_by(user_id=user.id):
            if member.photo:
                try:
                    import os
                    photo_path = os.path.join(
                        app.config['UPLOAD_FOLDER'], 
                        member.photo
                    )
                    if os.path.exists(photo_path):
                        os.remove(photo_path)
                except Exception as e:
                    click.echo(f'Warning: Could not delete photo: {e}')
        
        db.session.delete(user)
        db.session.commit()
        
        click.echo(f'✓ User "{username}" and {member_count} family members deleted')
    else:
        click.echo('Deletion cancelled')


@app.cli.command()
@with_appcontext
def list_members():
    """List all family members."""
    members = FamilyMember.query.all()
    
    if not members:
        click.echo('No family members found')
        return
    
    click.echo('\nFamily Members:')
    click.echo('─' * 80)
    
    for member in members:
        user = User.query.get(member.user_id)
        username = user.username if user else 'Unknown'
        age = f' ({member.get_age()} yrs)' if member.get_age() else ''
        click.echo(f'{member.get_full_name():<25} {username:<20} {member.gender}{age}')


@app.cli.command()
@with_appcontext
def database_stats():
    """Show database statistics."""
    user_count = User.query.count()
    member_count = FamilyMember.query.count()
    
    click.echo('\nDatabase Statistics:')
    click.echo('─' * 40)
    click.echo(f'Total Users:          {user_count}')
    click.echo(f'Total Family Members: {member_count}')
    
    if user_count > 0:
        avg_members = member_count / user_count
        click.echo(f'Avg Members/User:     {avg_members:.2f}')
    
    # Storage usage
    storage = get_storage_usage()
    click.echo(f'\nStorage Usage:')
    click.echo(f'  Files:               {storage["file_count"]}')
    click.echo(f'  Total Size:          {storage["total_mb"]} MB')


@app.cli.command()
@with_appcontext
def backup_database():
    """Create a backup of the database."""
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        backup_path = create_backup(db_path)
        
        if backup_path:
            click.echo(f'✓ Backup created: {backup_path}')
        else:
            click.echo('✗ Backup failed')
    else:
        click.echo('ℹ Backup command only works with SQLite database')
        click.echo('For PostgreSQL, use pg_dump command')


@app.cli.command()
@with_appcontext
def generate_secret_key():
    """Generate a new secret key."""
    from utils import generate_secret_key
    
    secret_key = generate_secret_key()
    click.echo('Generated Secret Key:')
    click.echo('─' * 60)
    click.echo(secret_key)
    click.echo('\nAdd this to your .env file as:')
    click.echo(f'SECRET_KEY={secret_key}')


@app.cli.command()
@with_appcontext
def check_integrity():
    """Check database integrity."""
    click.echo('Checking database integrity...')
    click.echo('─' * 60)
    
    errors = []
    
    # Check users
    users = User.query.all()
    click.echo(f'✓ Found {len(users)} users')
    
    # Check family members
    members = FamilyMember.query.all()
    click.echo(f'✓ Found {len(members)} family members')
    
    # Check for orphaned members (user deleted but members remain)
    for member in members:
        if not User.query.get(member.user_id):
            errors.append(f'Orphaned member: {member.get_full_name()} (user_id: {member.user_id})')
    
    # Check for invalid relationships
    for member in members:
        if member.father_id:
            if not FamilyMember.query.get(member.father_id):
                errors.append(f'Invalid father reference: {member.get_full_name()}')
        
        if member.mother_id:
            if not FamilyMember.query.get(member.mother_id):
                errors.append(f'Invalid mother reference: {member.get_full_name()}')
        
        if member.spouse_id:
            if not FamilyMember.query.get(member.spouse_id):
                errors.append(f'Invalid spouse reference: {member.get_full_name()}')
    
    # Report results
    if errors:
        click.echo('\n⚠️  Integrity Issues Found:')
        for error in errors:
            click.echo(f'  - {error}')
    else:
        click.echo('\n✓ Database integrity check passed')


@app.cli.command()
@with_appcontext
def cleanup_storage():
    """Clean up orphaned files from uploads directory."""
    import os
    
    upload_dir = app.config.get('UPLOAD_FOLDER', 'static/uploads')
    
    if not os.path.exists(upload_dir):
        click.echo('Upload directory not found')
        return
    
    # Get all files in upload directory
    files_to_check = []
    for filename in os.listdir(upload_dir):
        filepath = os.path.join(upload_dir, filename)
        if os.path.isfile(filepath) and filename != '.gitkeep':
            files_to_check.append(filename)
    
    if not files_to_check:
        click.echo('No files to check')
        return
    
    click.echo(f'Checking {len(files_to_check)} files...')
    
    # Check which files are referenced in database
    orphaned = []
    for filename in files_to_check:
        member = FamilyMember.query.filter_by(photo=filename).first()
        if not member:
            orphaned.append(filename)
    
    if orphaned:
        click.echo(f'\nFound {len(orphaned)} orphaned files:')
        for filename in orphaned:
            click.echo(f'  - {filename}')
        
        if click.confirm('\nDelete orphaned files?'):
            deleted = 0
            for filename in orphaned:
                try:
                    filepath = os.path.join(upload_dir, filename)
                    os.remove(filepath)
                    deleted += 1
                except Exception as e:
                    click.echo(f'Error deleting {filename}: {e}')
            
            click.echo(f'✓ Deleted {deleted} orphaned files')
    else:
        click.echo('✓ No orphaned files found')


@app.cli.command()
@with_appcontext
def export_members(format='csv'):
    """Export family members to file.
    
    Supported formats: csv, json
    Example: flask export-members --format=csv
    """
    members = FamilyMember.query.all()
    
    if not members:
        click.echo('No family members to export')
        return
    
    if format == 'csv':
        import csv
        
        filename = f'export_members_{click.get_current_context().info_name}.csv'
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'First Name', 'Last Name', 'Gender', 'DOB', 
                'Email', 'Phone', 'Address', 'Biography'
            ])
            
            # Write data
            for member in members:
                writer.writerow([
                    member.first_name,
                    member.last_name,
                    member.gender,
                    member.dob if member.dob else '',
                    member.email or '',
                    member.phone or '',
                    member.address or '',
                    member.biography or ''
                ])
        
        click.echo(f'✓ Exported {len(members)} members to {filename}')
    
    elif format == 'json':
        import json
        
        filename = f'export_members_{click.get_current_context().info_name}.json'
        
        data = []
        for member in members:
            data.append({
                'id': member.id,
                'first_name': member.first_name,
                'last_name': member.last_name,
                'gender': member.gender,
                'dob': str(member.dob) if member.dob else None,
                'email': member.email,
                'phone': member.phone,
                'address': member.address,
                'biography': member.biography
            })
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        click.echo(f'✓ Exported {len(members)} members to {filename}')
    
    else:
        click.echo(f'Unsupported format: {format}')


if __name__ == '__main__':
    app.cli()
