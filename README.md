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

## **Visualizations**
A range of visualizations are generated to support analysis and understanding, including:
### Feature distributions
#### All Features
![outputAllFeatures.png](/images/outputAllFeatures.png)
#### Post-PCA Features
![outputPCA_Pariplot.png](/images/outputPCA_Pariplot.png)
### Player performance comparisons
![big3.png](/images/big3.png)
![RafaelNadal_elo_rating.png](/images/RafaelNadal_elo_rating.png)
![NovakDjokovic_elo_rating.png](/images/NovakDjokovic_elo_rating.png)
![RogerFederer_elo_rating.png](/images/RogerFederer_elo_rating.png)

## **Project Structure**
```bash
TennisPredict/
├── data/                   # Raw and processed datasets
├── images/                 # Graphs and visualizations
├── models/                 # Saved models and checkpoints
├── utils/                  # Utility functions for processing and evaluation
├── 0.CleanData.ipynb       # Data cleaning and exploration
├── 1.CreateDataset.ipynb   # Feature engineering and dataset preparation
├── 2.TrainModel.ipynb      # Model training and evaluation
├── 3.Predict.ipynb         # Match outcome predictions
├── requirements.txt        # Python dependencies
└── README.md               # Project overview
```
## **Getting Started**
1. **Clone the repository**
```bash
git clone https://github.com/MohammadYehya/TennisPredict.git
cd TennisPredict
```
2. **Create a virtual environment** *(optional but recommended)*
```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```
3. **Install the dependencies**
```bash
pip install -r requirements.txt
```
4. **Run the notebooks**
Launch your preferred IDE and run the notebooks in order:\
`0.CleanData.ipynb`\
`1.CreateDataset.ipynb`\
`2.TrainModel.ipynb`\
`3.Predict.ipynb`

