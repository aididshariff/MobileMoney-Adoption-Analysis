# ==============================================================================
# 1. IMPORTS
# All toolkits needed for the entire analysis pipeline
# ==============================================================================
import pandas as pd
import numpy as np  
import seaborn as sns
import matplotlib.pyplot as plt
import os
from pathlib import Path
import traceback
import sys
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.ensemble import RandomForestRegressor
print("All libraries imported successfully.")

# ==============================================================================
# 2. MAIN EXECUTION FUNCTION
# This function orchestrates the entire analysis pipeline.
# ==============================================================================
def main():
    print("\n--- Pipeline started ---")
    
    # DEFINE PATHS AND CREATE DIRECTORIES
    # Resolve paths relative to the repository root (two levels up from this file)
    # This makes the script work no matter what the current working directory is
    base_dir = Path(__file__).resolve().parent.parent

    RAW_DATA_PATH = base_dir / 'data' / 'raw' / 'global_findex.csv'

    # Path for the final Tableau-ready CSV
    TABLEAU_OUTPUT_PATH = base_dir / 'data' / 'processed' / 'tableau_ready_data.csv'

    # Charts Folder
    OUTPUT_DIR_CHARTS = base_dir / 'outputs' / 'charts'

    # Model Summaries Folder (For .txt files like OLS and RF summaries)
    OUTPUT_DIR_SUMMARY = base_dir / 'outputs' / 'model_summaries'

    # Summary Data Folder (For CSV files like feature importance, VIF, etc.)
    OUTPUT_DIR_DATA = base_dir / 'outputs' / 'summary data'

    # Ensure all directories exist (use Path.mkdir)
    OUTPUT_DIR_SUMMARY.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR_CHARTS.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR_DATA.mkdir(parents=True, exist_ok=True)
    print("File paths and directories configured.")

    # ==========================================================================
    # 3. DATA CLEANING AND PREPARATION (From 02_data_cleaning.ipynb)
    # ==========================================================================
    try:
        if not RAW_DATA_PATH.exists():
            print(f"ERROR: Raw data file not found at {RAW_DATA_PATH}. Please check the path.")
            sys.exit(1)
        df = pd.read_csv(RAW_DATA_PATH)
        print(f"Data loaded successfully from {RAW_DATA_PATH}. Initial shape: {df.shape}")
    except Exception as e:
        print(f"ERROR: Failed to read raw data: {e}")
        traceback.print_exc()
        sys.exit(1)
    
    # 3.1 FILTER AGGREGATES (Crucial cleaning step from 02_data_cleaning)
    aggregate_terms = ['world', 'Developing economies', 'East Asia & Pacific (excluding high income)',
                       'Europe & Central Asia (excluding high income)', 'Middle East & North Africa (excluding high income)',
                       'Sub-Saharan Africa (excluding high income)', 'Latin America & Caribbean (excluding high income)',
                       'South Asia', 'High income', 'Low income', 'Lower middle income', 'Upper middle income']
    df = df[~df['countrynewwb'].isin(aggregate_terms)].copy()

    # 3.2 DROP EXCESSIVELY MISSING COLUMNS (>90%)
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    cols_to_drop = missing_percentage[missing_percentage >= 90.0].index.tolist()
    df.drop(columns=cols_to_drop, inplace=True)
    print(f"Data filtered. Aggregates removed. {len(cols_to_drop)} columns dropped. Current shape: {df.shape}")

    # 3.3 SELECT COLUMNS FOR MODELING (From 04_modeling.ipynb)
    cols = ['year', 'regionwb24_hi', 'incomegroupwb24', 'pop_adult',
            'account_t_d', 'mobileaccount_t_d', 'internet']
    df_model = df[cols].copy()

    # 3.4 IMPUTATION (Prior to split and scaling)
    df_model['mobileaccount_t_d'] = df_model['mobileaccount_t_d'].bfill(axis=0).fillna(0)
    df_model['internet'] = df_model['internet'].bfill(axis=0).fillna(0)
    df_model['account_t_d'] = df_model['account_t_d'].fillna(df_model['account_t_d'].median())
    print("Imputation complete. Data ready for encoding.")

    # 3.5 ENCODING AND SCALING
    categorical_cols = ['regionwb24_hi', 'incomegroupwb24']
    df_model_encoded = pd.get_dummies(df_model, columns=categorical_cols, drop_first=True)

    X = df_model_encoded.drop(columns=['mobileaccount_t_d'])
    y = df_model_encoded['mobileaccount_t_d']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    numerical_cols = ['year', 'pop_adult', 'account_t_d', 'internet']
    standard_scaler = StandardScaler()
    X_train[numerical_cols] = standard_scaler.fit_transform(X_train[numerical_cols])
    X_test[numerical_cols] = standard_scaler.transform(X_test[numerical_cols])
    
    # 3.6 IDENTIFY AND CORRECT MULTICOLLINEARITY (VIF check showed these must be dropped)
    columns_to_drop_vif = ['incomegroupwb24_Low income', 'regionwb24_hi_High income']
    X_train_corrected = X_train.drop(columns=columns_to_drop_vif, errors='ignore')
    X_test_corrected = X_test.drop(columns=columns_to_drop_vif, errors='ignore')
    print(f"Data prepared, scaled, and VIF columns dropped. Train shape: {X_train_corrected.shape}")

    # ==========================================================================
    # 4. LINEAR REGRESSION BASELINE & OLS INFERENCE (From 04_modeling.ipynb)
    # ==========================================================================
    
    # 4.1 TRAIN AND EVALUATE CORRECTED LINEAR MODEL
    model_corrected = LinearRegression()
    model_corrected.fit(X_train_corrected, y_train)
    y_pred_corrected = model_corrected.predict(X_test_corrected)
    r2_corrected = r2_score(y_test, y_pred_corrected)
    mse_corrected = mean_squared_error(y_test, y_pred_corrected)
    
    print(f"\nLinear Regression R-squared (Baseline V2): {r2_corrected:.4f}")

    # 4.2 SAVE LINEAR MODEL SUMMARY (V2 Baseline)
    summary_text_corrected = (
        " --- Linear Regression V2: Clean Baseline ---\n"
        f"R-squared (Final Baseline): {r2_corrected:.4f}\n"
        f"Mean Squared Error (MSE): {mse_corrected:.4f}\n"
        "\nNOTE: Best linear model (VIF corrected) used as baseline."
    )
    file_path = OUTPUT_DIR_SUMMARY / 'linear_model_summary_V2_baseline.txt'
    with open(file_path, 'w') as f:
        f.write(summary_text_corrected)
    print("Linear model V2 baseline summary saved.")

    # 4.3 RUN AND SAVE OLS SUMMARY (For P-values/Inference)
    X_train_sm = sm.add_constant(X_train_corrected.astype(float))
    ols_model = sm.OLS(y_train, X_train_sm).fit()
    ols_summary_text = ols_model.summary().as_text()

    file_path_ols = OUTPUT_DIR_SUMMARY / 'ols_pvalue_summary_inference.txt'
    with open(file_path_ols, 'w') as f:
        f.write(ols_summary_text)
    print("OLS P-value summary saved for inference.")

    # ==========================================================================
    # 5. RANDOM FOREST MODELING & FEATURE IMPORTANCE
    # ==========================================================================

    # 5.1 TRAIN RANDOM FOREST MODEL
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train_corrected, y_train)
    y_rf_pred = rf_model.predict(X_test_corrected)
    r2_rf = r2_score(y_test, y_rf_pred)
    rmse_rf = np.sqrt(mean_squared_error(y_test, y_rf_pred))
    
    print(f"Random Forest Model trained. R-squared: {r2_rf:.4f} (Huge improvement!)")

    # 5.2 SAVE RANDOM FOREST SUMMARY
    rf_summary_text = (
        "--- Random Forest Model Evaluation (FINAL MODEL) ---\n"
        f"R-squared: {r2_rf:.4f}\n"
        f"Root Mean Squared Error (RMSE): {rmse_rf:.4f}\n"
    )
    file_path = OUTPUT_DIR_SUMMARY / 'random_forest_model_summary_FINAL.txt'
    with open(file_path, 'w') as f:
        f.write(rf_summary_text)

    # 5.3 EXTRACT AND SAVE FEATURE IMPORTANCES
    feature_importances = pd.DataFrame({
        'Feature': X_train_corrected.columns,
        'Importance': rf_model.feature_importances_
    }).sort_values(by='Importance', ascending=False)

    # Export the table (saved in summary data folder)
    file_path_csv = OUTPUT_DIR_DATA / 'rf_feature_importances_table.csv'
    feature_importances.to_csv(file_path_csv, index=False)
    print("Feature importance CSV saved to summary data folder.")

    # 5.4 SAVE FEATURE IMPORTANCE PLOT
    # Plotting code adapted from your notebook (top 6 features for clarity)
    df_plot = feature_importances.head(6)
    plt.figure(figsize=(10,6))
    sns.barplot(x='Importance', y='Feature', data=df_plot, palette='viridis')
    plt.title('Random Forest Feature Importance')
    plt.xlabel('Importance Score')
    plt.ylabel('Feature')
    
    file_path_chart = OUTPUT_DIR_CHARTS / 'rf_feature_importance_plot.png'
    plt.savefig(str(file_path_chart), bbox_inches='tight', dpi=300)
    plt.close()
    print("Feature importance plot saved to charts folder.")

    # ==========================================================================
    # 6. FINAL DATA OUTPUT FOR TABLEAU (From 04_modeling.ipynb)
    # ==========================================================================
    
    # Apply the model to the full dataset (X) and save the predicted outcome
    X_full = df_model_encoded.drop(columns=['mobileaccount_t_d'])
    
    # Re-apply VIF column drops to the full set
    X_full_corrected = X_full.drop(columns=columns_to_drop_vif, errors='ignore')

    # Ensure full data is scaled correctly using the *fitted* scaler
    X_full_corrected_scaled = X_full_corrected.copy()
    X_full_corrected_scaled[numerical_cols] = standard_scaler.transform(X_full_corrected_scaled[numerical_cols])

    # Generate final predictions
    df_model['Predicted_Adoption'] = rf_model.predict(X_full_corrected_scaled)
    
    # Merge key original columns back in for Tableau (country, region, year)
    df_model[['countrynewwb', 'codewb', 'regionwb24_hi', 'year']] = df[['countrynewwb', 'codewb', 'regionwb24_hi', 'year']].reset_index(drop=True)

    # Save the final Tableau-ready CSV
    # Ensure parent folder for table output exists
    TABLEAU_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_model.to_csv(TABLEAU_OUTPUT_PATH, index=False)
    print(f"\nFinal Tableau-Ready Data saved to: {TABLEAU_OUTPUT_PATH}")

    print("--- Pipeline Complete ---")

# ==============================================================================
# 7. EXECUTION BLOCK
# ==============================================================================
if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("Unhandled exception in pipeline:")
        traceback.print_exc()
        sys.exit(1)