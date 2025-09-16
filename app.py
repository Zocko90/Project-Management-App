import sqlite3
import csv
import logging
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

DB_NAME = "project_management.db"

# -------------------------
# Helper: colored status
# -------------------------
def colored_status(status):
    if status == "todo":
        return Fore.YELLOW + status + Style.RESET_ALL
    elif status == "in_progress":
        return Fore.BLUE + status + Style.RESET_ALL
    elif status == "done":
        return Fore.GREEN + status + Style.RESET_ALL
    else:
        return status

# -------------------------
# Logging
# -------------------------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# -------------------------
# Database
# -------------------------
def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'todo',
            priority INTEGER DEFAULT 3,
            deadline TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT
        )
        """)
        conn.commit()
        logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {e}")
        print("Error initializing database. Check app.log for details.")
    finally:
        conn.close()

# -------------------------
# CRUD
# -------------------------
def add_project(title, description=None, status='todo', priority=3, deadline=None):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        created_at = datetime.utcnow().isoformat()
        cursor.execute("""
        INSERT INTO projects (title, description, status, priority, deadline, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, status, priority, deadline, created_at))
        conn.commit()
        logging.info(f"Project added: {title}")
    except sqlite3.Error as e:
        logging.error(f"Failed to add project '{title}': {e}")
        print(f"Error adding project '{title}'. Check app.log.")
    finally:
        conn.close()

def list_projects():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects")
        projects = cursor.fetchall()
        logging.info("Listed all projects.")
        return projects
    except sqlite3.Error as e:
        logging.error(f"Failed to list projects: {e}")
        print("Error listing projects. Check app.log.")
        return []
    finally:
        conn.close()

def update_project(project_id, title=None, description=None, status=None, priority=None, deadline=None):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        updated_at = datetime.utcnow().isoformat()

        fields = []
        values = []

        if title: fields.append("title = ?"); values.append(title)
        if description: fields.append("description = ?"); values.append(description)
        if status: fields.append("status = ?"); values.append(status)
        if priority: fields.append("priority = ?"); values.append(priority)
        if deadline: fields.append("deadline = ?"); values.append(deadline)

        fields.append("updated_at = ?")
        values.append(updated_at)
        values.append(project_id)

        query = f"UPDATE projects SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        logging.info(f"Project {project_id} updated.")
    except sqlite3.Error as e:
        logging.error(f"Failed to update project {project_id}: {e}")
        print(f"Error updating project {project_id}. Check app.log.")
    finally:
        conn.close()

