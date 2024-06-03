import pandas as pd
from flask import Flask, render_template
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def generate_graph(data, title):
    path_counter = data['Path'].value_counts()
    x_labels = path_counter.index.tolist()
    y_values = path_counter.tolist()

    # Define custom colors and bar width for each path
    colors = {'a': 'blue', 'b': 'green', 'c': 'red'}
    bar_width = 0.5

    plt.figure(figsize=(10, 6))
    plt.bar(x_labels, y_values, color=[colors[path] for path in x_labels], width=bar_width)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Convert plot to base64 for embedding in HTML
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    plt.close()

    return plot_url

@app.route('/')
def index():
    df = pd.read_csv("Safety_score_dataset.csv")  # Replace "your_file.csv" with the path to your CSV file
    unique_combinations = df.groupby(['DepartureAirport', 'Arrival Airport']).size().reset_index(name='Count')
    graphs = {}

    for index, row in unique_combinations.iterrows():
        departure = row['DepartureAirport']
        arrival = row['Arrival Airport']
        filtered_data = df[(df['DepartureAirport'] == departure) & (df['Arrival Airport'] == arrival)]
        title = f"From {departure} to {arrival}"
        graphs[title] = generate_graph(filtered_data, title)

    return render_template('graph.html', graphs=graphs)

if __name__ == '__main__':
    app.run(debug=True)
