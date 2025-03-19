import sqlite3

async def generate_report(db):
    """Vygeneruje prehľad nabíjacích relácií."""
    with sqlite3.connect(db.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date(timestamp), vehicle_id, user_id, COUNT(*) FROM sessions
            GROUP BY date(timestamp), vehicle_id, user_id
            ORDER BY date(timestamp) DESC LIMIT 10
        """)
        rows = cursor.fetchall()
        report = "\n".join(
            [f"{date}: Vehicle {vid} - User {uid} ({count}x)"
             for date, vid, uid, count in rows]
        )
        return report if report else "Žiadne dáta"
