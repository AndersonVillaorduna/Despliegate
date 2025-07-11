from flask import Blueprint, request, jsonify
import datetime, uuid, os
from dotenv import load_dotenv
import google.generativeai as genai
from mini_db.conexion import conectar_db

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
pregunta_bp = Blueprint('pregunta_bp', __name__)

@pregunta_bp.route('/pregunta', methods=['POST'])
def procesar_pregunta():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        user_uid = data.get('user_uid')
        session_id = data.get('session_id')  # ⚠️ debe enviarse desde Angular

        if not prompt or not user_uid or not session_id:
            return jsonify({"error": "Faltan datos"}), 400

        model = genai.GenerativeModel('gemini-2.5-flash')
        respuesta = model.generate_content(prompt).text.strip()

        v_id = str(uuid.uuid4())
        conn = conectar_db()
        cursor = conn.cursor()

        # ✅ Verificar si la sesión ya existe
        cursor.execute("SELECT 1 FROM chat_session WHERE session_id = %s", (session_id,))
        existe = cursor.fetchone()

        # ✅ Si no existe, crear nueva sesión
        if not existe:
            cursor.execute("""
                INSERT INTO chat_session (session_id, student_id)
                VALUES (%s, %s)
            """, (session_id, user_uid))

        # ✅ Insertar mensaje en la sesión correspondiente
        cursor.execute("""
            INSERT INTO chat (v_id, v_title, student_id, respuesta, fecha, level_id, session_id)
            VALUES (%s, %s, %s, %s, %s, NULL, %s)
        """, (v_id, prompt, user_uid, respuesta, datetime.datetime.now(), session_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"respuesta": respuesta})

    except Exception as e:
        print(" Error interno:", str(e))
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Nuevo endpoint para crear sesión manualmente 
@pregunta_bp.route('/sesion', methods=['POST'])
def crear_sesion():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        student_id = data.get('student_id')

        if not session_id or not student_id:
            return jsonify({"error": "Faltan datos"}), 400

        conn = conectar_db()
        cursor = conn.cursor()

        # Insertar nueva sesión si no existe
        cursor.execute("SELECT 1 FROM chat_session WHERE session_id = %s", (session_id,))
        existe = cursor.fetchone()

        if not existe:
            cursor.execute("""
                INSERT INTO chat_session (session_id, student_id)
                VALUES (%s, %s)
            """, (session_id, student_id))
            conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Sesión registrada correctamente"})

    except Exception as e:
        print(" Error creando sesión:", str(e))
        return jsonify({"error": "Error creando sesión", "detalle": str(e)}), 500

