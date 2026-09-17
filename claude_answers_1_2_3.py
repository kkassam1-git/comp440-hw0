"""
Claude's answers to the three questions in questions.md.

    uv run python claude_answers_1_2_3.py

Filled in by a Claude that has never seen the student's work. Kept as it was written.
"""

from load_data import GENRES, load_all


def question_1(ratings_df, movies_df):
    print("=" * 70)
    print("1. BASIC RATING STATISTICS")
    print("=" * 70)

    # (a) counts and star distribution
    n_ratings = len(ratings_df)
    n_users = ratings_df["user_id"].nunique()
    n_movies = ratings_df["movie_id"].nunique()
    print(f"\n(a) {n_ratings:,} ratings, {n_users:,} users, {n_movies:,} movies")
    print("    Rating distribution:")
    counts = ratings_df["rating"].value_counts().sort_index()
    for star, count in counts.items():
        pct = 100 * count / n_ratings
        print(f"      {star} stars: {count:6,} ({pct:5.1f}%)  {'#' * int(pct)}")

    # (b) ratings per user
    per_user = ratings_df.groupby("user_id").size()
    median_per_user = per_user.median()
    n_100plus = (per_user >= 100).sum()
    print(f"\n(b) Median ratings per user: {median_per_user:.1f}")
    print(f"    Users with >= 100 ratings: {n_100plus} of {n_users} ({100 * n_100plus / n_users:.1f}%)")

    # (c) top 10 most-rated movies
    rating_counts = ratings_df.groupby("movie_id").size().rename("n_ratings")
    joined = movies_df.set_index("movie_id")[["title"]].join(rating_counts)
    top_by_count = joined.sort_values("n_ratings", ascending=False).head(10)
    print("\n(c) 10 most-rated movies:")
    for title, n in zip(top_by_count["title"], top_by_count["n_ratings"]):
        print(f"      {n:4,}  {title}")

    # (d) top 10 by mean rating among movies with >= 20 ratings
    stats = ratings_df.groupby("movie_id")["rating"].agg(mean="mean", count="count")
    stats = stats.join(movies_df.set_index("movie_id")["title"])
    qualified = stats[stats["count"] >= 20]
    top_by_mean = qualified.sort_values("mean", ascending=False).head(10)
    print("\n(d) 10 highest mean-rating movies (>= 20 ratings):")
    for title, mean, count in zip(top_by_mean["title"], top_by_mean["mean"], top_by_mean["count"]):
        print(f"      {mean:.3f}  ({count:3d} ratings)  {title}")

    return stats


def question_2(stats):
    print("\n" + "=" * 70)
    print("2. WHAT IS THE BEST MOVIE IN THIS DATASET?")
    print("=" * 70)
    print("""
"Best" can't just mean "highest average rating": with only 20 ratings required to
qualify, a handful of enthusiastic fans can push an obscure movie to a perfect
5.0 average. The fix is the same one IMDb uses for its Top 250: shrink each
movie's mean toward the dataset-wide average, by an amount that depends on how
few ratings it has. A movie with 3 ratings gets pulled almost all the way back
to the global mean; a movie with 500 ratings barely moves. This is a Bayesian
average (posterior mean with a Beta/Normal-ish prior):

    WR = (v / (v + m)) * R  +  (m / (v + m)) * C

    R = the movie's own mean rating
    v = the movie's number of ratings
    C = the mean rating across ALL movies (the prior)
    m = a "confidence" constant: the number of ratings a movie needs before its
        own average starts to dominate the prior. I used the median number of
        ratings per movie, so a movie needs a typical amount of evidence before
        its score is trusted over the global average.
""")
    C = stats["mean"].mul(stats["count"]).sum() / stats["count"].sum()  # global mean, rating-weighted
    m = stats["count"].median()
    stats = stats.copy()
    stats["weighted_rating"] = (stats["count"] / (stats["count"] + m)) * stats["mean"] + (m / (stats["count"] + m)) * C
    print(f"Global mean rating C = {C:.3f}, confidence constant m = {m:.0f} ratings\n")

    top = stats.sort_values("weighted_rating", ascending=False).head(10)
    print("Top 10 by weighted (Bayesian-adjusted) rating:")
    for title, row in top.iterrows():
        print(f"      {row['weighted_rating']:.3f}  (raw mean {row['mean']:.2f}, {row['count']:3.0f} ratings)  {row['title']}")

    winner = top.iloc[0]
    print(f"\n==> Best movie: \"{winner['title']}\" "
          f"(weighted rating {winner['weighted_rating']:.3f}, raw mean {winner['mean']:.2f} "
          f"over {winner['count']:.0f} ratings)")


def question_3(ratings_df, movies_df):
    print("\n" + "=" * 70)
    print("3. WHICH MOVIE IS THE MOST ARTSY?")
    print("=" * 70)
    print("""
"Artsy" is a genre-flavor question, not a rating-quality question, so I built a
genre score instead of looking at stars. I hand-labeled each of the 19 genres as
art-house-coded, mainstream/commercial-coded, or neutral, based on the kind of
movie that genre usually signals:

    art-house (+):   Film-Noir (+3), Documentary (+3), Drama (+1), War (+1), Mystery (+1)
    mainstream (-):  Action (-2), Adventure (-2), Sci-Fi (-2), Animation (-2), Children's (-2),
                      Comedy (-1), Musical (-1), Thriller (-1), Western (-1), Fantasy (-1), Horror (-1)
    neutral (0):     Crime, Romance, unknown

A movie's artsiness score is the sum of its genres' weights. Genre alone leaves
lots of ties, so among the tied leaders I break ties by picking the more obscure
movie (fewer ratings) -- an art-house classic that only a handful of people in
this 1990s dataset bothered to rate fits "artsy" better than a Film-Noir/Drama
movie that was also a mass-market hit.
""")
    WEIGHTS = {
        "Film-Noir": 3, "Documentary": 3,
        "Drama": 1, "War": 1, "Mystery": 1,
        "Action": -2, "Adventure": -2, "Sci-Fi": -2, "Animation": -2, "Children's": -2,
        "Comedy": -1, "Musical": -1, "Thriller": -1, "Western": -1, "Fantasy": -1, "Horror": -1,
        "Crime": 0, "Romance": 0, "unknown": 0,
    }
    assert set(WEIGHTS) == set(GENRES)

    movies_df = movies_df.copy()
    movies_df["artsy_score"] = sum(movies_df[g] * w for g, w in WEIGHTS.items())
    rating_counts = ratings_df.groupby("movie_id").size().rename("n_ratings")
    scored = movies_df.set_index("movie_id")[["title", "artsy_score"]].join(rating_counts).fillna({"n_ratings": 0})

    top = scored.sort_values(["artsy_score", "n_ratings"], ascending=[False, True]).head(10)
    print("Top 10 by artsy score (ties broken toward fewer ratings, i.e. more obscure):")
    for title, score, n in zip(top["title"], top["artsy_score"], top["n_ratings"]):
        print(f"      score {score:+.0f}  ({n:.0f} ratings)  {title}")

    winner = top.iloc[0]
    print(f"\n==> Most artsy movie: \"{winner['title']}\" "
          f"(artsy score {winner['artsy_score']:+.0f}, {winner['n_ratings']:.0f} ratings)")


def claude_answers():
    ratings, ratings_df, movies, movies_df, users, users_df = load_all()
    stats = question_1(ratings_df, movies_df)
    question_2(stats)
    question_3(ratings_df, movies_df)


if __name__ == "__main__":
    claude_answers()
