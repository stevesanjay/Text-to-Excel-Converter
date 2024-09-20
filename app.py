from flask import Flask, render_template, request, redirect
import pandas as pd
import os

app = Flask(__name__)

# Create an uploads folder if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_data():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        
        if uploaded_file.filename != '':
            
            text_file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(text_file_path)
            
            with open(text_file_path, 'r') as f:
                data = f.read()

            sections = data.strip().split("-------------")
            rows = []

            for section in sections:
                lines = section.strip().split("\n")
                name = lines[0].strip()
                github = lines[1].strip() if len(lines) > 1 else None
                linkedin = lines[2].strip() if len(lines) > 2 and "linkedin" in lines[2] else None
                kaggle = lines[3].strip() if len(lines) > 3 and "kaggle" in lines[3] else None
                
                rows.append({
                    "Name": name,
                    "GitHub": github,
                    "LinkedIn": linkedin,
                    "Kaggle": kaggle
                })

            df = pd.DataFrame(rows)
            excel_file = "mler_details.xlsx"
            df.to_excel(excel_file, index=False)

            return f"Data successfully saved to {excel_file} and {text_file_path}"

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
