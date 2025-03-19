import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.cluster import KMeans

#Loading Cleaned Food Truck Dataset
file_path = "Cleaned_Mobile_Food_Facility_Permit.csv"
vendor = pd.read_csv(file_path)

vendor = vendor.dropna(subset=['FoodItems']) #Drop missing value in FoodItems lists

#remove special characters and split into list
vendor['FoodItems'] = vendor['FoodItems'].str.lower().str.replace(r'[^a-z\s]', '', regex=True)
vendor['FoodItems'] = vendor['FoodItems'].str.split()

#extract food items and creating encoding
food_items = list(set(item for sublist in vendor['FoodItems'] for item in sublist))
food_items_df = pd.DataFrame(0, index=vendor.index, columns=food_items)

for index, items in vendor['FoodItems'].items():
    for item in items:
        food_items_df.at[index, item] = 1

#K-means clustering with 7 clusters
K = 7
kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
vendor['Cluster'] = kmeans.fit_predict(food_items_df)

# Identify representative food items for each cluster
cluster_representatives = {}
for cluster in range(K):
    cluster_indices = vendor[vendor['Cluster'] == cluster].index
    food_counts = Counter(item for index in cluster_indices for item in vendor.loc[index, 'FoodItems'])
    cluster_representatives[cluster] = [item for item, _ in food_counts.most_common(5)] # Top 5 items

             
print("\n  Cluster Groups")

# Show first 10 in each cluster
display_items = 10  

for cluster in range(K):
    cluster_indices = vendor[vendor['Cluster'] == cluster].index
    food_counts = Counter(item for index in cluster_indices for item in vendor.loc[index, 'FoodItems'])
    
 # Get lists from top lists
    cleaned_foods = [food.strip() for food, _ in food_counts.most_common(display_items) if isinstance(food, str) and food.strip()]
    
    if cleaned_foods:
        print(f"Cluster {cluster}: {', '.join(cleaned_foods)}")
    else:
        print(f"Cluster {cluster}: No significant food items found")
        
#Clusters Scatter plot
plt.figure(figsize=(12, 12))
for cluster in range(K):
    cluster_indices = vendor[vendor['Cluster'] == cluster].index
    plt.scatter(food_items_df.loc[cluster_indices].sum(axis=1),
                cluster_indices,
                label=f'Cluster {cluster}')

plt.xlabel('Total Items Sold by Vendors')
plt.ylabel('Vendors (Index)')
plt.title('K-Means Clustering')
plt.legend()
plt.show()


