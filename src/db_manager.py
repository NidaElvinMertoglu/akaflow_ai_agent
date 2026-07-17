import pandas as pd
import sqlite3


def init_db():

    df = pd.read_csv('data/student_churn_dataset_v2.csv')


    conn = sqlite3.connect('data/student_data.db')


    df.to_sql('students', conn, if_exists='replace', index=False)

    conn.close()
    print("Pipeline Tamamlandı: CSV -> SQL aktarımı başarılı.")


if __name__ == "__main__":
    init_db()