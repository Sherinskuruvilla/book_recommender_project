import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

# Load CSV
#df = pd.read_csv("..data/clean/books.csv")
df = pd.read_csv(r"C:\Users\sheri\Desktop\Ironhack\book_recommender_project\data\clean\books.csv")

# Combine fields into one text string per book
df["features"] = (
    df["title"].astype(str) + " "
    + df["author"].astype(str) + " "
    + df["genre"].astype(str) + " "
    + df["description"].astype(str)
)

# TF-IDF representation
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X = vectorizer.fit_transform(df["features"])

# Choose number of clusters
k = 10
kmeans = KMeans(n_clusters=k, random_state=42)
df["cluster"] = kmeans.fit_predict(X)

def recommend_books(book_title, top_n=10):
    # Find all titles that contain the search term (case-insensitive)
    matches = df[df["title"].str.lower().str.contains(book_title.lower(), na=False)]
    
    if matches.empty:
        print(f"Book '{book_title}' not found in dataset.")
        return pd.DataFrame()
    
    # Just take the first match
    idx = matches.index[0]
    found_title = df.loc[idx, "title"]
    print(f"Found match: '{found_title}'")
    
    # Find the cluster of that book
    cluster_id = df.loc[idx, "cluster"]
    cluster_books = df[df["cluster"] == cluster_id].index
    
    # Compute cosine similarity within the cluster
    sims = cosine_similarity(X[idx], X[cluster_books]).flatten()
    
    # Sort by similarity
    sorted_indices = cluster_books[sims.argsort()[::-1]]
    
    # Remove the input book itself
    sorted_indices = sorted_indices[sorted_indices != idx]
    
    # Return top N recommended books
    return df.iloc[sorted_indices[:top_n]][["title", "author", "genre", "image_url"]]
