#!/bin/bash

# Create dataset with the latest data for 2023-24 season
cd src/Process-Data
echo "Running: python -m Get_Data"
echo "This command fetches data."
python -m Get_Data
echo "Running: python -m Get_Odds_Data"
echo "This command retrieves odds-related data."
python -m Get_Odds_Data
echo "Running: python -m Create_Games"
echo "This command creates game-related data."
python -m Create_Games

# Train models
echo "Changing directory to ../Train-Models"
cd ../Train-Models
echo "Running: python -m XGBoost_Model_ML"
python -m XGBoost_Model_ML
echo "Running: python -m XGBoost_Model_UO"
python -m XGBoost_Model_UO

git add -A
git commit -m "add new models"
git push
