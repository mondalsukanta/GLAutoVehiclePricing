# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""
Trains ML model using training dataset and evaluates using test dataset. Saves trained model.
"""
import os
import argparse
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import mlflow
import mlflow.sklearn

def select_first_file(path):

    files = os.listdir(path)
    return os.path.join(path,files[0])

def parse_args():
    '''Parse input arguments'''

    parser = argparse.ArgumentParser("train")
    
    # -------- WRITE YOUR CODE HERE --------
    
    # Step 1: Define arguments for train data, test data, model output, and RandomForest hyperparameters. Specify their types and defaults.  
    parser.add_argument("--train_dataset", type=str, help="Path to train dataset")
    parser.add_argument("--test_dataset", type=str, help="Path to test dataset")
    parser.add_argument("--n_estimators", type=int, default=100, help="The number of trees in the forest")
    parser.add_argument("--max_depth", type=int, default=None, help="Maximum depth of the tree")
    parser.add_argument("--model_output", type=str, help="Path to save the trained model")

    args = parser.parse_args()

    return args

def main(args):
    '''Read train and test datasets, train model, evaluate model, save trained model'''

    # -------- WRITE YOUR CODE HERE --------

    # Step 2: Read the train and test datasets from the provided paths using pandas. Replace '_______' with appropriate file paths and methods.  
    # load datasets
    train_df = pd.read_csv(select_first_file(args.train_dataset))
    test_df = pd.read_csv(select_first_file(args.test_dataset))
    # Step 3: Split the data into features (X) and target (y) for both train and test datasets. Specify the target column name.  
    y_train = train_df['price'] # specify the target column
    X_train = train_df.drop(columns=['price']) # drop the price column 
    y_test = test_df['price']
    X_test = test_df.drop(columns=['price'])    
    # Step 4: Initialize the RandomForest Regressor with specified hyperparameters, and train the model using the training data.  
    model = RandomForestRegressor(n_estimators=args.n_estimators, max_depth=args.max_depth, random_state=42)
    model.fit(X_train, y_train) # train the model
    # Step 5: Log model hyperparameters like 'n_estimators' and 'max_depth' for tracking purposes in MLflow.  
    mlflow.log_param("model", "Random Forest Regressor")
    mlflow.log_param("n_estimators", args.n_estimators)
    mlflow.log_param("max_depth", args.max_depth)
    # Step 6: Predict target values on the test dataset using the trained model, and calculate the mean squared error.  
    yhat_test = model.predict(X_test)
    mse = mean_squared_error(y_test, yhat_test) # compute and log mean squared error
    # Step 7: Log the MSE metric in MLflow for model evaluation, and save the trained model to the specified output path.  
    mlflow.log_metric("MSE", float(mse)) # log MSE
    print(f"Saving model to: {args.model_output}")
    mlflow.sklearn.save_model(sk_model=model, path=str(args.model_output))

if __name__ == "__main__":
    
    mlflow.start_run()

    # Parse Arguments
    args = parse_args()

    lines = [
        f"Train dataset input path: {args.train_data}",
        f"Test dataset input path: {args.test_data}",
        f"Model output path: {args.model_output}",
        f"Number of Estimators: {args.n_estimators}",
        f"Max Depth: {args.max_depth}"
    ]

    for line in lines:
        print(line)

    main(args)

    mlflow.end_run()

