🌾 Agricultural Monitoring & Farm Resilience Analysis (Sri Lanka)
📌 Project Overview

This project investigates how farm monitoring practices influence agricultural productivity and resilience in Sri Lanka. Using real-world secondary datasets from FAOSTAT and NASA POWER, the study applies statistical modelling, hypothesis testing, regression analysis, time series forecasting, and Bayesian inference to evaluate agricultural performance under environmental and management factors.

The goal is to determine whether improved farm monitoring practices are associated with better crop yield and resilience against climate variability.

🎯 Research Statement

Farmers who monitor their farms regularly respond better to agricultural challenges.

This statement is evaluated using:

Descriptive Analytics
Inferential Statistics
Predictive Modelling
📊 Learning Outcomes Coverage
LO	Area
LO1	Probability distributions (Gamma, Normal)
LO2	Hypothesis testing (t-test, significance testing)
LO3	Regression analysis (multiple linear regression)
LO4	Exponential family distributions (Poisson, Exponential)
LO5	Time series forecasting (ARIMA model)
LO6	Bayesian inference (posterior estimation)
📂 Datasets Used
🌱 Agricultural Data (FAOSTAT)
Crop Yield (Rice, Sri Lanka)
Fertilizer Usage (Nitrogen-based inputs)
Irrigation Area
Area Harvested
🌦 Climate Data (NASA POWER)
Annual Rainfall (mm)
Average Temperature (°C)
🔧 Data Engineering

A Monitoring Index was constructed to represent farm management intensity:

Monitoring Index = (Fertilizer Use + Irrigation Area) / Area Harvested

This proxy represents the level of agricultural monitoring and input intensity.

📊 Methodology
1. Descriptive Analytics
Mean, variance, and distribution analysis
Trend analysis of yield and climate variables
Visualization using boxplots and histograms
2. Inferential Statistics
Hypothesis testing (t-test / regression significance)
Evaluation of monitoring impact on yield
3. Regression Analysis

Multiple Linear Regression model:

Yield = β0 + β1(Monitoring Index) + β2(Rainfall) + β3(Temperature)
4. Probability Distributions
Gamma distribution for response times
Poisson distribution for event frequency
Exponential distribution for time intervals
5. Time Series Forecasting
ARIMA model applied on yield data
Forecast accuracy evaluated using MAPE
6. Bayesian Analysis
Posterior estimation of monitoring effectiveness
95% credible intervals computed for effect size
📈 Key Results Summary
Monitoring Index shows positive relationship with crop yield
Climate variables significantly affect agricultural output
Forecasting model achieved high predictive accuracy (low MAPE)
Bayesian inference confirms positive but uncertain effect of monitoring
⚠️ Limitations
Some agricultural variables are proxy-based due to lack of direct monitoring data
Model performance is limited by small time-series sample size
Additional variables such as soil quality and pest infestation were not included
🚀 Tools & Technologies
Python (Pandas, NumPy)
Scikit-learn
Statsmodels
Matplotlib / Seaborn
Bayesian modeling tools
📌 Project Structure
data/
 ├── raw/
 ├── processed/

notebooks/
 ├── EDA.ipynb
 ├── Hypothesis_Testing.ipynb
 ├── Regression_Model.ipynb
 ├── Time_Series.ipynb
 ├── Bayesian_Analysis.ipynb

src/
 ├── data_cleaning.py
 ├── feature_engineering.py
 ├── modeling.py

results/
 ├── graphs/
 ├── outputs/
🧠 Key Insight

Agricultural productivity is not solely dependent on environmental conditions but is significantly influenced by farm management intensity, represented through the constructed Monitoring Index.

📌 Conclusion

This project demonstrates how statistical modelling and machine learning techniques can be applied to real-world agricultural systems to understand the relationship between farm monitoring practices and crop productivity. The results support the hypothesis that better monitoring contributes to improved agricultural outcomes under climate variability.
