"""
Test the *_original_artist routines.

These tests are invoked by running `pytest` with the
appropriate options and environment variables, as
defined in `conftest.py`.
"""

# Standard libraries

# Installed packages
import pytest

# Local modules
import user


@pytest.fixture
def userv(request, user_url, auth):
    return user.User(user_url, auth)


@pytest.fixture
def user_example(request):
    return ('fjs***@sfu.ca', 'Jingshan', 'Feng')


def test_simple_run(userv, user_example):
    trc, u_id = userv.create(user_example[0], user_example[1], user_example[2])
    assert trc == 200
    trc, email, fname, lname = userv.read(u_id)
    assert (trc == 200
            and email == user_example[0]
            and fname == user_example[1]
            and lname == user_example[2])
    userv.delete(u_id)
    # No status to check
