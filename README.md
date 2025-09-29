# Mobile Money Adoption Analysis
This project explores **mobile money adoption in Kenya** using survey data. The goal is to practice **data cleaning, analysis and visualization** with a real-world dataset.

## Analysis Goals
The main analysis will focus on answering questions like:
1. **Demographics & Adoption** – How do age, gender, and location affect mobile money usage?
2. **Education & Adoption** – Are people with higher education more likely to use mobile money?
3. **Income & Poverty Levels** – Is mobile money adoption higher among certain income groups?
4. **Mobile Money & Financial Inclusion** – How does mobile money improve access to financial services?
5. **Trends** – Are adoption rates changing over time?

## Project Overview
- Understand how education, age, gender, and income affect mobile     money usage.
- Clean messy survey data (missing values, inconsistent text, duplicates).
- Explore adoption trends using Python (Pandas, Matplotlib, Seaborn).
- Visualize key insights with graphs and tables.

## Project Structure
```
project_name/
├── data/
│ ├── raw/ # Raw data (not included in repo)
│ ├── processed/ # Cleaned / transformed data
│ └── codebook/ # Variable categories & descriptions
├── notebooks/ # Jupyter notebooks
├── scripts/ # Python scripts for automation
├── outputs/ # Charts, reports, dashboards
├── README.md # Project documentation
└── requirements.txt # Python dependencies
```
## Codebook
The file `data/codebook/Findex_2025_codebook.csv` contains variable names, assigned categories, and descriptions to help interpret the dataset.  
Note: The underlying raw Findex microdata is proprietary and **not included** in this repository.

## Tools & Libraries
- **Python 3**
- **Pandas** – for data cleaning & manipulation
- **Matplotlib, Seaborn & Tableau** – for data visualization and dashboard
- **Jupyter Notebook** – to run the analysis step by step
- **Git & GitHub** – version control and project sharing

## Getting Started
1. Clone this repository:
``` 
git clone git@github.com:aididshariff/MobileMoney-Adoption-Analysis.git
cd MobileMoney-Adoption-Analysis
```
2. Install the required Python libraries:
```
pip install -r requirements.txt
```
3. Open Jupyter Notebook:
```  jupyter notebook ```
4. Run the notebooks in order ``` (01_cleaning.ipynb → 02_analysis.ipynb → 03_visualization.ipynb)```.
