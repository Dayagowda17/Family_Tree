# 🌳 Family Tree Web Application

A modern, responsive web application to build and manage your family tree online. Create, edit, and visualize family members with relationships in an interactive interface.

## ✨ Features

- ✅ **User Authentication** - Secure login and registration system
- ✅ **Family Member Management** - Add, edit, and delete family members
- ✅ **Relationship Tracking** - Track father, mother, spouse, and children relationships
- ✅ **Photo Uploads** - Upload and manage family member photos with automatic resizing
- ✅ **Interactive Family Tree** - Visual representation of family hierarchy
- ✅ **Search Functionality** - Search family members by name, email, or phone
- ✅ **Responsive Design** - Mobile-friendly Bootstrap 5 interface
- ✅ **User Profiles** - View and manage user profile information
- ✅ **Dashboard** - Overview of family statistics and quick actions
- ✅ **Database Support** - SQLite for development, PostgreSQL for production
- ✅ **Production Ready** - Configured for Railway and Heroku deployment

## 🛠️ Technology Stack

- **Backend**: Flask 2.3.3
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Image Processing**: Pillow
- **Server**: Gunicorn
- **Deployment**: Railway, Heroku

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git

## 🚀 Local Development Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Family_Project
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite:///family.db
```

### 5. Initialize Database
```bash
flask db upgrade
# Or simply run the app to auto-create tables
```

### 6. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### 7. Create a Test Account
- Navigate to the registration page
- Create a new account with credentials
- Login and start adding family members

## 📁 Project Structure

```
Family_Project/
│
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── .gitignore              # Git ignore file
├── Procfile                # Heroku deployment config
├── runtime.txt             # Python version
├── railway.json            # Railway deployment config
│
├── models/
│   ├── __init__.py         # SQLAlchemy initialization
│   ├── user.py             # User model
│   ├── family.py           # FamilyMember model
│   └── relationship.py     # Relationship model
│
├── routes/
│   ├── auth.py             # Authentication routes
│   ├── dashboard.py        # Dashboard routes
│   ├── family.py           # Family member routes
│   └── upload.py           # File upload routes
│
├── templates/
│   ├── base.html           # Base template
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── dashboard.html      # Dashboard
│   ├── add_member.html     # Add member form
│   ├── edit_member.html    # Edit member form
│   ├── profile.html        # Member profile
│   ├── family_tree.html    # Family tree visualization
│   ├── search_results.html # Search results
│   ├── 404.html            # 404 error page
│   ├── 500.html            # 500 error page
│   └── 403.html            # 403 error page
│
├── static/
│   ├── css/
│   │   └── style.css       # Custom CSS
│   ├── js/
│   │   └── script.js       # JavaScript functions
│   ├── images/             # Static images
│   └── uploads/            # User uploaded photos
│
└── family.db               # SQLite database
```

## 🔐 Security Features

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- User authentication with Flask-Login
- SQL injection prevention with SQLAlchemy ORM
- Secure file uploads with validation
- Environment-based secret keys

## 🎨 Customization

### Changing Colors
Edit `static/css/style.css` to customize color scheme:
```css
:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    --danger-color: #dc3545;
}
```

### Adding New Features
1. Create new model in `models/` if needed
2. Create new routes in `routes/` directory
3. Create corresponding templates in `templates/`
4. Register blueprint in `app.py`

## 📤 Deployment

### Deploy to Railway

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Create New Project**
   ```bash
   railway init
   ```

4. **Link PostgreSQL Database**
   ```bash
   railway add
   ```

5. **Deploy**
   ```bash
   railway up
   ```

### Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   npm install -g heroku
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create New App**
   ```bash
   heroku create your-app-name
   ```

4. **Add PostgreSQL Database**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set FLASK_ENV=production
   ```

6. **Deploy**
   ```bash
   git push heroku main
   ```

### Environment Variables for Production

Set these variables in your deployment platform:
- `SECRET_KEY` - Strong random secret key
- `FLASK_ENV` - Set to `production`
- `DATABASE_URL` - PostgreSQL connection string (automatically set by platform)

## 📊 Database Models

### User Model
- id, username, email, password_hash
- first_name, last_name
- created_at, updated_at
- Relationship with FamilyMembers

### FamilyMember Model
- id, user_id, first_name, last_name, gender
- dob (date of birth), phone, email, address
- biography, photo
- father_id, mother_id, spouse_id (foreign keys)
- created_at, updated_at

### Relationship Model
- id, member_id, related_member_id
- relationship_type, notes
- created_at

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database (delete and recreate)
rm family.db
python app.py
```

### Virtual Environment Issues
```bash
# Deactivate and remove old environment
deactivate
rm -rf venv

# Create fresh environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Change port in app.py or run on different port
python app.py --port 8000
```

## 📝 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/logout` - Logout user

### Dashboard
- `GET /dashboard` - View dashboard
- `GET /profile` - View user profile
- `GET /search` - Search family members

### Family Management
- `GET /family/add` - Add member form
- `POST /family/add` - Create new member
- `GET /family/<id>` - View member profile
- `GET /family/<id>/edit` - Edit member form
- `POST /family/<id>/edit` - Update member
- `POST /family/<id>/delete` - Delete member
- `GET /family/tree` - View family tree

### File Upload
- `POST /upload/photo/<id>` - Upload member photo
- `POST /upload/photo/<id>/delete` - Delete member photo

## 📞 Contact & Support

For issues, questions, or feature requests, please create an issue on GitHub.

## 📄 License

This project is open source and available under the MIT License.

## 🎯 Future Enhancements

- [ ] Export family tree as PDF
- [ ] Multiple language support
- [ ] Advanced relationship tracking (siblings, cousins, etc.)
- [ ] Family timeline feature
- [ ] Document storage for family records
- [ ] Notifications and reminders
- [ ] Social sharing features
- [ ] Mobile app (React Native)

## 🙏 Acknowledgments

- Bootstrap 5 for responsive design
- Flask for web framework
- SQLAlchemy for ORM
- Pillow for image processing

---

**Made with ❤️ for family connections**
