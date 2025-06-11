# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Example: Load data from a CSV file
data = pd.read_csv('data.csv')

# 1. Data Exploration and Cleaning
print(data.head())  # Display the first few rows
print(data.info())  # Get data types and missing values
print(data.describe())  # Descriptive statistics

# Handle missing values
data.dropna(inplace=True)  # Remove rows with missing values
data.fillna(data.mean(), inplace=True)  # Fill missing values with the mean

# 2. Data Analysis (Example: Explore relationships)
# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

# Scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(data['feature_a'], data['feature_b'])
plt.title('Scatter Plot of Feature A vs. Feature B')
plt.xlabel('Feature A')
plt.ylabel('Feature B')
plt.show()

# Histogram
plt.figure(figsize=(8, 6))
plt.hist(data['feature_c'], bins=20)
plt.title('Histogram of Feature C')
plt.xlabel('Feature C')
plt.ylabel('Frequency')
plt.show()

# 3. Feature Engineering (Example: Creating new features)
data['feature_d'] = data['feature_a'] + data['feature_b']

# 4. Model Training (Example: Linear Regression)
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Split data into training and testing sets
X = data[['feature_a', 'feature_b']]
y = data['feature_c']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# 5. Further Analysis (Example: Clustering)
from sklearn.cluster import KMeans

# Determine the optimal number of clusters using the elbow method
sse = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42, n_init=10) # Specify n_init to avoid warning
    kmeans.fit(data[['feature_a', 'feature_b']])
    sse.append(kmeans.inertia_)

# Plot the SSE values to find the elbow point
plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), sse, marker='o')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of clusters')
plt.ylabel('SSE')
plt.show()

# Example: Performing K-Means clustering with 3 clusters
kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42, n_init=10)  # Specify n_init
data['cluster'] = kmeans.fit_predict(data[['feature_a', 'feature_b']])

# Visualize clusters
plt.figure(figsize=(8, 6))
plt.scatter(data['feature_a'], data['feature_b'], c=data['cluster'], cmap='viridis')
plt.title('K-Means Clustering')
plt.xlabel('Feature A')
plt.ylabel('Feature B')
plt.show()