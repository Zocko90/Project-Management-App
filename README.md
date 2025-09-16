# Project Management App

A simple command-line Project Management application written in Python using SQLite.  
Manage your projects with CRUD operations, search, filter, sort, and export to CSV.

---

## Features

- Add, list, update, delete projects
- Mark projects as complete
- Search projects by title
- Filter projects by status (`todo`, `in_progress`, `done`)
- Sort projects by deadline
- Export projects to CSV
- Robust logging and error handling

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/project-management-app.git
cd project-management-app
Usage

Run the CLI menu:

python main.py


Example interaction:

--- Project Management Menu ---
1. Add Project
2. List Projects
3. Update Project
4. Delete Project
5. Mark Project Complete
6. Search by Title
7. Filter by Status
8. Sort by Deadline
9. Export to CSV
0. Exit
Choose an option: 1
Title: Build Portfolio Website
Description: Create personal portfolio site with Python projects
Priority (1-5, default 3): 2
Deadline (YYYY-MM-DD, optional): 2025-09-30
Project 'Build Portfolio Website' added.


List projects:

ID:1 | Title: Build Portfolio Website | Status: todo | Priority: 2 | Deadline: 2025-09-30

Screenshots

Menu view:

List view:

Optional GIF demonstrating add/list:

Logging

All events and errors are logged to app.log.

License

MIT License


---

Saveti:  
1. Dodaj **screenshotove i GIF** u folder `screenshots/` unutar repo.  
2. GIF može biti **kratak 5–10 sekundi** koji pokazuje kako dodaješ i listuješ projekat.  
3. README je **potpuno na engleskom** i jasan za portfolio — recruiter odmah vidi da znaš Python, SQLite, CLI, error handling i logging.  

