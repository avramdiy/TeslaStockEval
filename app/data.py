from flask import Flask, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

@app.route('/load-csv', methods=['GET'])
def load_csv():
    try:
        # File path
        file_path = r"C:\\Users\\Ev\\Desktop\\TRG Week 12\\TSLA.csv"

        # Check if the file exists
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found at the specified path."}), 404

        # Load CSV into a DataFrame
        df = pd.read_csv(file_path)

        # Convert DataFrame to raw HTML table
        html_table = df.to_html(index=False, classes='table table-striped')

        return html_table

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)