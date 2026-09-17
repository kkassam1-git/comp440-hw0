"""
Part 2: the best movie.

    uv run python human_part2.py

Write your rule on the `**My rule:**` line of WRITEUP.md. Print the top 10 movies (id, title,
ratings count, mean rating) under it.
"""

from load_data import load_all
import pandas as pd


def top10_my_rule(ratings, ratings_df, movies, movies_df):
    print("== My rule ==")
    # My rule weights each individual rating by how many years afer the release it was posted
    # then average the weighted ratings per move. The core idea being taht rating give long after
    # the release date is indicative of a movie that has "stood the test of time."
    merge_ratings_movie = ratings_df.merge(movies_df[["movie_id", "title"]], on = "movie_id")

    #extracting year of release from title
    merge_ratings_movie["release_year"] = merge_ratings_movie["title"].str.extract(r"\((\d{4})\)$").astype(float)
    merge_ratings_movie = merge_ratings_movie.dropna(subset = ["release_year"])
    merge_ratings_movie["release_year"] = merge_ratings_movie["release_year"].astype(int)

    merge_ratings_movie ["review_year"] = pd.to_datetime(merge_ratings_movie["timestamp"], unit = "s").dt.year

    merge_ratings_movie["years_since_release"] = (merge_ratings_movie["review_year"] - merge_ratings_movie["release_year"]).clip(lower=0)

    # +1 so a review from release date still counts
    merge_ratings_movie["weight"] = merge_ratings_movie["years_since_release"] + 1


    ## calculate weighted mean per movie: sum(rating * weight) / sum(weight)
    merge_ratings_movie["rating_weighted"] = merge_ratings_movie["rating"] * merge_ratings_movie["weight"]
    movie_stats = merge_ratings_movie.groupby(["movie_id", "title"]).agg(
        weighted_sum = ("rating_weighted", "sum"),
        weight_total = ("weight", "sum"),
        count = ("rating", "count")
    ).reset_index()
    movie_stats["time_weighted_mean"] = movie_stats["weighted_sum"] / movie_stats["weight_total"]

    # also weighted by how many reviews the movie has, 70 reviews is set as the bar 
    df_rating_mean = ratings_df["rating"].mean()
    m = 70 
    movie_stats["final_score"] = (
        (movie_stats["count"] / (movie_stats["count"] + m)) * movie_stats["time_weighted_mean"]
        + (m / (movie_stats["count"] + m)) * df_rating_mean
    )

    top10 = movie_stats.sort_values(by="final_score", ascending=False).head(10)
    print(top10[["movie_id", "title", "count", "time_weighted_mean", "final_score"]])



def human_part2(ratings, ratings_df, movies, movies_df):
    print("part 2 unimplemented")  # delete this line when you start
    top10_my_rule(ratings, ratings_df, movies, movies_df)


if __name__ == "__main__":
    ratings, ratings_df, movies, movies_df, users, users_df = load_all()
    human_part2(ratings, ratings_df, movies, movies_df)
