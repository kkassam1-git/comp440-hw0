"""
Part 1: basic rating statistics.

    uv run python human_part1.py

Answer the four questions below with your own code, print each answer under its label, and
explain each in one sentence in WRITEUP.md.
"""

from load_data import load_all


def human_part1(ratings, ratings_df, movies, movies_df, users, users_df):

    print("== (a) ==")
    # (a) How many ratings, users, and movies are there, and how are ratings distributed across 1-5 stars?
    num_ratings = len(ratings_df)
    num_users = ratings_df["user_id"].nunique()
    num_moves = ratings_df["movie_id"].nunique()
    print("Total number of ratings:", num_ratings)
    print("Total number of users:", num_users)
    print("Total number of movies:", num_moves)

    rating_distribution_counts = ratings_df["rating"].value_counts().sort_index()
    print("Ratings by star groups:", rating_distribution_counts)

    print("== (b) ==")
    # (b) What is the median number of ratings per user, and how many users have 100 or more ratings?

    ratings_individual_user = ratings_df["user_id"].value_counts()
    median_ratings = ratings_individual_user.median()
    users_100_plus = ratings_individual_user[ratings_individual_user >= 100].count()

    print("Median ratings per user:", median_ratings)
    print("Users with 100+ ratings:", users_100_plus)

    print("== (c) ==")
    # (c) Join ratings to titles. Which 10 movies have the most ratings?

    ratings_titles = ratings_df.merge(movies_df[["movie_id", "title"]], on = "movie_id")
    ratings_indvidual_movie = ratings_titles.groupby("title").size()
    most_rated = ratings_indvidual_movie.sort_values(ascending = False).head(10)
    print("10 most rated movies:")
    print(most_rated)

    print("== (d) ==")
    # (d) Among movies with at least 20 ratings, which 10 have the highest mean rating?
    #     Show title, mean, and count.
    movie_stats = ratings_titles.groupby("title")["rating"].agg(["mean", "count"])
    ratings_20_plus = movie_stats[movie_stats["count"] >= 20]
    highest_mean = ratings_20_plus.sort_values(by = "mean", ascending = False).head(10)

    print("10 highest rated movies (20+ ratings)")
    print(highest_mean)

if __name__ == "__main__":
    ratings, ratings_df, movies, movies_df, users, users_df = load_all()
    human_part1(ratings, ratings_df, movies, movies_df, users, users_df)
