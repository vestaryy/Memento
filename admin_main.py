import logging
import time
import os
from admin.db_audit import DatabaseAuditor
from admin.analytics import SemanticAnalyzer
from admin.activity import ActivityTracker

DB_PATH = 'db/assistant.db'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | [%(name)s] | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)

log_sys = logging.getLogger("SYSTEM")
log_db = logging.getLogger("DATABASE")
log_ana = logging.getLogger("ANALYTICS")

def run_admin_panel():
    auditor = DatabaseAuditor(DB_PATH)
    analyzer = SemanticAnalyzer(DB_PATH)
    tracker = ActivityTracker(DB_PATH)

    os.system('cls' if os.name == 'nt' else 'clear')
    log_sys.info("Запуск панели управления Memento Pro...")
    log_sys.info(f"Целевая база данных: {DB_PATH}")
    time.sleep(0.5)

    while True:
        print("\n" + "="*60)
        print("  MEMENTO ADMINISTRATIVE INTERFACE")
        print("="*60)
        print(" [1] Проверка статуса БД")
        print(" [2] Глубокий семантический анализ")
        print(" [3] Карта активности записей")
        print(" [0] Завершить сессию")
        print("-" * 60)

        choice = input()

        if choice == '1':
            log_db.info("Инициирована проверка целостности базы...")
            if auditor.check_connection():
                stats = auditor.get_general_stats()
                log_db.info("--- РЕЗУЛЬТАТЫ АУДИТА ---")
                log_db.info(f"Файл: {stats['db_name']} - СТАТУС: OK")
                log_db.info(f"Зарегистрировано пользователей: {stats['users']}")
                log_db.info(f"Всего воспоминаний в архиве: {stats['memories']}")
            else:
                log_db.error("КРИТИЧЕСКАЯ ОШИБКА: База данных assistant.db не найдена или повреждена!")

        elif choice == '2':
            log_ana.info("Запуск процесса обработки текстовых данных...")
            data = analyzer.get_text_metrics()
            if data:
                log_ana.info("--- СЕАНС АНАЛИТИКИ ЗАВЕРШЕН ---")
                log_ana.info(f"Средний объем воспоминания: {data['avg_len']} символов.")
                log_ana.info(f"Суммарный объем текста: {data['total_chars']} симв.")
                log_ana.info("Наиболее часто используемые теги/слова:")
                for word, count in data['top_words']:
                    log_ana.info(f"  > '{word}': {count} вхождений")
            else:
                log_ana.warning("Анализ невозможен: в базе данных отсутствуют текстовые описания.")


        elif choice == '3':
            log_sys.info("Сбор статистики по временным меткам...")
            report = tracker.get_time_report()
            days_data = report.get('days_dist')
            if days_data:
                log_sys.info("--- ПО ДНЯМ НЕДЕЛИ ---")
                for day, count in days_data.items():
                    log_sys.info(f"{day.ljust(10)} | {'█' * count} ({count} зап.)")

            else:

                log_sys.warning("Данные об активности отсутствуют.")


        elif choice == '0':
            log_sys.info("Закрытие административного доступа...")
            log_sys.info("Сессия успешно завершена. До свидания!")
            break
        
        else:
            log_sys.error("Введена неверная команда. Повторите попытку.")

if __name__ == "__main__":
    try:
        run_admin_panel()
    except KeyboardInterrupt:
        log_sys.warning("\nПринудительное завершение работы пользователем.")
