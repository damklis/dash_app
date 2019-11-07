import os
import datetime
import pandas as pd
import time
from datadownloader.downloader import DataDownloader
from datadownloader.connection_decorator import connection_checker
from dbconfig.hive_conf import HiveConfig

## Query to extract App"s version premiere date.
query_dates = """
SELECT event_data["App_version"] as app,
        MIN(`date`) as first_events
FROM events.game
WHERE `date` > "2019-03-30"
AND (event_data["App_version"] LIKE "0.__" 
        OR event_data["App_version"] LIKE "0.__._")
AND geoip_country NOT IN ("company", "PL", "US")
AND event_data["IP"] != "XX.XX.XX.XX.XX"
AND event_data["Device_version"] != "Google Pixel XL"
AND event_data["Player_ID"] != "114187787"
GROUP BY event_data["App_version"]
HAVING MIN(`date`) != current_date
ORDER BY app DESC
LIMIT 2
"""

## Getting informations about version"s release date.
events_downloader = DataDownloader(**HiveConfig.conf)
dates = events_downloader.read_sql(query_dates)

first_version = dates.loc[1]["app"]
second_version = dates.loc[0]["app"]
first_date = dates["first_events"][1]
second_date = dates["first_events"][0]

## Query that extract data neccesary to calculate win_ratio.
query_win_ratio = """WITH games AS
(SELECT NVL(event_data["Levels_bundle_version"], "01") as levels,
        event_data["Player_ID"] AS user_id,
        event_data["Game_number"] AS game_id,
        event_data["Board_id"] AS board_id,
        event_data["App"] AS app_version,
        event_data["Win"] AS won_lose,
        CAST(event_data["Move_last"] as int) AS moves_last
FROM events.game
WHERE `date` >= "{first_dt}"
AND event_name = "end_game"
AND geoip_country != "company"
AND event_data["App"] IN ("{first}", "{second}")
AND (event_data["Levels_bundle_version"] != "default" 
        OR event_data["Levels_bundle_version"] IS NULL)),

plays AS(SELECT board_id,
       SUM(CASE WHEN won_lose = 1 THEN 1 ELSE 0 END) as wins,
       SUM(CASE WHEN won_lose = 0 THEN 1 ELSE 0 END) as loss,
       COUNT(DISTINCT game_id) as total_games,
       app_version,
       levels,
       AVG(moves_last) as moves_last_mean,
       cast(percentile(moves_last, 0.50) as int) as moves_last_median,
       cast(percentile(moves_last, 0.75) - percentile(moves_last, 0.25) as int) as iqr
FROM games
GROUP BY board_id, app_version, levels),

attempts AS(SELECT app_version,
        levels,
        board_id,
        user_id,
        COUNT(game_id) as attempt
FROM games
GROUP BY app_version, levels, board_id, user_id),

median AS(SELECT app_version,
       levels,
       board_id,
       ROUND(percentile(attempt, 0.50),2) as median_attempt
FROM attempts
GROUP BY app_version, levels, board_id)

SELECT a.app_version as app_version,
       a.levels as levels_bundle,
       a.board_id as board_id,
       a.wins as wins,
       a.loss as loss,
       a.total_games as total_games,
       a.moves_last_median as moves_left,
       a.iqr as iqr,
       b.median_attempt as median_attempt
FROM plays a
JOIN median b
ON a.app_version = b.app_version AND a.levels = b.levels AND a.board_id = b.board_id
""".format(first=first_version, second=second_version, first_dt=first_date)


## Query that extract data neccesary to calculate drop_rate.
query_drop_rate = """
WITH installs AS (SELECT DISTINCT user_id
FROM events.game
WHERE event_name = "type"
AND `date` BETWEEN "{first_dt}" AND "{second_dt}"
AND geoip_country != "company"
AND event_data["App_version"] IN ("{first}", "{second}")),

SELECT board_id,
       count(DISTINCT user_id) total_users,
       app_version,
       levels as levels_bundle
FROM
(SELECT user_id,
        event_data["Board_id"] AS board_id,
        event_data["App"] AS app_version,
        NVL(event_data["Levels_bundle_version"], "01") as levels
FROM events.game
WHERE `date` BETWEEN "{first_dt}" AND "{second_dt}"
AND event_name = "start_game"
AND event_data["App"] IN ("{first}", "{second}")
AND (event_data["Levels_bundle_version"] != "default" 
        OR event_data["Levels_bundle_version"] IS NULL) as temp
""".format(first=first_version, second=second_version,
    first_dt=first_date, second_dt=second_date)

