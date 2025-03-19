import pandas as pd
import os

# Load the cvs file
file_path = "Mobile_Food_Facility_Permit_20250317.csv"

foodtruck = pd.read_csv(file_path, encoding='utf-8') #Print 20 rows 
print(foodtruck.head(20))


############
#Begin cleaning dataset


#Remove Duplicates
foodtruck.drop_duplicates(inplace=True)

#Delete empty row or null value
foodtruck = foodtruck[(foodtruck['FacilityType'].str.strip() != '') & (foodtruck['FacilityType'].notna())]

#Delete row in empty row or equal zero in LocationDescription and cnn
foodtruck = foodtruck[(foodtruck['LocationDescription'].str.strip() != '') & (foodtruck['LocationDescription'].notna())]
foodtruck['cnn'] = pd.to_numeric(foodtruck['cnn'],errors='coerce')
foodtruck = foodtruck[(foodtruck['cnn'] != '0') & (foodtruck['cnn'].notna())]


#Change Latitude, Longitude, and Zip Codes into numeric, and delete empty
# or equal to zero in dataset
foodtruck['Latitude'] = pd.to_numeric(foodtruck['Latitude'], errors='coerce')
foodtruck['Longitude'] = pd.to_numeric(foodtruck['Longitude'], errors='coerce')
foodtruck['Zip Codes'] = pd.to_numeric(foodtruck['Zip Codes'], errors='coerce')
foodtruck = foodtruck[(foodtruck['Latitude'] != 0) & (foodtruck['Latitude'].notna())]
foodtruck = foodtruck[(foodtruck['Longitude'] != 0) & (foodtruck['Longitude'].notna())]


#Remove any white space and make data field into title type.
foodtruck['Applicant'] = foodtruck['Applicant'].str.strip().str.title()
foodtruck['FacilityType'] = foodtruck['FacilityType'].str.strip().str.title()


#Save cleaned data
cleaned_file_path = "Cleaned_Mobile_Food_Facility_Permit.csv"
foodtruck.to_csv(cleaned_file_path, index=False)

#Load Data
clean_file = "Cleaned_Mobile_Food_Facility_Permit.csv"
new_foodtruck = pd.read_csv(clean_file, encoding='utf-8') #Print part of dataset
print("After Data cleaning")
print(new_foodtruck.head(20)) #Print 20 rows




