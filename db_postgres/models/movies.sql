SELECT
    CAST(id as INT) as movie_id,
    TO_DATE("Release Date", 'YY-MM-DD') as release_date,
    "IMDB URL" as imdb_url,
    CAST(CAST("Film-Noir" as INT) as BOOLEAN) as film_noir,
    CAST(CAST("crime" as INT) as BOOLEAN) as crime,
    CAST(CAST("drama" as INT) as BOOLEAN) as drama,
    CAST(CAST("war" as INT) as BOOLEAN) as war,
    CAST(CAST("Action" as INT) as BOOLEAN) as action,
    CAST(CAST("comedy" as INT) as BOOLEAN) as comedy,
    CAST(CAST("horror" as INT) as BOOLEAN) as horror,
    CAST(CAST("Sci-Fi" as INT) as BOOLEAN) as sci_fi,
    CAST(CAST("fantasy" as INT) as BOOLEAN) as fantasy,
    CAST(CAST("musical" as INT) as BOOLEAN) as musical,
    CAST(CAST("mystery" as INT) as BOOLEAN) as mystery,
    CAST(CAST("romance" as INT) as BOOLEAN) as romance,
    CAST(CAST("western" as INT) as BOOLEAN) as western,
    CAST(CAST("thriller" as INT) as BOOLEAN) as thriller,
    CAST(CAST("animation" as INT) as BOOLEAN) as animation,
    CAST(CAST("Children's" as INT) as BOOLEAN) as children,
    CAST(CAST("adventure" as INT) as BOOLEAN) as adventure,
    CAST(CAST("documentary" as INT) as BOOLEAN) as documentary,
    CAST(CAST("unknown" as INT) as BOOLEAN) as unknown,
    "Name" as name
FROM {{source('recommender_system_raw_data', 'movies')}}














