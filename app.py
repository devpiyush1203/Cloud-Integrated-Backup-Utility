from flask import Flask, request, render_template
from backup_engine import run_backup_pipeline

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    status_messages = []
    if request.method == 'POST':
        source = request.form.get('source')
        destination = request.form.get('destination')
        bucket = request.form.get('bucket')
        mode = request.form.get('backup_mode')

        # Logic call karna
        status_messages = run_backup_pipeline(source, destination, bucket, mode)
        return render_template("index.html", messages=status_messages)
    
    return render_template("index.html", messages=status_messages)

if __name__ == "__main__":
    app.run(debug=True)