#  Endpoint para obtener historial por sesión
@pregunta_bp.route('/historial/<session_id>/<student_id>', methods=['GET'])
def obtener_historial(session_id, student_id):
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT v_title, respuesta
            FROM chat
            WHERE session_id = %s AND student_id = %s
            ORDER BY fecha ASC
        """, (session_id, student_id))

        mensajes = cursor.fetchall()
        cursor.close()
        conn.close()

        historial = []
        for pregunta, respuesta in mensajes:
            historial.append({"de": "usuario", "texto": pregunta})
            historial.append({"de": "bot", "texto": respuesta})

        return jsonify(historial)

    except Exception as e:
        print("❌ Error al obtener historial:", str(e))
        return jsonify({"error": "Error al obtener historial", "detalle": str(e)}), 500
from flask import Blueprint, request, jsonify
import datetime, uuid, os
from dotenv import load_dotenv
import google.generativeai as genai
from mini_db.conexion import conectar_db

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
pregunta_bp = Blueprint('pregunta_bp', __name__)

@pregunta_bp.route('/pregunta', methods=['POST'])
def procesar_pregunta():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        user_uid = data.get('user_uid')
        session_id = data.get('session_id')  # ⚠️ debe enviarse desde Angular

        if not prompt or not user_uid or not session_id:
            return jsonify({"error": "Faltan datos"}), 400

        model = genai.GenerativeModel('gemini-2.5-flash')
        respuesta = model.generate_content(prompt).text.strip()

        v_id = str(uuid.uuid4())
        conn = conectar_db()
        cursor = conn.cursor()

        # ✅ Verificar si la sesión ya existe
        cursor.execute("SELECT 1 FROM chat_session WHERE session_id = %s", (session_id,))
        existe = cursor.fetchone()

        # ✅ Si no existe, crear nueva sesión
        if not existe:
            cursor.execute("""
                INSERT INTO chat_session (session_id, student_id)
                VALUES (%s, %s)
            """, (session_id, user_uid))

        # ✅ Insertar mensaje en la sesión correspondiente
        cursor.execute("""
            INSERT INTO chat (v_id, v_title, student_id, respuesta, fecha, level_id, session_id)
            VALUES (%s, %s, %s, %s, %s, NULL, %s)
        """, (v_id, prompt, user_uid, respuesta, datetime.datetime.now(), session_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"respuesta": respuesta})

    except Exception as e:
        print("❌ Error interno:", str(e))
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# ✅ Nuevo endpoint para crear sesión manualmente (si se desea desde Angular)
@pregunta_bp.route('/sesion', methods=['POST'])
def crear_sesion():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        student_id = data.get('student_id')

        if not session_id or not student_id:
            return jsonify({"error": "Faltan datos"}), 400

        conn = conectar_db()
        cursor = conn.cursor()

        # Insertar nueva sesión si no existe
        cursor.execute("SELECT 1 FROM chat_session WHERE session_id = %s", (session_id,))
        existe = cursor.fetchone()

        if not existe:
            cursor.execute("""
                INSERT INTO chat_session (session_id, student_id)
                VALUES (%s, %s)
            """, (session_id, student_id))
            conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Sesión registrada correctamente"})

    except Exception as e:
        print("❌ Error creando sesión:", str(e))
        return jsonify({"error": "Error creando sesión", "detalle": str(e)}), 500

# ✅ Endpoint para obtener historial por sesión
@pregunta_bp.route('/historial/<session_id>/<student_id>', methods=['GET'])
def obtener_historial(session_id, student_id):
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT v_title, respuesta
            FROM chat
            WHERE session_id = %s AND student_id = %s
            ORDER BY fecha ASC
        """, (session_id, student_id))

        mensajes = cursor.fetchall()
        cursor.close()
        conn.close()

        historial = []
        for pregunta, respuesta in mensajes:
            historial.append({"de": "usuario", "texto": pregunta})
            historial.append({"de": "bot", "texto": respuesta})

        return jsonify(historial)

    except Exception as e:
        print("❌ Error al obtener historial:", str(e))
        return jsonify({"error": "Error al obtener historial", "detalle": str(e)}), 500
@pregunta_bp.route('/sesiones/<student_id>', methods=['GET'])
def obtener_sesiones(student_id):
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT session_id, MAX(fecha) as ultima_fecha
            FROM chat
            WHERE student_id = %s
            GROUP BY session_id
            ORDER BY ultima_fecha DESC
        """, (student_id,))
        sesiones = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify([{"session_id": s[0], "ultima_fecha": s[1].isoformat()} for s in sesiones])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Subir pregunta desde el front.
@pregunta_bp.route('/SubirPregunta', methods=['POST'])
def subirPregunta():
    try:
        data = request.get_json()
        level_id = data.get('level_id')
        text_content = data.get('text_content')
        title = data.get('title')
        alt1 = data.get('alt1')
        alt2 = data.get('alt2')
        alt3 = data.get('alt3')
        alt4 = data.get('alt4')
        correct_alt = data.get('correct_alt')
        print(data)
        if not all([level_id, text_content, title, alt1, alt2, alt3, alt4, correct_alt]):
            return jsonify({"error": "Faltan datos"}), 400

        conn = conectar_db()
        cursor = conn.cursor()
        # Insertar nueva pregunta
        cursor.execute("""
                INSERT INTO questions (level_id, text_content, title,alt1,alt2,alt3,alt4,correct_alt)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (level_id, text_content,title, alt1, alt2, alt3, alt4, correct_alt))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Pregunta registrada correctamente"})

    except Exception as e:
        print("❌ Error creando pregunta:", str(e))
        return jsonify({"error": "Error creando pregunta", "detalle": str(e)}), 500