def delete_project(project_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        logging.info(f"Project {project_id} deleted.")
    except sqlite3.Error as e:
        logging.error(f"Failed to delete project {project_id}: {e}")
        print(f"Error deleting project {project_id}. Check app.log.")
    finally:
        conn.close()

# -------------------------
# Search / Filter / Sort / Export
# -------------------------
def search_projects(keyword):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE title LIKE ?", ('%' + keyword + '%',))
        return cursor.fetchall()
    finally:
        conn.close()

def filter_projects(status):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE status = ?", (status,))
        return cursor.fetchall()
    finally:
        conn.close()

def sort_projects_by_deadline():
    """Return all projects sorted by deadline (earliest first). Projects without deadline go last."""
    projects = list_projects()
    
    def parse_deadline(p):
        deadline_str = p[5]  # index 5 = deadline
        if deadline_str:
            try:
                return datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError:
                return datetime.max
        return datetime.max
    
    projects_sorted = sorted(projects, key=parse_deadline)
    return projects_sorted

def export_projects_to_csv(filename="projects_export.csv"):
    try:
        projects = list_projects()
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Title", "Description", "Status", "Priority", "Deadline", "Created At", "Updated At"])
            writer.writerows(projects)
        print(f"All projects exported to {filename}")
        logging.info(f"Projects exported to {filename}")
    except Exception as e:
        logging.error(f"Failed to export projects: {e}")
        print("Error exporting projects. Check app.log.")

# -------------------------
# CLI Menu
# -------------------------
def menu():
    while True:
        print("\n--- Project Management Menu ---")
        print("1. Add Project")
        print("2. List Projects")
        print("3. Update Project")
        print("4. Delete Project")
        print("5. Mark Project Complete")
        print("6. Search by Title")
        print("7. Filter by Status")
        print("8. Sort by Deadline")
        print("9. Export to CSV")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Title: ").strip()
            description = input("Description (optional): ").strip()
            priority_input = input("Priority (1-5, default 3): ").strip()
            priority = int(priority_input) if priority_input.isdigit() else 3
            deadline_input = input("Deadline (YYYY-MM-DD, optional): ").strip()
            deadline = None
            if deadline_input:
                try:
                    datetime.strptime(deadline_input, "%Y-%m-%d")
                    deadline = deadline_input
                except ValueError:
                    print("Invalid date format. Deadline will be set to None.")
            add_project(title, description, priority=priority, deadline=deadline)
            print(f"Project '{title}' added.")

        elif choice == "2":
            projects = list_projects()
            if not projects:
                print("No projects found.")
            else:
                for p in projects:
                    print(f"ID:{p[0]} | Title:{p[1]} | Status:{colored_status(p[3])} | Priority:{p[4]} | Deadline:{p[5]}")

        elif choice == "3":
            project_id_input = input("Enter project ID to update: ").strip()
            if not project_id_input.isdigit():
                print("Invalid ID."); continue
            project_id = int(project_id_input)
            title = input("New title (leave blank to keep current): ").strip() or None
            description = input("New description (leave blank to keep current): ").strip() or None
            status = input("New status (todo/in_progress/done, leave blank to keep current): ").strip() or None
            priority_input = input("New priority (1-5, leave blank to keep current): ").strip()
            priority = int(priority_input) if priority_input.isdigit() else None
            deadline_input = input("New deadline (YYYY-MM-DD, leave blank to keep current): ").strip()
            deadline = None
            if deadline_input:
                try:
                    datetime.strptime(deadline_input, "%Y-%m-%d")
                    deadline = deadline_input
                except ValueError:
                    print("Invalid date format. Deadline will be ignored.")
            update_project(project_id, title, description, status, priority, deadline)
            print(f"Project ID {project_id} updated.")

        elif choice == "4":
            project_id_input = input("Enter project ID to delete: ").strip()
            if not project_id_input.isdigit():
                print("Invalid ID."); continue
            delete_project(int(project_id_input))
            print(f"Project ID {project_id_input} deleted.")

        elif choice == "5":
            project_id_input = input("Enter project ID to mark as complete: ").strip()
            if not project_id_input.isdigit():
                print("Invalid ID."); continue
            update_project(int(project_id_input), status="done")
            print(f"Project ID {project_id_input} marked as complete.")

        elif choice == "6":
            keyword = input("Enter keyword to search in title: ").strip()
            results = search_projects(keyword)
            for p in results:
                print(f"ID:{p[0]} | Title:{p[1]} | Status:{colored_status(p[3])} | Priority:{p[4]} | Deadline:{p[5]}")

        elif choice == "7":
            status = input("Enter status to filter (todo/in_progress/done): ").strip()
            results = filter_projects(status)
            for p in results:
                print(f"ID:{p[0]} | Title:{p[1]} | Status:{colored_status(p[3])} | Priority:{p[4]} | Deadline:{p[5]}")

        elif choice == "8":
            results = sort_projects_by_deadline()
            for p in results:
                print(f"ID:{p[0]} | Title:{p[1]} | Status:{colored_status(p[3])} | Priority:{p[4]} | Deadline:{p[5]}")

        elif choice == "9":
            export_projects_to_csv()

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("Invalid option. Please choose again.")

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    init_db()
    menu()



