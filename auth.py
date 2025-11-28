from crm_app.db import connection
from crm_app.utils import normalize_phone

def check_auth(user_id: str, phone10: str) -> bool:
    if not user_id or not phone10: return False
    user_phone_norm = normalize_phone(phone10)
    if not user_phone_norm: return False

    try:
        with connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT phone FROM clients WHERE id = %s;", (user_id,))
                row = cur.fetchone()
                if not row: return False
                db_norm = normalize_phone(row[0])
                return db_norm == user_phone_norm
    except Exception as e:
        print("DB ERROR (auth):", e)
        return False
