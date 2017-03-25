import hypothesis
from hypothesis import strategies
from hypothesis.searchstrategy import SearchStrategy

from beylerbey.data_access import is_db_uri_mysql
from beylerbey.data_access.utils import MYSQL_DRIVER_NAME_PREFIX
from sqlalchemy.engine.url import URL
from tests.utils import sync


def extend_mysql_db_uri_like_strings_strategy(
        child: SearchStrategy) -> SearchStrategy:
    res = (strategies
           .tuples(child, strategies.text(min_size=1)))
    return res.map(''.join)


mysql_empty_db_uri_strategy = strategies.builds(
    URL,
    drivername=strategies.just(MYSQL_DRIVER_NAME_PREFIX))
non_mysql_like_driver_names_strategy = strategies.text(
    alphabet=strategies.characters(blacklist_characters=set(MYSQL_DRIVER_NAME_PREFIX)))
non_mysql_empty_db_uri_strategy = strategies.builds(
    URL,
    drivername=non_mysql_like_driver_names_strategy)


@hypothesis.given(mysql_empty_db_uri=mysql_empty_db_uri_strategy,
                  non_mysql_empty_db_uri=non_mysql_empty_db_uri_strategy)
@hypothesis.settings(perform_health_check=False)
@sync
async def test_is_db_uri_mysql(mysql_empty_db_uri: URL,
                               non_mysql_empty_db_uri: URL) -> None:
    assert await is_db_uri_mysql(mysql_empty_db_uri)
    assert not await is_db_uri_mysql(non_mysql_empty_db_uri)
