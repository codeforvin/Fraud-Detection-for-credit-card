import os
import nbformat
from nbclient import NotebookClient
from flask import Flask, request, render_template, send_from_directory
import uuid
import shutil
import json
import base64

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def run_notebook(notebook_path, dataset_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Replace placeholder
    for cell in nb.cells:
        if cell.cell_type == 'code' and 'DATASET_PATH' in cell.source:
            cell.source = cell.source.replace('DATASET_PATH', f"'{dataset_path}'")

    # Force the kernel metadata
    if 'metadata' in nb and 'kernelspec' in nb['metadata']:
        nb['metadata']['kernelspec']['name'] = 'python3'
        nb['metadata']['kernelspec']['display_name'] = 'Python 3'

    client = NotebookClient(nb, kernel_name='python3')

    try:
        client.execute()
    except Exception as e:
        return f"⚠️ Notebook execution failed with error:\n\n{str(e)}", [], {}

    # Collect outputs
    final_outputs = []
    images = []
    metrics = {}  # Placeholder for metrics

    for cell in nb.cells:
        if 'outputs' in cell:
            for output in cell.outputs:
                if output.output_type == 'stream':
                    final_outputs.append(output.text)
                elif output.output_type == 'execute_result':
                    final_outputs.append(output['data'].get('text/plain', ''))
                elif output.output_type == 'display_data' and 'image/png' in output.data:
                    # Save image from output
                    image_filename = f"{uuid.uuid4()}.png"
                    with open(os.path.join(UPLOAD_FOLDER, image_filename), 'wb') as f:
                        f.write(base64.b64decode(output.data['image/png']))
                    images.append(image_filename)
                elif output.output_type == 'execute_result' and 'text/plain' in output.data:
                    # Example: Extract metrics like accuracy, precision, recall, etc.
                    if "Accuracy" in output.data['text/plain']:
                        metrics['Accuracy'] = output.data['text/plain'].strip()
                    elif "Precision" in output.data['text/plain']:
                        metrics['Precision'] = output.data['text/plain'].strip()
                    elif "Recall" in output.data['text/plain']:
                        metrics['Recall'] = output.data['text/plain'].strip()

    return "\n".join(final_outputs), images, metrics

# Flask route to upload notebook and dataset, run the notebook and show results
@app.route('/')
def index():
    return render_template('index.html', result=None, images=None, metrics=None)

@app.route('/predict', methods=['POST'])
def predict():
    if 'notebook' not in request.files or 'dataset' not in request.files:
        return "Please upload both a notebook and a dataset."
    
    notebook_file = request.files['notebook']
    dataset_file = request.files['dataset']
    notebook_filename = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.ipynb")
    dataset_filename = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.csv")
    
    notebook_file.save(notebook_filename)
    dataset_file.save(dataset_filename)
    
    result, images, metrics = run_notebook(notebook_filename, dataset_filename)
    
    return render_template('index.html', result=result, images=images, metrics=metrics)

# Route to serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
