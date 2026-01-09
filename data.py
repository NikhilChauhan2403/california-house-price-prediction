import pandas as pd
import numpy as np
import os
import joblib

MODEL_FILE="model.pkl"

PIPELINE_FILE="pipeline.pkl"

from sklearn.model_selection import StratifiedShuffleSplit 
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

def build_pipeline(num_attributes,cat_attributes):
    num_pipeline=Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler() )
    ])
    cat_pipeline=Pipeline([
        ("encoder",OneHotEncoder(handle_unknown="ignore", sparse_output=True ,max_categories=20))
    ])
    full_pipeline=ColumnTransformer([
        ("num",num_pipeline, num_attributes),
        ("cat",cat_pipeline, cat_attributes)
    ])
    return full_pipeline

if not os.path.exists(MODEL_FILE):
    housing=pd.read_csv("data.csv")
    housing['income_cat']=pd.cut(housing['median_income'],
                                bins=[0,1.5,3.0,4.5,6,np.inf],
                                labels=[1,2,3,4,5])
    split=StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)
    for train_index,test_index in split.split(housing, housing["income_cat"]):
        housing.loc[test_index].drop("income_cat", axis=1).to_csv("input.csv" ,index=False)
        housing=housing.loc[train_index].drop("income_cat",axis=1)
    print(housing)
        

    housing_labels=housing["median_house_value"].copy()
    housing_features=housing.drop("median_house_value",axis=1)
    num_attributes=housing_features.drop("ocean_proximity",axis=1).columns.tolist()
    cat_attributes=["ocean_proximity"]

    pipeline=build_pipeline(num_attributes,cat_attributes)

    housing_prepared=pipeline.fit_transform(housing_features)
    model=RandomForestClassifier(n_estimators=50,     
    max_depth=15,         
    n_jobs=-1,
    random_state=42)
    model.fit(housing_prepared,housing_labels)
    
    joblib.dump(model,MODEL_FILE)
    joblib.dump(pipeline,PIPELINE_FILE)
    print("congrats model saved and trained")
else:
    model=joblib.load(MODEL_FILE)
    pipeline=joblib.load(PIPELINE_FILE)
    cols=['longitude', 'latitude', 'housing_median_age', 'total_rooms',
       'total_bedrooms', 'population', 'households', 'median_income', 'ocean_proximity']
    def predict_price(values):
        """
            values = [longitude, latitude, housing_median_age, 
              total_rooms, total_bedrooms, population, 
              households, median_income, ocean_proximity]
        """
        x = pd.DataFrame([values], columns=cols)
        transformed = pipeline.transform(x)
        prediction = model.predict(transformed)
        return prediction[0]

