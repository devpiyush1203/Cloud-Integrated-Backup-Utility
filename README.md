# 🚀 Automated Cloud-Integrated Backup Utility

A robust DevOps tool designed to automate the backup process of local directories to both local storage (like OneDrive/Local Disk) and AWS S3 Cloud. Featuring a user-friendly Flask-based web interface and comprehensive logging.

## 🌟 Features
- **Hybrid Backup Mode:** Option to back up locally, to AWS S3, or both.
- **Smart Compression:** Automatically creates timestamped ZIP archives.
- **Web Portal:** Clean UI to manage backup paths and configurations.
- **Cloud Integration:** Securely uploads data to AWS S3 using Boto3.
- **Retention Management:** Automatically cleans up old local backups (keeps last 5).
- **Audit Logging:** Detailed logs of every execution in `devops_backup.log`.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Web Framework:** Flask
- **Cloud Provider:** AWS (S3 Service)
- **Libraries:** Boto3, Shutil, Logging, Jinja2

## 📁 Project Structure
```text
├── app.py                # Flask Web Application
├── backup_engine.py      # Core Backup Logic (Zip & Upload)
├── templates/
│   └── index.html        # Web UI Template
├── devops_backup.log     # Execution Logs (Generated)
└── requirements.txt      # List of Dependencies