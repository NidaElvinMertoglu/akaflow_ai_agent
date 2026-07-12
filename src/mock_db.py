import sqlite3
from ai_agent.config import STUDENT_TABLE, CHURN_SCORE_COLUMN, IS_CHURN_COLUMN


def run_mock_setup():

    conn = sqlite3.connect("akaflow_mock.db")
    cursor = conn.cursor()

    # Şimdilik  geçici tablo
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {STUDENT_TABLE} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        {CHURN_SCORE_COLUMN} REAL,
        {IS_CHURN_COLUMN} INTEGER
    )""")

    # Test verilerini
    cursor.execute(f"SELECT COUNT(*) FROM {STUDENT_TABLE}")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            f"INSERT INTO {STUDENT_TABLE} (name, {CHURN_SCORE_COLUMN}, {IS_CHURN_COLUMN}) VALUES ('Ahmet Yılmaz', 0.88, 1)")
        cursor.execute(
            f"INSERT INTO {STUDENT_TABLE} (name, {CHURN_SCORE_COLUMN}, {IS_CHURN_COLUMN}) VALUES ('Ayşe Demir', 0.12, 0)")
        print("Sahte veriler başarıyla eklendi!")

    conn.commit()
    conn.close()
    print("Geçici test veri tabanı hazır!")


if __name__ == "__main__":
    run_mock_setup()