# **TennisPredict**
An in-depth data analysis and notebook that allows users to set a tournament or select two tennis players and predict the match winner based on historical data, player statistics, and advanced machine learning models.

## **Dataset**
All the data can be found in the [data folder](https://github.com/MohammadYehya/TennisPredict/tree/main/data) which is a publicly available historical ATP tennis match dataset from [Jeff Sackmann’s Tennis Data](https://github.com/JeffSackmann/tennis_atp).

The original data contains matches from 1985 till 2024.\
Details about the columns features can be found in the [matches_data_dictionary.txt](https://github.com/MohammadYehya/TennisPredict/tree/main/data/matches_data_dictionary.txt) file and include about 49 features for the singles matches. Each year contains approximately 3000 matches.

> [!IMPORTANT]
> Post-cleaning and data transformation(feature augmentation, data merging, etc), the final dataset is the file [1finalDataset.csv](https://github.com/MohammadYehya/TennisPredict/tree/main/data/1finalDataset.csv) and is of the dimensions **(95376 x 68)**.

## **Machine Learning Models**
The following models are implemented:
- Decision Tree
- Random Forest
- Random Forest + GridSearchCV
- XGBoost
- XGBoost + GridSearchCV
- Sequential Neural Network

