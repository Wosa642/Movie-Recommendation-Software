import json

def load_movies(file_path='movies.json'):
    try:
        with open(file_path, 'r') as file:
            movies = json.load(file)
        return movies
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in movies.json.")
        return {}

def recommend_movies(movies, query):
    if not movies:
        return 'No movies available for recommendation.'
    
    query = query.strip().lower()  # Convert query to lowercase for consistent matching

    # Handle "Recent <genre>" queries
    if query.startswith('recent'):
        genre_query = query.replace('recent', '').strip()
        matching_genres = [g for g in movies if genre_query in g.lower()]
        if matching_genres:
            genre = matching_genres[0]  # Pick the first matching genre
            recent_movies = [movie for movie in movies[genre] if movie['year'] >= 2000]
            if recent_movies:
                return sorted(recent_movies, key=lambda x: x['year'], reverse=True)
            return 'No recent movies found in this genre.'
        return 'No matching genres found for recent movies.'

    # Fuzzy Genre matching
    matching_genres = [g for g in movies if query in g.lower()]
    
    if matching_genres:
        if len(matching_genres) > 1:
            print("\nDid you mean one of these genres?")
            for i, genre in enumerate(matching_genres, 1):
                print(f"{i}. {genre}")
            try:
                choice = int(input("\nEnter the number of your choice (or 0 to search all): "))
                if 0 < choice <= len(matching_genres):
                    return sorted(movies[matching_genres[choice-1]], key=lambda x: x['year'], reverse=True)
                elif choice == 0:
                    results = []
                    for genre in matching_genres:
                        results.extend(movies[genre])
                    return sorted(results, key=lambda x: x['year'], reverse=True)
                else:
                    print("Invalid choice, searching all matching genres.")
                    results = []
                    for genre in matching_genres:
                        results.extend(movies[genre])
                    return sorted(results, key=lambda x: x['year'], reverse=True)
            except ValueError:
                print("Invalid input, searching all matching genres.")
                results = []
                for genre in matching_genres:
                    results.extend(movies[genre])
                return sorted(results, key=lambda x: x['year'], reverse=True)
        else:
            return sorted(movies[matching_genres[0]], key=lambda x: x['year'], reverse=True)
    
    # Fuzzy Tag matching
    results = []
    for genre in movies:
        for movie in movies[genre]:
            if any(query in tag.lower() for tag in movie.get('tags', [])):
                results.append(movie)

    return sorted(results, key=lambda x: x['year'], reverse=True) if results else "No matches found for genre or keyword."

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
        print('No movies to recommend')
        return
    
    print("Welcome to the Movie Recommender!")
    print("Enter a genre (e.g., Sci-Fi, Action, War, Comedy), a keyword (e.g., action, funny),")
    print("or 'Recent <genre>' for newer movies. Type 'quit' to exit.")

    while True:
        user_input = input("\nWhat would you like to watch? ").strip()
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        if not user_input:
            print("Please enter a genre, keyword, or 'quit'.")
            continue
        
        recommendations = recommend_movies(movies, user_input)
        display_recommendations(recommendations)

if __name__ == "__main__":
    main()
