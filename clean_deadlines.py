import sqlite3
from datetime import datetime
import logging

DB_NAME = "project_management.db"
LOG_FILE = "deadline_cleanup.log"

# Konfiguracija logovanja
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Lista formata koje želimo prepoznati
DATE_FORMATS = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"]

def parse_date(date_str):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None  # nevalidan datum

def clean_deadlines():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, deadline FROM projects")
    rows = cursor.fetchall()

    for project_id, title, deadline in rows:
        if deadline:
            new_deadline = parse_date(deadline)
            if new_deadline:
                if new_deadline != deadline:
                    # datum validan ali u pogrešnom formatu → konvertuj
                    cursor.execute(
                        "UPDATE projects SET deadline = ? WHERE id = ?",
                        (new_deadline, project_id)
                    )
                    msg = f"Project '{title}' deadline '{deadline}' → converted to '{new_deadline}'"
                    print(msg)
                    logging.info(msg)
            else:
                # nevalidan datum → postavi na NULL
                cursor.execute(
                    "UPDATE projects SET deadline = NULL WHERE id = ?",
                    (project_id,)
                )
                msg = f"Project '{title}' had invalid deadline '{deadline}' → set to NULL"
                print(msg)
                logging.warning(msg)
        else:
            # prazno ili NULL → ostaje NULL
            pass

    conn.commit()
    conn.close()
    final_msg = "All deadlines cleaned. Sort by Deadline should now work correctly."
    print(final_msg)
    logging.info(final_msg)

if __name__ == "__main__":
    clean_deadlines()



