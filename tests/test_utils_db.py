from utils.db import check_db_exists


def test_check_db_exits():
    # Database should always exist before bot polling starts
    # Else there is not point of running an instance without data
    r = check_db_exists()
    assert r == True
