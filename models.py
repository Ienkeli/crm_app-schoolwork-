from crm_app.db import connection

def get_full_name(user_id: str) -> str:
    try:
        with connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT full_name FROM clients WHERE id=%s;", (user_id,))
                row = cur.fetchone()
                if row:
                    return row[0]
    except Exception as e:
        print("DB ERROR (get_full_name):", e)
    return ""
