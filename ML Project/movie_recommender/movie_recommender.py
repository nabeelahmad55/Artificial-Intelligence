# movie_recommender.py
"""
🎬 Movie Recommendation System
Author: Nabeel Ahmad
GitHub: https://github.com/nabeelahmad55
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------
# Step 1: Create Sample Dataset
# ---------------------------
data = {
    'title': [
        'The Matrix',
        'John Wick',
        'Inception',
        'Interstellar',
        'The Dark Knight',
        'Pulp Fiction',
        'Fight Club',
        'Forrest Gump',
        'The Shawshank Redemption',
        'Avengers: Endgame'
    ],
    'description': [
        'A computer hacker learns about the true nature of reality and his role in the war against its controllers.',
        'An ex-hitman comes out of retirement to track down the gangsters that killed his dog and took everything from him.',
        'A thief who steals corporate secrets through dream-sharing technology is given an inverse task of planting an idea.',
        'A team of explorers travel through a wormhole in space to ensure humanity’s survival.',
        'When the menace known as the Joker wreaks havoc, Batman must accept one of the greatest psychological tests of his ability.',
        'The lives of two mob hitmen, a boxer, and a pair of diner bandits intertwine in a tale of crime and redemption.',
        'An insomniac office worker and a soap maker form an underground fight club that evolves into something much more.',
        'The life journey of Forrest Gump who unwittingly influences several historical events in the 20th century.',
        'Two imprisoned men bond over a number of years, finding solace and redemption through acts of common decency.',
        'After the devastating events of Infinity War, the Avengers assemble once more to restore balance to the universe.'
    ]
}

movies_df = pd.DataFrame(data)

# ---------------------------
# Step 2: Compute TF-IDF Matrix
# ---------------------------
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(movies_df['description'])

# ---------------------------
# Step 3: Compute Cosine Similarity
# ---------------------------
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# ---------------------------
# Step 4: Recommend Function
# ---------------------------
def recommend(movie_title, num_recommendations=5):
    if movie_title not in movies_df['title'].values:
        print(f"\n❌ Movie '{movie_title}' not found in database.\n")
        return

    idx = movies_df[movies_df['title'] == movie_title].index[0]
    similarity_scores = list(enumerate(cosine_sim[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:num_recommendations + 1]

    print(f"\n🎥 Movies similar to '{movie_title}':\n")
    for i, score in similarity_scores:
        print(f"👉 {movies_df.iloc[i]['title']} (Similarity: {score:.2f})")

# ---------------------------
# Step 5: Run App
# ---------------------------
if __name__ == "__main__":
    print("🎬 Welcome to Movie Recommendation System!")
    print("Available movies:\n")
    for title in movies_df['title']:
        print(f"• {title}")
    print("\n")

    user_input = input("Enter a movie title to get recommendations: ").strip()
    recommend(user_input)
