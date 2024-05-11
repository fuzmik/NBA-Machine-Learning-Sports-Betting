#!/bin/bash

start_time=$(date +%l:%M:%S)

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
echo "Running: python -m Add_Days_Rest"
echo "This command adds days rest game-related data."
python -m Add_Days_Rest
# Train models
echo "Changing directory to ../Train-Models"
cd ../Train-Models
echo "Running: python -m XGBoost_Model_ML-edited"
python -m XGBoost_Model_ML-edited
echo "Running: python -m XGBoost_Model_UO-edited"
python -m XGBoost_Model_UO-edited

end_time=$(date +%l:%M:%S)
execution_time=$((end_time - start_time))
echo "Script execution time: $execution_time seconds"

git status

exit 0
