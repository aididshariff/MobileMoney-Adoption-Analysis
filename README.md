# Mobile Money Adoption Analysis
This repository contains analysis of the **Global Findex Database 2025**, which provides data on financial inclusion and the use of digital financial services across more than 140 economies.  

The project is designed as a beginner-friendly workflow while also keeping a professional structure for reproducibility and future extensions.  


## Dataset  
- **Source**: Global Findex Database 2025 (World Bank)  
- **Note**: The underlying raw Findex microdata is proprietary and **not included** in this repository.


## Codebook  
The file `data/codebook/Findex_2025_codebook.csv` contains variable names, assigned categories, and descriptions to help interpret the dataset.




## Repository Structure
```
MobileMoney-Adoption-Analysis/
├── data/
│   ├── raw/          # Raw data (not included in repo)
│   ├── processed/    # Cleaned / transformed data
│   └── codebook/     # Variable categories & descriptions
├── docs/             # Documentation 
├── notebooks/        # Jupyter notebooks
├── scripts/          # Python scripts for automation
├── outputs/          # Charts, dashboards
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


## REPORT

**Final Model Evaluation: Linear Regression vs. Random Forest Regressor**

The project transitioned from a simple linear model to a powerful ensemble model to overcome data complexity and maximize predictive accuracy for Mobile Money Adoption.

1. **Linear Regression (OLS) Analysis:**
The corrected OLS model established**statistical inference** but failed at **prediction** due to violated assumptions.

**Performance & Assumption Check**
| Metric/Assumption |	Result | Interpretation |
| :--- | :---: | :--- |
| **R-squared ($\text{R}^2$)** | $0.127$ | **Poor Fit.** The model explains only $12.7\%$ of variance. |
| **VIF** | (Max Score)$< 5$ | **Stable.** Multicollinearity fixed; coefficients are reliable. |
| **Linearity** (Residuals) |	**Violated** |	Non-random pattern confirms a non-linear relationship. |

**Key Statistical Drivers ($\text{P} < 0.05$)**

|Feature | Coefficient (coef) | Rank in OLS | 
| :--- | :---: | :--- |
| **regionwb24_hi_Sub-Saharan Africa...** | $+0.0970$ | **1** |
| **year** | $+0.0414$ | **2** |
| **account_t_d** (Traditional Banking) | $+0.0396$ | **3** |

2. **Random Forest Regressor Analysis:**
The Random Forest model was chosen to address the non-linearity, resulting in a **massive improvement in predictive power.**

**Model Performance**

| Metric |	Linear Regression (Final) |	Random Forest Regressor	|Improvement |
| :--- | :---: | :---:| :--- |
| **R-squared ($\text{R}^2$)$** | 0.127$ | $0.6804 | $+534% **Increase** |
| **RMSE** | $0.1634$ | $0.0984$ | $\approx 40\%$ **Reduction in Error** |

**Key Predictive Drivers (Feature Importance):**
| Rank | Feature | Importance Score |	OLS P-value |
| :--- | :---: | :---: | :--- |
| **1** | **pop_adult** (Adult Population Size) | $0.311$ | $0.234$ (Not Significant) |
| **2** | **account_t_d** (Traditional Banking Access) | $0.237$ | $0.000$ (Highly Significant) |
| **3** | **internet** (Internet Penetration) | $0.180$ | $0.000$ (Highly Significant) |
| **4** | **year** (Time Trend) | $0.119$ | $0.000$ (Highly Significant) |

**Final Conclusion and Insights:**

1. Success of Non-Linear Modeling
The project successfully achieved its predictive goal. By correctly diagnosing the failure of the linear model and pivoting to the Random Forest Regressor, the model's accuracy surged, explaining over **two-thirds of the variance** in Mobile Money Adoption.

2. Contradictory Driver:**Adult Population** ($\text{pop\_adult}$)
The most valuable modeling insight is the contrasting role of Adult Population Size ($\text{pop\_adult}$):
    - The OLS model (straight-line assumption) dismissed it as insignificant.
    - The Random Forest model identified it as the **single most important predictor** ($\text{Importance} = 31.1\%$) for maximizing predictive accuracy.
This demonstrates that the relationship between population and adoption is highly non-linear, likely acting as a critical threshold or interacting with other features (like internet/banking access) in complex ways that only the Random Forest could capture.

3. Confirmed Foundational Drivers
The Random Forest confirmed the OLS findings that Traditional Banking Access ($\text{account\_t\_d}$) and Internet Penetration are foundational, positively correlated factors in driving mobile money adoption. The Sub-Saharan Africa region remains the most important feature, confirming its unique role in the global adoption landscape.




## Citation  
When using this dataset, please cite:  
**Klapper, L., Singer, D., Norris, A., & Starita, L. (2025). Global Findex Database 2025: Connectivity and Financial Inclusion in the Digital Economy. World Bank. DOI: https://doi.org/10.60572/rvnp-6q76**
