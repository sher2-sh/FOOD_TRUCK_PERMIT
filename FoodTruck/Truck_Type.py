from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder   
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import pandas as pd

#Loading Clean data sets
file_path = "Cleaned_Mobile_Food_Facility_Permit.csv"
trucktype = pd.read_csv(file_path)


# Using latitude and Longitude for truck location but location
# could also be use. Using permit that each ventor have a permit. FoodItems of each
# truck and their LoctionDescription
features = ["Latitude", "Longitude", "permit", "LocationDescription", "FoodItems"]
target = "FacilityType"

#Encoding categorical target variable
label_encoder = LabelEncoder()
trucktype[target] = label_encoder.fit_transform(trucktype[target])

#Convert to string before encoding
for col in ["permit", "LocationDescription", "FoodItems"]:
    trucktype[col] = trucktype[col].astype(str)  
    trucktype[col] = LabelEncoder().fit_transform(trucktype[col])

#Splitting data into training and testing 40% of data
X = trucktype[features]
y = trucktype[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

#Training a RandomForestClassifier using 9 tree any more is not needed
#accuracy does not increase by much
model = RandomForestClassifier(n_estimators=9, random_state=42)
model.fit(X_train, y_train)

#setting up to display plot tree
plt.figure(figsize=(15, 15))
plot_tree(model.estimators_[0], feature_names=features, class_names=label_encoder.classes_, filled=True, rounded=True, fontsize=8)
plt.show()

#Making predictions
y_pred = model.predict(X_test)

#Evaluating the model
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred, target_names=label_encoder.classes_)

accuracy, classification_rep

print(f"Accuracy: {accuracy}")
print("Classification Result\n", classification_rep)

