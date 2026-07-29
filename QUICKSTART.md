# 🚀 Quick Start Guide - Family Tree Application

## ⚡ 60-Second Setup

### Windows
```cmd
setup.bat
python app.py
```
Then open: http://localhost:5000

### macOS / Linux
```bash
chmod +x setup.sh
./setup.sh
python app.py
```
Then open: http://localhost:5000

### Docker (All Platforms)
```bash
docker-compose up
```
Then open: http://localhost:5000

---

## 📝 First Time Usage

1. **Open Application**
   - Go to http://localhost:5000
   - Click "Register" or "Get Started"

2. **Create Account**
   - Username: (your choice)
   - Email: your@email.com
   - Password: (min 6 characters)
   - Click "Register"

3. **Login**
   - Enter credentials
   - Click "Login"

4. **Add First Family Member**
   - Dashboard → "Add Member"
   - Fill in details
   - Click "Add Member"

5. **View Family Tree**
   - Dashboard → "Family Tree"
   - See your family visualization

---

## 💻 Common Commands

### Virtual Environment

**Activate:**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**Deactivate:**
```bash
deactivate
```

**Install packages:**
```bash
pip install -r requirements.txt
```

**Update packages:**
```bash
pip install --upgrade package-name
pip freeze > requirements.txt
```

### Running Application

**Development:**
```bash
python app.py
```

**With Gunicorn (production):**
```bash
gunicorn app:app
```

**With auto-reload:**
```bash
flask run --reload
```

**On different port:**
```bash
python app.py --port 8000
```

### Database

**Reset database:**
```bash
rm family.db
python app.py
```

**Backup database:**
```bash
cp family.db family.db.backup
```

**Restore database:**
```bash
cp family.db.backup family.db
```

### Code Quality

**Format code:**
```bash
black .
```

**Sort imports:**
```bash
isort .
```

**Check style:**
```bash
flake8 .
```

**Run tests:**
```bash
pytest
pytest --cov=.
```

### Docker

**Start services:**
```bash
docker-compose up
```

**Stop services:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f
```

**Rebuild containers:**
```bash
docker-compose up --build
```

**Access database:**
```bash
docker-compose exec db psql -U family_user -d family_tree
```

---

## 🔧 Configuration

### Change Settings

Edit `.env` file:
```env
FLASK_ENV=development  # Change to 'production'
SECRET_KEY=your-key    # Generate new one
DATABASE_URL=...       # Change database
DEBUG=True             # Set to False for production
```

### Generate Secret Key

```bash
# Windows
python -c "import secrets; print(secrets.token_urlsafe(32))"

# macOS/Linux
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Change Port

In `.env`:
```env
PORT=8000
```

---

## 🐛 Troubleshooting

### "Port 5000 already in use"
```bash
# Kill process on port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### "Module not found" Error
```bash
pip install -r requirements.txt
```

### Database file corrupted
```bash
rm family.db
python app.py
```

### Virtual environment issues
```bash
# Remove old environment
rm -rf venv

# Create new environment
python -m venv venv
source venv/bin/activate  # or activate.bat on Windows
pip install -r requirements.txt
```

### Can't connect to database
1. Check DATABASE_URL in .env
2. Verify database is running
3. Check credentials
4. Reset database: `rm family.db`

### Static files not loading
1. Check path in templates
2. Verify file exists in `static/` folder
3. Restart Flask application
4. Clear browser cache (Ctrl+Shift+Delete)

---

## 📚 Project Structure

```
Family_Project/
├── app.py                 # Start here
├── config.py              # Configuration
├── .env                   # Secrets (don't commit!)
├── models/                # Database models
├── routes/                # URL routes
├── templates/             # HTML pages
├── static/                # CSS, JS, images
└── family.db              # Database file
```

---

## 🚀 Deployment

### Deploy to Railway (Easiest)

1. Push to GitHub
2. Go to railway.app
3. Connect your repository
4. Set environment variables
5. Deploy!

### Deploy to Heroku

```bash
heroku create your-app-name
heroku config:set SECRET_KEY=<your-key>
git push heroku main
```

See `DEPLOYMENT.md` for more options.

---

## 📋 Feature Overview

| Feature | How to Use |
|---------|-----------|
| Add Member | Dashboard → Add Member |
| Edit Member | Dashboard → Member → Edit |
| Delete Member | Dashboard → Member → Delete |
| Upload Photo | Member Profile → Upload Photo |
| Search Members | Dashboard → Search box |
| View Family Tree | Dashboard → Family Tree |
| Link Relationships | Edit Member → Select Parents/Spouse |
| View Profile | Dashboard → Member → View |

---

## 🔑 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+F` | Search members |
| `Ctrl+Enter` | Submit form |
| `Esc` | Close modal/dialog |
| `Tab` | Navigate form fields |
| `Enter` | Confirm action |

