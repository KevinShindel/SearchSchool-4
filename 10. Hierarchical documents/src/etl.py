import json

from pandas import read_csv, merge, Series


def collect_to_dict(series: Series, keys: list):
    data = [dict(zip(keys, item)) for item in tuple(zip(*series.values))]
    return data


def main():
    movies_df = read_csv('movies.csv')
    tags_df = read_csv('tags.csv',
                       names=['tag_user_id', 'movieId', 'tag_value', 'tag_timestamp'],
                       skiprows=1)
    ratings_df = read_csv('ratings.csv',
                          names=['rating_user_id', 'movieId', 'rating_value', 'rating_timestamp'],
                          skiprows=1)

    movie_w_tags_df = merge(left=movies_df, right=tags_df, how='left', on='movieId')\
        .groupby(['movieId', 'title', 'genres'])\
        .agg({'tag_user_id': list, 'tag_value': list, 'tag_timestamp': list}).reset_index()

    final_df = merge(left=movie_w_tags_df, right=ratings_df, on='movieId', how='left')\
        .groupby(['movieId', 'title', 'genres'])\
        .agg({'rating_user_id': list, 'rating_value': list, 'rating_timestamp': list, 'tag_user_id': 'first',
              'tag_value': 'first', 'tag_timestamp': 'first'}).reset_index()

    rating_columns = ['userId', 'value', 'timestamp']

    final_df['rating'] = (final_df[['rating_user_id', 'rating_value', 'rating_timestamp']].
                          apply(lambda df: collect_to_dict(df, rating_columns), axis=1))

    tags_columns = ['userId', 'value', 'timestamp']

    final_df['tag'] = (final_df[['tag_user_id', 'tag_value', 'tag_timestamp']].
                       apply(lambda df: collect_to_dict(df, tags_columns), axis=1))

    records = final_df[['movieId', 'title', 'genres', 'rating', 'tag']].to_dict('records')

    with open('result.json', 'w') as handler:
        handler.write(json.dumps(records, indent=4))


if __name__ == '__main__':
    main()
