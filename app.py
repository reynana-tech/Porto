from flask import Flask, render_template, send_from_directory
from config import Config
from model import get_profiles, get_skills, get_projects, get_experience
from jinja2 import ChoiceLoader, FileSystemLoader

app = Flask(
    __name__,
    static_folder='Frontend',
    static_url_path='/static'
)

# Tambahkan loader untuk root dan Frontend
app.jinja_loader = ChoiceLoader([
    FileSystemLoader('.'),          # cari template di root project
    FileSystemLoader('Frontend')    # cari template di Frontend
])

app.secret_key = Config.SECRET_KEY

# Halaman utama (public portfolio)
@app.route("/")
def home():
    profiles    = get_profiles()
    skills      = get_skills()
    projects    = get_projects()
    experience  = get_experience()
    return render_template("index.html",   # file ada di root project
        profiles=profiles,
        skills=skills,
        projects=projects,
        experience=experience
    )

# Register blueprints untuk admin
from Backend.utama.utama import utama_bp
from Backend.admin.login import login_bp
from Backend.admin.dashboard import dashboard_bp
from Backend.admin.profiles import profiles_bp
from Backend.admin.skills import skills_bp
from Backend.admin.experience import experience_bp
from Backend.admin.projects import projects_bp
from Backend.admin.upload import upload_bp
from Backend.admin.contact import contact_bp

app.register_blueprint(utama_bp)
app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(profiles_bp)
app.register_blueprint(skills_bp)
app.register_blueprint(experience_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(contact_bp)

# Favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('.', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    try:
        from model import init_db
        init_db()
        print("✅ Database tables initialized.")
    except Exception as e:
        print(f"⚠️  Database init error: {e}")

    app.run(debug=True, host='0.0.0.0', port=5000)
