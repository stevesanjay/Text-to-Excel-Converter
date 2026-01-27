from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def upload_data():
    rows = []  # list to store data for display

    if request.method == 'POST':
        uploaded_file = request.files['file']

        if uploaded_file and uploaded_file.filename != '':
            text_file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(text_file_path)

            with open(text_file_path, 'r') as f:
                data = f.read()

            sections = data.strip().split("-------------")

            for section in sections:
                lines = [l.strip() for l in section.strip().split("\n") if l.strip()]
                if not lines:
                    continue

                rows.append({
                    "Name": lines[0],
                    "GitHub": lines[1] if len(lines) > 1 else "",
                    "LinkedIn": lines[2] if len(lines) > 2 else "",
                    "Kaggle": lines[3] if len(lines) > 3 else ""
                })

            # Save Excel file
            df = pd.DataFrame(rows)
            df.to_excel("mler_details.xlsx", index=False)

            # ✅ Render template with rows instead of returning string
            return render_template('upload.html', rows=rows)

    # For GET requests
    return render_template('upload.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
