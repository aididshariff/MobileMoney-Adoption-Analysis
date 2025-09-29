# Mobile Money Adoption Analysis
This repository contains analysis of the **Global Findex Database 2025**, which provides data on financial inclusion and the use of digital financial services across more than 140 economies.  

The project is designed as a beginner-friendly workflow while also keeping a professional structure for reproducibility and future extensions.  


## Dataset  
- **Source**: Global Findex Database 2025 (World Bank)  
- **Note**: The underlying raw Findex microdata is proprietary and **not included** in this repository.


## Codebook  
The file `data/codebook/Findex_2025_codebook.csv` contains variable names, assigned categories, and descriptions to help interpret the dataset.


## Planned Analysis Workflow  

This is a step-by-step roadmap. Tasks will be marked when completed.  

- [x] **Baseline: Financial Inclusion Levels**  
  - Share of adults with an account (any, bank, or mobile money)  
  - Country and regional summaries  

- [ ] **Digital Finance Adoption**  
  - Mobile account usage  
  - Digital payments (sending/receiving money, paying bills, remittances)  

- [ ] **Borrowing, Savings, and Insurance Behavior**  
  - Borrowing sources (formal, informal, family/friends)  
  - Saving patterns (formal vs. informal)  
  - Insurance uptake  

- [ ] **Barriers to Financial Access**  
  - Reasons for being unbanked (cost, documentation, trust, distance, etc.)  

- [ ] **Gaps & Inequalities**  
  - Gender gap in account ownership  
  - Differences by income group, education, or region  

- [ ] **Policy & Practice Implications**  
  - Summarize insights that matter for financial inclusion strategie



## Analysis Goals
The main analysis will focus on answering questions like:
1. **Demographics & Adoption** – How do age, gender, and location affect mobile money usage?
2. **Education & Adoption** – Are people with higher education more likely to use mobile money?
3. **Income & Poverty Levels** – Is mobile money adoption higher among certain income groups?
4. **Mobile Money & Financial Inclusion** – How does mobile money improve access to financial services?
5. **Trends** – Are adoption rates changing over time?


## Repository Structure
```
MobileMoney-Adoption-Analysis/
├── data/
│   ├── raw/          # Raw data (not included in repo)
│   ├── processed/    # Cleaned / transformed data
│   └── codebook/     # Variable categories & descriptions
├── docs/             # Documentation (workflow, setup, analysis plan)
├── notebooks/        # Jupyter notebooks
├── scripts/          # Python scripts for automation
├── outputs/          # Charts, reports, dashboards
├── README.md         # Project documentation
└── requirements.txt  # Python dependencies

```


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
