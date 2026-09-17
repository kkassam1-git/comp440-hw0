"""
Part 3: the most ___ movie.

    uv run python human_part3.py

Pick an adjective. Write it on the `**My adjective:**` line of WRITEUP.md and a one-sentence
definition a classmate could code on the `**My definition:**` line. Print the top 5 movies
under it.
"""

from load_data import load_all



def top5_my_definition(ratings, ratings_df, movies, movies_df, users_df):
    print("== My definition ==")
    print(users_df["occupation"].unique())

    artsy_occupations = ["writer", "entertainment", "artist"]

    ratings_occupation = ratings_df.merge(users_df[["user_id", "occupation"]], on = "user_id")
    artsy_ratings = ratings_occupation[ratings_occupation["occupation"].isin(artsy_occupations)]

    artsy_ratings_titles = artsy_ratings.merge(movies_df[["movie_id", "title"]], on = "movie_id")

    movie_stats = artsy_ratings_titles.groupby("title")["rating"].agg(["mean", "count"])
    ratings_minimum = movie_stats[movie_stats["count"] >= 5]

    artsy_occupation_top_5 = ratings_minimum.sort_values(by = "mean", ascending = False).head(5)
    print(artsy_occupation_top_5)



def human_part3(ratings, ratings_df, movies, movies_df, users_df):
    print("part 3 unimplemented")  # delete this line when you start
    top5_my_definition(ratings, ratings_df, movies, movies_df, users_df)


if __name__ == "__main__":
    ratings, ratings_df, movies, movies_df, users, users_df = load_all()
    human_part3(ratings, ratings_df, movies, movies_df, users_df)
