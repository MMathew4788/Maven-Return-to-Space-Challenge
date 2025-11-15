import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# 1. Work on a copy to avoid issues
data = dataset.copy()

# 2. Outlier detection on 'Price' using IQR
Q1 = data['Price'].quantile(0.25)
Q3 = data['Price'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Identify outliers
outlier_mask = (data['Price'] < lower_bound) | (data['Price'] > upper_bound)
data['Price_outlier'] = outlier_mask.map({True: 'Yes', False: 'No'})

# 3. Remove outliers for modeling (treat as missing)
data.loc[outlier_mask, 'Price'] = None

# 4. Indicator for imputation (missing or outlier replaced)
data['Price_imputed'] = data['Price'].isnull().map({True: 'Yes', False: 'No'})

# 5. Prepare feature columns (excluding Price, Price_imputed, Price_outlier)
feature_cols = [col for col in data.columns if col not in ['Price', 'Price_imputed', 'Price_outlier']]

# 6. Encode categorical variables
category_mappings = {}
for col in feature_cols:
    if data[col].dtype == 'object':
        data[col] = data[col].astype('category')
        category_mappings[col] = dict(enumerate(data[col].cat.categories))
        data[col] = data[col].cat.codes

# 7. Split data for training and predicting
train = data[data['Price'].notnull()]
test = data[data['Price'].isnull()]

# 8. Train and predict
if not train.empty and not test.empty:
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(train[feature_cols], train['Price'])
    predicted_prices = rf.predict(test[feature_cols])
    data.loc[data['Price'].isnull(), 'Price'] = predicted_prices

# 9. Decode categorical columns
for col in category_mappings:
    reverse_map = {code: category for code, category in category_mappings[col].items()}
    data[col] = data[col].map(reverse_map)

# 10. Output
result = data
