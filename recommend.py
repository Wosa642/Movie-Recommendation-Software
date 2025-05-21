# Movie Recommender System
# This script recommends movies based on user input.
# adding to verify git tracking.
import json

def load_movies(file_path='movies.json'):
    import json
    with open(file_path, 'r') as file:
        movies = json.load(file)
    return movies



def recommend_movies(movies, query):
    if not movies:
        return 'No movies available for recommendation.'
    query = query.strip().title()

    if query.startswith('Recent'):
        genre = query.replace('Recent', '').strip().title()
        if genre in movies:
            recent_movies = [movies for movies in movies[genre] if movies['year'] >= 2000]
        if recent_movies:
            return sorted(recent_movies, key=lambda x: x['year'], reverse=True)
        else:
            return 'No recent movies found in this genre.'
          
    # Fuzzy Genre matching
    matching_genres = []
    for genre in movies.keys():
        if query in genre.lower():
            matching_genres.append(genre)
    
    if matching_genres:
        if len(matching_genres) > 1:
            print("\nDid you mean one of these genres?")
            for i, genre in enumerate(matching_genres, 1):
                print(f"{i + 1}. {genre}")
            try:
                choice = int(input("\nEnter the number of your choice (or 0 to search all): "))
                if 0 < choice <= len(matching_genres):
                    return sorted(movies[matching_genres[choice-1]], key=lambda x: x['year'], reverse=True)
                elif choice == 0:
                    results = []
                    for genre in matching_genres:
                        results.extend(movies[genre])
                    return sorted(results, key=lambda x: x['year'], reverse=True)
            except ValueError:
                pass
        else:
            return sorted (movies[matching_genres[0]], key=lambda x: x['year'], reverse=True)
    
    
    # Fuzzy Tag matching
    results = []
    for genre in movies:
        for movie in movies[genre]:
            if any(query.lower() in tag.lower() for tag in movie.get('tags', [])):
                results.append(movie)

    # Sort keyword results by year
    return sorted(results, key=lambda x: x["year"], reverse=True) if results else "No matches found for genre or keyword." 

# Display recommendations in a formatted way
def display_recommendations(recommendations):
    if isinstance(recommendations, list):
        if recommendations:
            print("\nRecommended movies:")
            for movie in recommendations:
                print(f"- {movie['title']} ({movie['year']}) by {movie['director']} (Rating: {movie['rating']})")
        else:
            print("No recommendations found.")
    else:
        print(recommendations)

def main():
    movies = load_movies()
    if not movies:
        print('No movies to recommend')#
        return
    
    print("Welcome to the Movie Recommender!")
    print("Enter a genre (e.g., Sci-Fi, Action, War, Comedy), a keyword (e.g., action, funny),")
    print("or 'Recent <genre>' for newer movies. Type 'quit' to exit.")

    while True:
        user_input = input("\nWhat would you like to watch? ").strip()
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        if not user_input:
            print("Please enter a genre, keyword, or 'quit'.")
            continue
        
        recommendations = recommend_movies(movies, user_input)
        display_recommendations(recommendations)


if __name__ == "__main__":
   main()
    
