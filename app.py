from flask import Flask, render_template, request, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)

# Temporary storage for Excel in memory
excel_data = None

@app.route('/', methods=['GET', 'POST'])
def upload_data():
    global excel_data
    rows = []

    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file and uploaded_file.filename != '':
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
            excel_data = output  # Save for download

            return render_template('upload.html', rows=rows, excel_ready=True)

    return render_template('upload.html', rows=rows, excel_ready=False)


@app.route('/download')
def download_excel():
    global excel_data
    if excel_data:
        excel_data.seek(0)
        return send_file(excel_data, download_name="mler_details.xlsx", as_attachment=True)
    return "No Excel file available.", 404


if __name__ == '__main__':
    app.run(debug=True)
