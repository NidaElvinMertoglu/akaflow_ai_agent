import pandas as pd
import sqlite3


STUDENT_COLUMNS = ['ogrenci_id', 'yas', 'egitim_durumu', 'kurs_turu', 
    'kurs_suresi_hafta', 'kayitli_oldugu_hafta_sayisi', 
    'haftalik_ders_saati', 'toplam_ders_saati', 
    'son_giristen_beri_gun_sayisi', 'son_30_gun_giris_sayisi', 
    'son_30_gun_ai_etkilesim_sayisi', 'tamamlanan_odev_orani', 
    'memnuniyet_skoru', 'is_churn']

PAYMENT_COLUMNS = ['ogrenci_id', 'toplam_ucret', 'odenen_tutar', 
    'kalan_borc', 'taksit_sayisi', 'son_odeme_gecikme_gun_sayisi', 
    'odeme_yontemi']

ATTENDANCE_COLUMNS = ['ogrenci_id', 'devamsizlik_saati', 
    'devamsizlik_orani', 'ust_uste_devamsizlik_sayisi']


def init_db():

    df = pd.read_csv('data/student_churn_dataset_v2.csv')


    conn = sqlite3.connect('data/student_data.db')


    df[STUDENT_COLUMNS].to_sql('students', conn, if_exists='replace', index=False)
    df[PAYMENT_COLUMNS].to_sql('payments', conn, if_exists='replace', index=False)
    df[ATTENDANCE_COLUMNS].to_sql('attendance', conn, if_exists='replace', index=False)

    conn.close()
    print("Pipeline Tamamlandı: CSV -> SQL aktarımı başarılı (3 tablo: students, payments, attendance).")


if __name__ == "__main__":
    init_db()