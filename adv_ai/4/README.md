# Credit Card Fraud Detection with PyOD AutoEncoder

This project demonstrates unsupervised fraud detection with the AutoEncoder anomaly detector from [PyOD](https://pyod.readthedocs.io/). The model learns to reconstruct legitimate credit card transactions. Transactions with larger reconstruction errors receive higher anomaly scores and can be flagged for review.

## Project files

- `fraud_detection_autoencoder.ipynb` — data preparation, model training, threshold calibration, evaluation, and plots.
- `requirements.txt` — Python package dependencies.
- `creditcard.csv` — dataset file to download separately; it is not included in this project folder.

## Dataset

Download the anonymized credit card transactions dataset from [Kaggle](https://www.kaggle.com/datasets/whenamancodes/fraud-detection), extract `creditcard.csv`, and place it beside the notebook. The notebook expects a binary `Class` column, where `0` means legitimate and `1` means fraud. Numeric columns other than `Class` are used as model features.

The notebook reports the row and class counts when loaded. Confirm that these match the data you intend to analyze. The reviewed run contained 91,199 rows and 211 fraud cases, which is smaller than the commonly distributed full version of this dataset.

## Setup

Use Python 3.10 or newer and create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate     # Windows PowerShell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Launch JupyterLab and open the notebook:

```bash
jupyter lab
```

Run the notebook cells from top to bottom. Training runs on CPU by default and may take a few minutes depending on the data and machine.

## Notebook workflow

1. Loads the CSV, validates the target, and selects numeric features.
2. Splits the data into stratified training and held-out test partitions.
3. Reserves legitimate training rows for threshold calibration; fits imputation and scaling only from the model-fit rows.
4. Fits PyOD AutoEncoder on legitimate transactions only.
5. Sets the alert cutoff at the 99.5th percentile of the legitimate calibration scores, targeting an approximate 0.5% false-positive rate on similar legitimate transactions.
6. Reports ROC-AUC, average precision, confusion matrix, precision, recall, and plots the score distributions and Precision–Recall curve.

## Interpreting results

Fraud cases are rare, so accuracy can appear high even when a model misses fraud. Consider average precision and the Precision–Recall curve to assess how precision changes as recall increases. At a selected cutoff, inspect the confusion matrix and the number of alerts as well as fraud recall.

In the reviewed run on the 91,199-row dataset, ROC-AUC was 0.9536 and average precision was 0.6383. At the calibrated threshold, the model flagged 189 test transactions, including 55 of 63 fraud cases (about 87% recall and 29% precision). Those results are specific to that run and dataset. An anomaly score is a review signal, not proof of fraud; changing the threshold changes the balance between missed fraud and false alerts.

## Limitations

- Calibration assumes future legitimate transactions resemble the calibration data; changes in transaction patterns can alter the false-positive rate.
- Results from a subset may differ from results on the full dataset.
- The data is anonymized and historical and does not establish production performance or explain individual alerts.
- The threshold and model settings are educational starting points, not a production fraud policy.
