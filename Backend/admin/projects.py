from flask import Blueprint, render_template, request, jsonify
from model import get_db
from Backend.admin.dashboard import login_required

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('/admin/projects')
@login_required
def projects_page():
    return render_template('admin/projects.html')


@projects_bp.route('/api/admin/projects', methods=['GET'])
@login_required
def get_projects():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM projects ORDER BY is_featured DESC, id DESC")
            data = cur.fetchall()
        return jsonify({'success': True, 'data': data})
    finally:
        conn.close()


@projects_bp.route('/api/admin/projects', methods=['POST'])
@login_required
def create_project():
    data = request.get_json(silent=True) or {}
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO projects (title, description, tech_stack, image_url, demo_url, repo_url, is_featured)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (data.get('title'), data.get('description'), data.get('tech_stack'),
                  data.get('image_url'), data.get('demo_url'), data.get('repo_url'), data.get('is_featured', 0)))
            cur.execute("SELECT * FROM projects ORDER BY id DESC LIMIT 1")
            saved = cur.fetchone()
        conn.commit()
        return jsonify({'success': True, 'message': 'Proyek berhasil ditambahkan', 'data': saved})
    finally:
        conn.close()


@projects_bp.route('/api/admin/projects/<int:pid>', methods=['PUT'])
@login_required
def update_project(pid):
    data = request.get_json()
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE projects SET title=%s, description=%s, tech_stack=%s, image_url=%s,
                demo_url=%s, repo_url=%s, is_featured=%s WHERE id=%s
            """, (data.get('title'), data.get('description'), data.get('tech_stack'),
                  data.get('image_url'), data.get('demo_url'), data.get('repo_url'),
                  data.get('is_featured', 0), pid))
        conn.commit()
        return jsonify({'success': True, 'message': 'Proyek berhasil diupdate'})
    finally:
        conn.close()


@projects_bp.route('/api/admin/projects/<int:pid>', methods=['DELETE'])
@login_required
def delete_project(pid):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM projects WHERE id=%s", (pid,))
        conn.commit()
        return jsonify({'success': True, 'message': 'Proyek berhasil dihapus'})
    finally:
        conn.close()
