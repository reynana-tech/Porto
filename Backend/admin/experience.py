from flask import Blueprint, render_template, request, jsonify
from model import get_db
from Backend.admin.dashboard import login_required

experience_bp = Blueprint('experience', __name__)


@experience_bp.route('/admin/experience')
@login_required
def experience_page():
    return render_template('admin/experience.html')


@experience_bp.route('/api/admin/experiences', methods=['GET'])
@login_required
def get_experiences():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM experiences ORDER BY is_current DESC, id DESC")
            data = cur.fetchall()
        return jsonify({'success': True, 'data': data})
    finally:
        conn.close()


@experience_bp.route('/api/admin/experiences', methods=['POST'])
@login_required
def create_experience():
    data = request.get_json(silent=True) or {}
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO experiences (company, position, start_date, end_date, is_current, description, logo_url)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (data.get('company'), data.get('position'), data.get('start_date'),
                  data.get('end_date'), data.get('is_current', 0), data.get('description'), data.get('logo_url')))
            cur.execute("SELECT * FROM experiences ORDER BY id DESC LIMIT 1")
            saved = cur.fetchone()
        conn.commit()
        return jsonify({'success': True, 'message': 'Pengalaman berhasil ditambahkan', 'data': saved})
    finally:
        conn.close()


@experience_bp.route('/api/admin/experiences/<int:eid>', methods=['PUT'])
@login_required
def update_experience(eid):
    data = request.get_json()
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE experiences SET company=%s, position=%s, start_date=%s, end_date=%s,
                is_current=%s, description=%s, logo_url=%s WHERE id=%s
            """, (data.get('company'), data.get('position'), data.get('start_date'),
                  data.get('end_date'), data.get('is_current', 0), data.get('description'), data.get('logo_url'), eid))
        conn.commit()
        return jsonify({'success': True, 'message': 'Pengalaman berhasil diupdate'})
    finally:
        conn.close()


@experience_bp.route('/api/admin/experiences/<int:eid>', methods=['DELETE'])
@login_required
def delete_experience(eid):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM experiences WHERE id=%s", (eid,))
        conn.commit()
        return jsonify({'success': True, 'message': 'Pengalaman berhasil dihapus'})
    finally:
        conn.close()