## Query that extract data neccesary to calculate player\'s funnnel.
query_funnel = """
WITH installs AS (SELECT DISTINCT user_id
FROM events.game
WHERE event_name = "type"
AND `date` BETWEEN "{first_dt}" AND "{second_dt}"
AND geoip_country != "company"
AND event_data["App"] IN ("{first}", "{second}")),

SELECT event_name,
       board_id,
       COUNT(DISTINCT user_id) AS total_users,
       app_version,
       step
FROM(
SELECT CAST(event_data["Player_ID"] as int) as user_id,
        event_data["Board_id"] as board_id,
        event_data["Event_name"] as event_name,
        event_data["Step"] as step,
        event_data["App_version"] AS app_version,
        coalesce(event_data["Chest_id"], 0) as chest
FROM events.game
WHERE `date`  BETWEEN "{first_dt}" AND "{second_dt}"
AND event_data["App_version"] IN ("{first}", "{second}")
AND user_id IN (SELECT * FROM installs)
AND (event_data["Board_id"] < "020102" OR event_data["Board_id"] is null)
AND event_data["Event_name"] IN ("type", "start_game",
        "tutorial_step", "end_game") as temp
""".format(first=first_version, second=second_version,
    first_dt=first_date, second_dt=second_date)

## Query to extract info about sessions.
query_session = """
WITH installs AS (SELECT DISTINCT user_id
FROM events.game
WHERE event_name = "type"
AND geoip_country <> "company"
AND `date` >= "{first_dt}"
AND event_data["App_version"] IN ("{first}", "{second}"))

SELECT user_id as user_id,
       app_version as app_version,
       session as session,
       (max(`timestamp`) - min(`timestamp`)) / 1000 as sess_time
FROM
(SELECT user_id,
        app_version,
       `timestamp`,
       SUM(new_session) OVER (PARTITION BY user_id ORDER BY `timestamp`) + 1 as session
FROM (
    SELECT user_id,
           event_data["App_version"] as app_version,
           `timestamp`
        , CASE
            WHEN `timestamp`
                 - LAG (`timestamp`)
                 OVER (PARTITION BY user_id ORDER BY `timestamp`) > 30 * 60 * 1000
            THEN 1
            ELSE 0
          END AS new_session
    FROM events.game
    WHERE `date` >= "{first_dt}"
    AND event_data["App_version"] IN ("{first}", "{second}")
    AND user_id IN (SELECT * FROM installs)) as sub1) as sub2
GROUP BY user_id, app_version, session
ORDER by user_id
""".format(first=first_version, second=second_version, first_dt=first_date)

