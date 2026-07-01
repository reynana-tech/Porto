from flask import Blueprint, render_template, request, jsonify
from model import get_db
from Backend.admin.dashboard import login_required

skills_bp = Blueprint('skills', __name__)


@skills_bp.route('/admin/skills')
@login_required
def skills_page():
    return render_template('admin/skills.html')


@skills_bp.route('/api/admin/skills', methods=['GET'])
@login_required
def get_skills():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM skills ORDER BY category, name")
            data = cur.fetchall()
        return jsonify({'success': True, 'data': data})
    finally:
        conn.close()


@skills_bp.route('/api/admin/skills', methods=['POST'])
@login_required
def create_skill():
    data = request.get_json(silent=True) or {}
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO skills (name, category, level, icon) VALUES (%s,%s,%s,%s)",
                        (data.get('name'), data.get('category'), data.get('level', 80), data.get('icon')))
            cur.execute("SELECT * FROM skills ORDER BY id DESC LIMIT 1")
            saved = cur.fetchone()
        conn.commit()
        return jsonify({'success': True, 'message': 'Skill berhasil ditambahkan', 'data': saved})
    finally:
        conn.close()


@skills_bp.route('/api/admin/skills/<int:sid>', methods=['PUT'])
@login_required
def update_skill(sid):
    data = request.get_json()
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE skills SET name=%s, category=%s, level=%s, icon=%s WHERE id=%s",
                        (data.get('name'), data.get('category'), data.get('level', 80), data.get('icon'), sid))
        conn.commit()
        return jsonify({'success': True, 'message': 'Skill berhasil diupdate'})
    finally:
        conn.close()


@skills_bp.route('/api/admin/skills/<int:sid>', methods=['DELETE'])
@login_required
def delete_skill(sid):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM skills WHERE id=%s", (sid,))
        conn.commit()
        return jsonify({'success': True, 'message': 'Skill berhasil dihapus'})
    finally:
        conn.close()
