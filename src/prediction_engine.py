import pandas as pd
import sqlite3
import joblib
import os
import logging

# 2. Loglama ayarlarını yap (Sadece bir kez yapılması yeterli)
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

DB_PATH = os.path.join(os.path.dirname(__file__), '../data/student_data.db')
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/final_logistic_model_v2.pkl')


def get_student_prediction(student_id: int):
    # Log: Tahmin isteği geldiğini kaydet
    logging.info(f"Tahmin isteği alındı: ogrenci_id={student_id}")

    conn = sqlite3.connect(DB_PATH)
    #injection hatası verdiği için bu 2 satır yerine alt 2 satırı kullandım
    #query = f"SELECT * FROM students WHERE ogrenci_id = {student_id}"
    #student_df = pd.read_sql(query, conn)
    
    query = """
        SELECT s.*, 
               p.toplam_ucret, p.odenen_tutar, p.kalan_borc, 
               p.taksit_sayisi, p.son_odeme_gecikme_gun_sayisi, 
               p.odeme_yontemi,
               a.devamsizlik_saati, a.devamsizlik_orani, 
               a.ust_uste_devamsizlik_sayisi
        FROM students s
        JOIN payments p ON s.ogrenci_id = p.ogrenci_id
        JOIN attendance a ON s.ogrenci_id = a.ogrenci_id
        WHERE s.ogrenci_id = ?
    """
    student_df = pd.read_sql(query, conn, params=(student_id,))

    conn.close()
    if student_df.empty:
        logging.warning(f"Öğrenci bulunamadı: ogrenci_id={student_id}")  # Log: Hata durumu
        return {"error": "Öğrenci bulunamadı"}

    model = joblib.load(MODEL_PATH)
    features = student_df.drop(columns=['ogrenci_id', 'is_churn', 'yas', 'egitim_durumu'], errors='ignore')

    prob = model.predict_proba(features)[0][1]

    # Kural tabanlı açıklamalar
    reasons = []
    if student_df['devamsizlik_orani'].values[0] > 0.3:
        reasons.append("Devamsızlık oranı yüksek.")
    if student_df['son_odeme_gecikme_gun_sayisi'].values[0] > 15:
        reasons.append("Ödeme gecikmesi kritik seviyede.")

    risk_status = "Riskli" if prob >= 0.40 else "Güvenli"

    # Log: Başarılı tahmin sonucunu kaydet
    logging.info(f"Tahmin tamamlandı: ogrenci_id={student_id}, Durum={risk_status}, Olasılık={round(prob, 2)}")

    return {
        "student_id": int(student_id),
        "churn_probability": round(float(prob), 2),
        "risk_status": risk_status,
        "reasons": reasons
    }