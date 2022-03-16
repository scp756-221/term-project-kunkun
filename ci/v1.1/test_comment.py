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
import comment


@pytest.fixture
def cserv(request, comment_url, auth):
    return comment.Comment(comment_url, auth)


@pytest.fixture
def example(request):
    return ('It\'s a comment text', 'mock_music_id', 'I love 756')


def test_simple_run(cserv, example):
    trc, c_id = cserv.create(example[0], example[1], example[2])
    assert trc == 200
    trc, text, music_id, song_title = cserv.read(c_id)
    assert (trc == 200 and text == example[0] and music_id == example[1]
            and song_title == example[2])
    cserv.delete(c_id)
    # No status to check


@pytest.fixture
def updated_comment_text(request):
    # Recorded 1967
    return ('It\'s an updated comment text',
            'update_mock_music_id', 'I love 756')


@pytest.fixture
def c_id_comment_text(request, cserv, updated_comment_text):
    trc, c_id = cserv.create(updated_comment_text[0],
                             updated_comment_text[1],
                             updated_comment_text[2])
    assert trc == 200
    yield c_id
    # Cleanup called after the test completes
    cserv.delete(c_id)


def test_update_comment_text(cserv, c_id_comment_text):
    trc, text = cserv.read_comment_text(c_id_comment_text)
    assert trc == 200


def test_full_cycle(cserv):
    # Create a music record and save its id in the variable `c_id`
    # ... Fill in the test ...
    example = ('It\'s a comment text', 'mock_music_id', 'I love 756')
    trc, c_id = cserv.create(example[0], example[1], example[2])
    assert trc == 200
    trc, text, music_id, song_title = cserv.read(c_id)
    assert (trc == 200 and text == example[0] and music_id == example[1]
            and song_title == example[2])
    trc, text = cserv.read_comment_text(c_id)
    assert trc == 200

    # The last statement of the test
    cserv.delete(c_id)
