from flask import Flask, render_template, request, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_data():
    rows = []

    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file and uploaded_file.filename != '':
            # Read file directly from memory
            data = uploaded_file.read().decode('utf-8')

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

            # Create Excel in memory
            df = pd.DataFrame(rows)
            output = BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)

            # Return Excel for download
            return send_file(output, download_name="mler_details.xlsx", as_attachment=True)

    return render_template('upload.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
