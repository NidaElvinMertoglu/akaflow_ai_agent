from apscheduler.schedulers.blocking import BlockingScheduler
from src.db_manager import init_db
import logging

# Loglama ayarları
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def job():
    logging.info("Otomatik veritabanı güncelleme işi başladı.")
    try:
        init_db()
        logging.info("Veritabanı başarıyla güncellendi.")
    except Exception as e:
        logging.error(f"Veritabanı güncellenirken hata oluştu: {e}")

# Zamanlayıcıyı ayarlama
scheduler = BlockingScheduler()
# Her gece saat 03:00'te çalışması için
scheduler.add_job(job, 'cron', hour=3, minute=0)



if __name__ == "__main__":
    logging.info("Scheduler başlatıldı. Her gece 03:00'te çalışacak.")
    scheduler.start()