---

## 🌐 URLs Reference

| Page | URL |
|------|-----|
| Home | http://localhost:5000/ |
| Register | http://localhost:5000/auth/register |
| Login | http://localhost:5000/auth/login |
| Dashboard | http://localhost:5000/dashboard |
| Add Member | http://localhost:5000/family/add |
| Family Tree | http://localhost:5000/family/tree |
| Search | http://localhost:5000/search |
| Profile | http://localhost:5000/profile |

---

## 📱 Responsive Design

Application works on:
- ✅ Desktop (1920px+)
- ✅ Laptop (1366px+)
- ✅ Tablet (768px+)
- ✅ Mobile (480px+)

Tip: Press F12 in browser to test responsive design.

---

## 🎨 Customization

### Change Colors

Edit `static/css/style.css`:
```css
:root {
    --primary-color: #0d6efd;      /* Blue */
    --secondary-color: #6c757d;    /* Gray */
    --danger-color: #dc3545;       /* Red */
}
```

### Add Logo

Place image in `static/images/logo.png`

Edit `templates/base.html`:
```html
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">
```

### Change Application Title

Edit all `templates/` files:
```html
{% block title %}Your Title{% endblock %}
```

---

## 📞 Getting Help

1. **Check Documentation**
   - README.md - Main guide
   - DEPLOYMENT.md - Deployment help
   - CONTRIBUTING.md - Contributing guide

2. **Search Issues**
   - GitHub Issues
   - Stack Overflow
   - Flask Documentation

3. **Ask for Help**
   - Create GitHub Issue
   - Join Discord community
   - Email support

---

## ✅ Checklist for Production

- [ ] Change SECRET_KEY in .env
- [ ] Set FLASK_ENV=production
- [ ] Use PostgreSQL (not SQLite)
- [ ] Enable HTTPS
- [ ] Set up backups
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Review security settings
- [ ] Test thoroughly
- [ ] Document your setup

---

## 🎯 Best Practices

1. **Never commit .env file** - Use .env.example
2. **Backup database regularly** - Prevent data loss
3. **Keep dependencies updated** - Security patches
4. **Test locally first** - Before deploying
5. **Document changes** - Help future developers
6. **Use meaningful commit messages** - Clear history
7. **Comment complex code** - Explain logic
8. **Use version control** - Track changes

---

## 🚀 Performance Tips

- Use PostgreSQL in production (faster than SQLite)
- Enable browser caching for static files
- Minimize CSS and JavaScript
- Optimize images before upload
- Use CDN for static files
- Enable database query caching
- Monitor performance regularly

---

## 🔒 Security Reminders

- ✅ Never share SECRET_KEY
- ✅ Use HTTPS in production
- ✅ Validate all user input
- ✅ Keep dependencies updated
- ✅ Use strong passwords
- ✅ Enable CSRF protection
- ✅ Backup data regularly
- ✅ Monitor for suspicious activity

---

## 📞 Quick Links

- **Flask**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Bootstrap**: https://getbootstrap.com/
- **PostgreSQL**: https://www.postgresql.org/
- **Railway**: https://railway.app/
- **Heroku**: https://www.heroku.com/

---

## 🎉 You're All Set!

Your Family Tree application is ready to use!

**What's next?**
1. Create your first account
2. Add family members
3. Link relationships
4. Upload photos
5. Customize to your needs
6. Share with family
7. Deploy online

---

**Happy documenting your family history! 🌳**
