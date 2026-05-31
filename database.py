import sqlite3

DB_NAME = "health_records.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name   TEXT    NOT NULL,
            dob         TEXT    NOT NULL,
            email       TEXT    NOT NULL UNIQUE,
            glucose     REAL    NOT NULL,
            haemoglobin REAL    NOT NULL,
            cholesterol REAL    NOT NULL,
            remarks     TEXT,
            created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_patient(full_name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO patients (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks))
        conn.commit()
        conn.close()
        return True, "Patient added successfully!"
    except sqlite3.IntegrityError:
        return False, "A patient with this email already exists."
    except Exception as e:
        return False, f"Database error: {str(e)}"

def fetch_all_patients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def fetch_patient_by_id(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_patient(patient_id, full_name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE patients
            SET full_name=?, dob=?, email=?, glucose=?, haemoglobin=?, cholesterol=?, remarks=?
            WHERE id=?
        """, (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks, patient_id))
        conn.commit()
        conn.close()
        return True, "Patient record updated successfully!"
    except sqlite3.IntegrityError:
        return False, "Another patient with this email already exists."
    except Exception as e:
        return False, f"Database error: {str(e)}"

def delete_patient(patient_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
        conn.commit()
        conn.close()
        return True, "Patient record deleted successfully!"
    except Exception as e:
        return False, f"Database error: {str(e)}"

def search_patients(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM patients
        WHERE LOWER(full_name) LIKE ? OR LOWER(email) LIKE ?
        ORDER BY created_at DESC
    """, (f"%{query.lower()}%", f"%{query.lower()}%"))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]