import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

# Load the dataset
df = pd.read_csv("phishing.csv")  # Preprocessed dataset

# Split features and labels
X = df.drop("Result", axis=1)  # All features
y = df["Result"]               # Label: 1 (legit), -1 (phishing)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the model
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)
