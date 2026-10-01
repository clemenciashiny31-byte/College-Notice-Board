# College Digital Notice Board

A simple web-based **College Digital Notice Board** where administrators can publish announcements and students can view them online.

## Features

### Student
- View all college announcements
- View notice details
- Notices are grouped by category
- Clean responsive interface

### Administrator
- Secure demo admin login
- Add/publish announcements
- View all published announcements
- Delete announcements
- SQLite database for storing notices

## Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Jinja2

## Project Structure

```text
College_Notice_Board/
│
├── app.py
├── requirements.txt
├── README.md
├── notice_board.db          # Created automatically after first run
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── notice_detail.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   └── add_notice.html
│
└── static/
    └── css/
        └── style.css
```

## How to Run

### 1. Open the project in VS Code

Extract the ZIP file and open the `College_Notice_Board` folder in VS Code.

### 2. Install Flask

Open the VS Code terminal:

```bash
pip install -r requirements.txt
```

### 3. Run the project

```bash
python app.py
```

### 4. Open in browser

```text
http://127.0.0.1:5000
```

## Admin Login

Open:

```text
http://127.0.0.1:5000/admin/login
```

Demo credentials:

```text
Username: admin
Password: admin123
```

## Project Flow

```text
Administrator
      |
      v
Admin Login
      |
      v
Admin Dashboard
      |
      v
Publish Announcement
      |
      v
SQLite Database
      |
      v
Digital Notice Board
      |
      v
Students View Announcements
```

## Note

This project is designed as a college project/demo. For production use, the admin credentials, secret key, database security, validation, and user authentication should be strengthened.
