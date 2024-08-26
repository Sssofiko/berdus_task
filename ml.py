import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('cleaned_data.csv')

descriptions = df['DESCRIPTION']
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(descriptions)

inertia = []
range_clusters = range(1, 20)

for k in range_clusters:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertia.append(kmeans.inertia_)

# График
plt.plot(range_clusters, inertia, 'bo-')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal Clusters')
plt.show()

# Кластеризация данных
optimal_clusters = 5  # Определила по графику
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
df['Cluster'] = kmeans.fit_predict(X)

# Анализ кластеров по CWE-ID и SEVERITY
cluster_analysis = df.groupby('Cluster')[['CWE-ID', 'SEVERITY']].agg(lambda x: x.value_counts().index[0])
print("Анализ кластеров по CWE-ID и SEVERITY:")
print(cluster_analysis)


# Извлечение ключевых слов для каждого кластера
def get_top_keywords(tfidf_matrix, cluster_labels, n_terms):
    terms = vectorizer.get_feature_names_out()
    clusters = np.unique(cluster_labels)

    mean_tfidf = np.array(tfidf_matrix.mean(axis=0)).flatten()
    df_keywords = pd.DataFrame({'term': terms, 'mean_tfidf': mean_tfidf})

    df_keywords['cluster'] = cluster_labels
    df_keywords = df_keywords.set_index('term')

    for cluster in clusters:
        cluster_df = df_keywords[df_keywords['cluster'] == cluster]
        if cluster_df.empty:
            print(f"\nCluster {cluster} is empty.")
        else:
            top_terms = cluster_df.nlargest(n_terms, 'mean_tfidf').index.tolist()
            print(f"\nCluster {cluster}:")
            print(', '.join(top_terms))


print("\nКлючевые слова-паттерны для каждого кластера:")
get_top_keywords(X, df['Cluster'], 10)

df.to_csv('clustered_data.csv', index=False)
print("\nРезультаты сохранены в файл 'clustered_data.csv'")
