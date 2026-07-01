from flask import Blueprint, render_template, jsonify
from model import get_db

utama_bp = Blueprint('utama', __name__)


@utama_bp.route('/health')
def health():
    return jsonify({'success': True, 'status': 'ok'})


@utama_bp.route('/api/profile')
def api_profile():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM profiles ORDER BY id DESC LIMIT 1")
            profile = cur.fetchone()
        return jsonify({'success': True, 'data': profile})
    finally:
        conn.close()


@utama_bp.route('/api/skills')
def api_skills():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM skills ORDER BY category, level DESC")
            skills = cur.fetchall()
        return jsonify({'success': True, 'data': skills})
    finally:
        conn.close()


@utama_bp.route('/api/experiences')
def api_experiences():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM experiences ORDER BY is_current DESC, id DESC")
            exps = cur.fetchall()
        return jsonify({'success': True, 'data': exps})
    finally:
        conn.close()


@utama_bp.route('/api/projects')
def api_projects():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM projects ORDER BY is_featured DESC, id DESC")
            projects = cur.fetchall()
        return jsonify({'success': True, 'data': projects})
    finally:
        conn.close()