## Query to extract info about player's economy during game.
query_economy = """WITH
installs AS (SELECT DISTINCT user_id
FROM events.game
WHERE event_name = "type"
AND `date` BETWEEN "{first_dt}" AND "{second_dt}"
AND geoip_country != "company"
AND event_data["App_version"] = "{first}"),

users AS(SELECT b.event_data["Board_id"] as board_id,
    a.event_data["App_version"] as app_version,
    NVL(a.event_data["Levels_bundle_version"], "01") as levels,
    b.user_id as user_id,
    get_json_object(a.event_data["Status"], "$.SC") as SC,
    get_json_object(a.event_data["Status"], "$.Energy") as Energy,
    get_json_object(a.event_data["Status"], "$.Stars") as Stars,
    get_json_object(a.event_data["Status"], "$.Keys") as Keys,
    get_json_object(a.event_data["Status"], "$.HC") as HC,
    dense_rank() OVER (PARTITION BY b.user_id ORDER BY b.`timestamp`) rank_lvl
FROM events.game a
JOIN events.game b
ON a.event_data["Game_number"] = b.event_data["Game_number"]
WHERE a.event_name = "end_game_2"
AND b.event_name = "end_game"
AND a.geoip_country != "company"
AND (a.event_data["Levels_bundle_version"] != "default" OR a.event_data["Levels_bundle_version"] IS NULL)
AND b.event_data["Win"] = 1
AND a.`date` BETWEEN "{first_dt}" AND "{second_dt}"
AND a.event_data["App_version"] = "{first}"),

versions AS(SELECT
    app_version,
    levels,
    rank_lvl as level,
    percentile(CAST(SC AS int), 0.50) as SC,
    percentile(CAST(Energy AS int), 0.50) as Energy,
    percentile(CAST(Stars AS int), 0.50) as Stars,
    ROUND(AVG(Keys), 2) as Keys,
    percentile(CAST(HC AS int), 0.50) as HC
FROM users
WHERE user_id IN (SELECT * FROM installs)
GROUP BY rank_lvl, app_version, levels
ORDER BY rank_lvl),


SELECT app_version,
       levels as levels_bundle,
       level,
       sc,
       energy,
       stars,
       keys,
       hc
FROM versions
""".format(first=first_version, second=second_version,
    first_dt=first_date, second_dt=second_date)

## Query to extract info about player's economy during game.
query_economy_2 = """WITH
installs AS (SELECT DISTINCT user_id
FROM events.game
WHERE event_name = "type"
AND `date` >= "{second_dt}"
AND geoip_country != "company"
AND event_data["App_version"] IN ("{first}", "{second}")),

events AS (SELECT b.event_data["Board_id"] as level,
    a.event_data["App_version"] as app_version,
    NVL(a.event_data["Levels_bundle_version"], "01") as levels,
    b.user_id as user_id,
    get_json_object(a.event_data["Status"], "$.SC") as SC,
    get_json_object(a.event_data["Status"], "$.Energy") as Energy,
    get_json_object(a.event_data["Status"], "$.Stars") as Stars,
    get_json_object(a.event_data["Status"], "$.Keys") as Keys,
    get_json_object(a.event_data["Status"], "$.HC") as HC
FROM events.game a
JOIN events.game b
ON a.event_data["Game_number"] = b.event_data["Game_number"]
WHERE a.event_name = "end_game_2"
AND a.geoip_country != "company"
AND (a.event_data["Levels_bundle_version"] != "default" 
        OR a.event_data["Levels_bundle_version"] IS NULL)
AND b.event_data["Win"] = 1
AND a.`date` >= "{second_dt}"
AND a.event_data["App_version"] IN ("{first}", "{second}"))

SELECT
    app_version,
    levels as levels_bundle,
    level,
    percentile(CAST(SC AS int), 0.50) as SC,
    percentile(CAST(Energy AS int), 0.50) as Energy,
    percentile(CAST(Stars AS int), 0.50) as Stars,
    ROUND(AVG(Keys), 2) as Keys,
    percentile(CAST(HC AS int), 0.50) as HC
FROM events
WHERE user_id IN (SELECT * FROM installs)
GROUP BY level, app_version, levels
""".format(first=first_version, second=second_version, second_dt=second_date)


## Dictionary of all queries.
QUERIES = {
    "query_session" : query_session,
    "query_funnel" : query_funnel,
    "query_drop_rate": query_drop_rate,
    "query_win_ratio": query_win_ratio,
    "query_economy" : query_economy,
    "query_economy_2" : query_economy_2,
    }


def run_querries(downloader=events_downloader):

    print("Running querries on Hive.")

    if not os.path.exists("datasets"):
        os.mkdir("datasets")
        print("Directory datasets created.")
    else:
        print("Directory datasets already exists.")

    for query_name, query in QUERIES.items():
        downloader.download_raw_events(
            query, "datasets/{}.pkl".format(query_name)
        )

    downloader.end_connection()

if __name__ == "__main__":
    run_querries()
