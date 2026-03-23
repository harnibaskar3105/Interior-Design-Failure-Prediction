from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
import pandas as pd

# Load fixed dataset
df = pd.read_csv("interior_design_fixed.csv")

X = df[["budget", "room_size", "material", "lighting"]]
y = df["failure"]

numeric_features = ["budget"]
categorical_features = ["room_size", "material", "lighting"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced"))
    ]
)

pipeline.fit(X, y)

# Save trained model
joblib.dump(pipeline, "interior_pipeline.pkl")
print("✅ Model trained and saved!")
