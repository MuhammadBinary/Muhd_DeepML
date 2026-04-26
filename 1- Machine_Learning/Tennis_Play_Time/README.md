# 🎾 Tennis Play Time Prediction

## Project Overview

This project implements a machine learning model to predict whether it is suitable to play tennis based on various weather conditions. Utilizing a classic decision tree algorithm, the model analyzes factors like Outlook, Temperature, Humidity, and Windiness to determine the optimal time for a tennis match. This serves as a foundational example of applying classification algorithms to simple, real-world decision-making scenarios.

## ✨ Features

*   **Data Loading & Exploration:** Loads and inspects the tennis dataset.
*   **Categorical Feature Encoding:** Converts categorical weather features into numerical representations suitable for machine learning.
*   **Decision Tree Classifier:** Trains a decision tree model to predict `PlayTennis` status.
*   **Prediction:** Makes predictions on new, unseen weather conditions.

## ⚙️ Technologies Used

*   **Python:** The core programming language.
*   **Pandas:** For data manipulation and analysis.
*   **NumPy:** For numerical operations.
*   **Scikit-learn:** For machine learning functionalities, specifically `OrdinalEncoder`, `LabelEncoder`, and `DecisionTreeClassifier`.

## 🚀 How It Works

1.  **Data Acquisition:** The project starts by loading the `Tennis_dataset.csv` file.
2.  **Data Preprocessing:**
    *   Categorical features (`Outlook`, `Temperature`, `Humidity`, `Windy`) are converted into numerical representations.
    *   `OrdinalEncoder` is used for `Outlook`, `Temperature`, and `Humidity` to preserve the ordinal relationship between categories.
    *   `LabelEncoder` is used for `Windy` (True/False) and the target variable `PlayTennis` (Yes/No).
3.  **Model Training:** A `DecisionTreeClassifier` is initialized and trained on the preprocessed features (`X`) and target variable (`y`).
4.  **Prediction:** The trained model can then predict whether tennis should be played given a new set of weather conditions.

## 📊 Project Structure

```
Tennis_Play_Time/
├── Good_Tennis_Time.ipynb   # Jupyter Notebook containing the data preprocessing and model training
├── Tennis_dataset.csv       # The dataset used for tennis play time prediction
└── README.md                # Project documentation
```

## 💻 Installation & Usage

### Prerequisites

*   Python 3.x
*   Jupyter Notebook (recommended for running the `.ipynb` file)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MuhammadBinary/Muhd_AI_repo.git
    cd Muhd_AI_repo/Machine_Learning/Tennis_Play_Time
    ```

2.  **Install dependencies:**
    ```bash
    pip install pandas numpy scikit-learn
    ```

### Running the Analysis

1.  **Open the Jupyter Notebook:**
    ```bash
    jupyter notebook Good_Tennis_Time.ipynb
    ```
2.  Run all cells in the notebook to see the data preprocessing steps, model training, and an example prediction.

## 💡 Future Enhancements

*   **Comparative Analysis:** Experiment with other classification algorithms (e.g., Logistic Regression, Support Vector Machines) and compare their performance.
*   **Hyperparameter Tuning:** Optimize the `DecisionTreeClassifier` parameters for better accuracy.
*   **Feature Importance Analysis:** Analyze which weather features are most influential in the decision-making process.
*   **Interactive Interface:** Create a simple web interface where users can input weather conditions and get a prediction.

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements or new features, please feel free to fork the repository and submit a pull request.
