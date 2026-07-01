import os
import sqlite3
from config import Config
try:
    import pymysql
    from pymysql.cursors import DictCursor
except Exception:
    pymysql = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # naik satu level dari folder Backend


def get_db():
    """Return a DB connection.

    Prefer TiDB/MySQL when `TIDB_HOST` is configured and PyMySQL is available.
    Otherwise fall back to a local SQLite DB file `fallback.db` so the app
    can run in environments without the external database (e.g. quick deploys).
    """
    # Use MySQL/TiDB when host present and pymysql installed
    if Config.TIDB_HOST and pymysql:
        ca_path = Config.TIDB_SSL_CA
        ssl_params = {'ca': ca_path} if ca_path else None
        print("Connecting to TiDB/MySQL host:", Config.TIDB_HOST)
        return pymysql.connect(
            host=Config.TIDB_HOST,
            port=Config.TIDB_PORT,
            user=Config.TIDB_USER,
            password=Config.TIDB_PASSWORD,
            database=Config.TIDB_DB,
            charset='utf8mb4',
            cursorclass=DictCursor,
            ssl=ssl_params
        )

    # Fallback to SQLite
    db_path = os.path.join(BASE_DIR, 'fallback.db')
    print("Using local SQLite fallback at:", db_path)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables and seed default portfolio data."""
    conn = get_db()
    try:
        # For compatibility with both MySQL (PyMySQL) and SQLite we branch
        # because parameter styles and a few SQL features differ.
        use_sqlite = isinstance(conn, sqlite3.Connection)
        cur = conn.cursor()

        if use_sqlite:
            # SQLite-compatible table definitions
            cur.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    title TEXT,
                    bio TEXT,
                    email TEXT,
                    phone TEXT,
                    location TEXT,
                    github TEXT,
                    linkedin TEXT,
                    instagram TEXT,
                    photo_url TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT,
                    level INTEGER DEFAULT 80,
                    icon TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS experiences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL,
                    position TEXT NOT NULL,
                    start_date TEXT,
                    end_date TEXT,
                    is_current INTEGER DEFAULT 0,
                    description TEXT,
                    logo_url TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    tech_stack TEXT,
                    image_url TEXT,
                    demo_url TEXT,
                    repo_url TEXT,
                    is_featured INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    subject TEXT,
                    message TEXT NOT NULL,
                    is_read INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Seed data using SQLite parameter style (?)
            cur.execute("SELECT COUNT(*) as cnt FROM profiles")
            if cur.fetchone()[0] == 0:
                cur.execute(
                    """
                    INSERT INTO profiles (name, title, bio, email, phone, location, github, linkedin, photo_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        'Shafa Reyna Nugrahani',
                        'Mahasiswa S1 Sistem Informasi',
                        'Saya adalah pengembang web yang senang membuat portofolio dan aplikasi yang nyaman digunakan.',
                        'shafareynana@gmail.com',
                        '+62 812-3456-7890',
                        'Salatiga, Indonesia',
                        'https://github.com',
                        'https://linkedin.com',
                        'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=800&q=80'
                    )
                )

            cur.execute("SELECT COUNT(*) as cnt FROM skills")
            if cur.fetchone()[0] == 0:
                cur.executemany(
                    "INSERT INTO skills (name, category, level, icon) VALUES (?, ?, ?, ?)",
                    [
                        ('Python', 'Backend', 90, 'python'),
                        ('Flask', 'Backend', 85, 'flask'),
                        ('JavaScript', 'Frontend', 88, 'javascript'),
                        ('MySQL', 'Database', 80, 'mysql'),
                        ('Git', 'Tools', 82, 'git')
                    ]
                )

            cur.execute("SELECT COUNT(*) as cnt FROM experiences")
            if cur.fetchone()[0] == 0:
                cur.executemany(
                    "INSERT INTO experiences (company, position, start_date, end_date, is_current, description, logo_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [
                        ('Universitas Kristen Satya Wacana', 'Asisten Laboratorium', '2024', 'Sekarang', 1,
                         'Membantu praktikum dan mendukung kegiatan akademik.', 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=400&q=80'),
                        ('PT. Inovasi Digital', 'Web Developer Intern', '2023', '2024', 0,
                         'Mengembangkan halaman web sederhana dan memperbaiki bug aplikasi.', 'https://images.unsplash.com/photo-1516321497487-e288fb19713f?auto=format&fit=crop&w=400&q=80')
                    ]
                )

            cur.execute("SELECT COUNT(*) as cnt FROM projects")
            if cur.fetchone()[0] == 0:
                cur.executemany(
                    "INSERT INTO projects (title, description, tech_stack, image_url, demo_url, repo_url, is_featured) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [
                        ('Portfolio Website', 'Website portofolio interaktif berbasis Flask dan TiDB.', 'Python, Flask, HTML, CSS', 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=800&q=80', 'https://example.com', 'https://github.com', 1),
                        ('Sistem Informasi Akademik', 'Aplikasi sederhana untuk mengelola data akademik.', 'Python, Flask, MySQL', 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=800&q=80', 'https://example.com', 'https://github.com', 0)
                    ]
                )

        else:
            # MySQL / TiDB path (original code) - keep using %s param style
            cur.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    title VARCHAR(150),
                    bio TEXT,
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    location VARCHAR(100),
                    github VARCHAR(200),
                    linkedin VARCHAR(200),
                    instagram VARCHAR(200),
                    photo_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            # Add instagram column if it doesn't exist (for existing databases)
            cur.execute("SHOW COLUMNS FROM profiles LIKE 'instagram'")
            if not cur.fetchone():
                cur.execute("ALTER TABLE profiles ADD COLUMN instagram VARCHAR(200) AFTER linkedin")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    category VARCHAR(50),
                    level INT DEFAULT 80,
                    icon VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS experiences (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    company VARCHAR(150) NOT NULL,
                    position VARCHAR(150) NOT NULL,
                    start_date VARCHAR(20),
                    end_date VARCHAR(20),
                    is_current TINYINT(1) DEFAULT 0,
                    description TEXT,
                    logo_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(150) NOT NULL,
                    description TEXT,
                    tech_stack VARCHAR(300),
                    image_url VARCHAR(500),
                    demo_url VARCHAR(300),
                    repo_url VARCHAR(300),
                    is_featured TINYINT(1) DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    subject VARCHAR(200),
                    message TEXT NOT NULL,
                    is_read TINYINT(1) DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)

            cur.execute("SELECT COUNT(*) as cnt FROM profiles")
            if cur.fetchone()['cnt'] == 0:
                cur.execute("""
                    INSERT INTO profiles (name, title, bio, email, phone, location, github, linkedin, photo_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    'Shafa Reyna Nugrahani',
                    'Mahasiswa S1 Sistem Informasi',
                    'Saya adalah pengembang web yang senang membuat portofolio dan aplikasi yang nyaman digunakan.',
                    'shafareynana@gmail.com',
                    '+62 812-3456-7890',
                    'Salatiga, Indonesia',
                    'https://github.com',
                    'https://linkedin.com',
                    'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=800&q=80'
                ))

            cur.execute("SELECT COUNT(*) as cnt FROM skills")
            if cur.fetchone()['cnt'] == 0:
                cur.execute("""
                    INSERT INTO skills (name, category, level, icon) VALUES
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s)
                """, (
                    'Python', 'Backend', 90, 'python',
                    'Flask', 'Backend', 85, 'flask',
                    'JavaScript', 'Frontend', 88, 'javascript',
                    'MySQL', 'Database', 80, 'mysql',
                    'Git', 'Tools', 82, 'git'
                ))

            cur.execute("SELECT COUNT(*) as cnt FROM experiences")
            if cur.fetchone()['cnt'] == 0:
                cur.execute("""
                    INSERT INTO experiences (company, position, start_date, end_date, is_current, description, logo_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s), (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    'Universitas Kristen Satya Wacana', 'Asisten Laboratorium', '2024', 'Sekarang', 1,
                    'Membantu praktikum dan mendukung kegiatan akademik.', 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=400&q=80',
                    'PT. Inovasi Digital', 'Web Developer Intern', '2023', '2024', 0,
                    'Mengembangkan halaman web sederhana dan memperbaiki bug aplikasi.', 'https://images.unsplash.com/photo-1516321497487-e288fb19713f?auto=format&fit=crop&w=400&q=80'
                ))

            cur.execute("SELECT COUNT(*) as cnt FROM projects")
            if cur.fetchone()['cnt'] == 0:
                cur.execute("""
                    INSERT INTO projects (title, description, tech_stack, image_url, demo_url, repo_url, is_featured)
                    VALUES (%s, %s, %s, %s, %s, %s, %s), (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    'Portfolio Website', 'Website portofolio interaktif berbasis Flask dan TiDB.', 'Python, Flask, HTML, CSS', 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=800&q=80', 'https://example.com', 'https://github.com', 1,
                    'Sistem Informasi Akademik', 'Aplikasi sederhana untuk mengelola data akademik.', 'Python, Flask, MySQL', 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=800&q=80', 'https://example.com', 'https://github.com', 0
                ))

        conn.commit()
    finally:
        conn.close()

def get_profiles():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM profiles")
            result = cur.fetchall()
        return result
    finally:
        conn.close()

def get_skills():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM skills")
            result = cur.fetchall()
        return result
    finally:
        conn.close()

def get_projects():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM projects")
            result = cur.fetchall()
        return result
    finally:
        conn.close()

def get_experience():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM experiences")
            result = cur.fetchall()
        return result
    finally:
        conn.close()
