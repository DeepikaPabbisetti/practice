import inspect

from test import execute_filter, filters_repo
from response import playlist


def extract_params(function_name, localnamespace, playlist_item):
    sig = inspect.signature(function_name)
    params = [param.name for param in sig.parameters.values()]
    values = [localnamespace.get(param, None) for param in params]

    params_dict = {param: localnamespace.get(param, None) for param in params}
    params_dict["playlist_item"] = playlist_item
    return params_dict


def create_media_feed(
    db_tables,
    PURCHASE_URL,
    table_name,
    entitlecheck,
    jwplayer_secret,
    geo_location,
    cloudfront_context,
    override_type,
):
    global playlist
    # print(playlist)
    playlist_item = playlist['playlist'][0]
    params = extract_params(
        create_media_feed, locals(), playlist_item
    )
    playlist = execute_filter(filters_repo, params)
    print("Final playlist:", playlist)


create_media_feed(
    db_tables=[],
    PURCHASE_URL="",
    table_name="",
    entitlecheck="",
    jwplayer_secret="",
    geo_location="",
    cloudfront_context="",
    override_type="",
)
# print(playlist["playlist"][0])