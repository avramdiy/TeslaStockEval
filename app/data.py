from flask import Flask, jsonify, request
import pandas as pd
import os
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Global file path
file_path = r"C:\\Users\\Ev\\Desktop\\TRG Week 12\\TSLA.csv"

# Load CSV into a DataFrame
def load_data():
    if not os.path.exists(file_path):
        raise FileNotFoundError("File not found at the specified path.")
    return pd.read_csv(file_path)

# Helper function to generate plots
def generate_plot(plot_func):
    img = io.BytesIO()
    plot_func()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

@app.route('/load-csv', methods=['GET'])
def load_csv():
    try:
        df = load_data()
        html_table = df.to_html(index=False, classes='table table-striped')
        return html_table
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/visualization/line', methods=['GET'])
def line_plot():
    try:
        df = load_data()
        def plot():
            df.plot(x='Date', y='Close', title='Line Plot of Closing Prices')
            plt.xlabel('Date')
            plt.ylabel('Close Price')
        plot_url = generate_plot(plot)
        return f'<img src="data:image/png;base64,{plot_url}"/>'
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/visualization/bar', methods=['GET'])
def bar_plot():
    try:
        df = load_data()
        def plot():
            df.head(10).plot.bar(x='Date', y='Volume', title='Bar Plot of Volume (Top 10 Days)')
            plt.xlabel('Date')
            plt.ylabel('Volume')
        plot_url = generate_plot(plot)
        return f'<img src="data:image/png;base64,{plot_url}"/>'
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)