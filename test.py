from utils import get_query_config, get_db_query
from filters import filter_pgdb
from db import get_db_response

database_url = "dbname=dsp host=192.168.1.140 port=7000 user=postgres password=postgres"

def filter_ad_break(playlist_item):
    return playlist_item

filters_repo = {
    "filter_ad_break": {
        "type": "data-driven",
        "function": filter_ad_break,
        "args": ["playlist_item"],
    },
    "filter_is_premium": {
        "type": "code",
        "code": """def filter_is_premium(playlist_item):
    query_config = get_query_config(
        ["is_premium"],
        {
            "item_selection_key": "xx123xx",
            "table_selection_column": "media_id",
        },
        False,
        "is_premium",
        "premium_assets",
    )
    query = get_db_query(query_config)
    response = get_db_response(
        query, "dbname=dsp host=192.168.1.140 port=7000 user=postgres password=postgres"
    )
    is_premium = response[0][0]
    playlist_item[query_config["target_key"]] = is_premium
    return playlist_item
""",
        "args": ["playlist_item"],
    },
}


def execute_filter(filters_repo, params):
    playlist_item = params["playlist_item"]
    for filter_name, filter_attributes in filters_repo.items():
        if filter_attributes["type"] == "code":
            exec(filter_attributes["code"])
            filter_args = [params.get(arg) for arg in filter_attributes["args"]]
            playlist_item = locals().get(filter_name)(*filter_args)
        else:
            filter_args = [params[arg] for arg in filter_attributes["args"]]
            playlist_item = filter_attributes["function"](filter_args)
    return playlist_item
