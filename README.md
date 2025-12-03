# Fraud-Detection-for-credit-card
This project allows users to upload a Jupyter Notebook and a dataset using a Flask web page. The server runs the notebook and shows all the results back on the site. It also includes a complete Credit Card Fraud Detection system that uses SMOTE, ensemble models, and clustering to improve accuracy, along with clear evaluation results.
1. Flask Notebook Runner
Key Features

Upload a Jupyter Notebook and dataset from the browser.

Server executes the notebook using NotebookClient.

Automatically replaces any placeholder (DATASET_PATH) inside the notebook.

Captures:

Text outputs

Printed results

Image outputs (JPEG/PNG)

Metrics (Accuracy, Precision, Recall)

Saves image outputs into uploads/.

Displays everything inside the web interface.

Tech Stack

Python

Flask

nbformat + nbclient

HTML templates

Base64 image decoding

How It Works

User uploads:

Notebook file (.ipynb)

Dataset (.csv)

Application stores both files in uploads/.

Notebook cells are scanned for the placeholder DATASET_PATH and replaced.

Notebook is executed with a Python 3 kernel.

Output is parsed, images are saved, and results are displayed.

2. Credit Card Fraud Detection Pipeline
Steps Included
2.1 Dataset Loading

Reads credit card dataset (2023 version).

Automatically identifies the target column.

2.2 Remove Highly Correlated Features

Correlation matrix computed.

Features > 0.9 correlation eliminated.

2.3 Train-Test Split

Stratified sampling.

80/20 split.

2.4 Scaling
StandardScaler applied to all features.

2.5 Clustering-Based Feature Engineering

KMeans clustering → added as an extra feature.
Fraud probability by cluster added.

2.6 Handling Imbalance with SMOTE
Oversamples minority fraud class.
Balances dataset for better learning.
2.7 Model Training

Models used:
Random Forest
AdaBoost
Soft Voting Ensemble
2.8 Cross-Validation
5-fold stratified CV

Accuracies reported with mean ± std deviation
2.9 Model Evaluation and Visualization
For each model:

Classification report

Accuracy score
Confusion matrix (saved as PNG)
ROC curve
Precision–Recall curve
Fraud vs Non-Fraud prediction summary

All confusion matrix images saved to:
uploads/
2.10 Saving Predictions

Outputs saved:
y_test.csv
rf_preds.csv
ab_preds.csv
ensemble_preds.csv

Folder Structure
project/
│── app.py                   # Flask app
│── templates/
│     └── index.html         # Frontend template
│── uploads/                 # Auto-saved notebook outputs & images
│── fraud_detection.py       # ML training pipeline
│── README.md
How to Run the Flask App
python app.py


Go to:

http://127.0.0.1:5000/
Upload the notebook and dataset.
How to Run the Fraud Detection Script
python fraud_detection.py


Outputs are saved automatically to uploads/.
Libraries Used

Flask
nbformat
nbclient
pandas
numpy
seaborn
matplotlib
scikit-learn
imbalanced-learn
uuid
base64
warnings

Use Cases
Automated notebook grading systems
Data science training platforms
Fraud detection research
Enterprise ML model evaluation
User-friendly personalized ML execution tools

Future Enhancements
Add async execution for large notebooks
GPU-enabled notebook execution
Add user authentication
Convert into a SaaS product for ML notebook execution
Add downloadable PDF report generation

