"""
Python  API for the comment service.
"""

# Standard library modules

# Installed packages
import requests


class Comment():
    """Python API for the comment service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the comment service. Often
        'http://cmpt756s3:30003/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the comment service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def create(self, text, music_id, song_title):
        """Create comment.

        Parameters
        ----------
        text: string
            The comment text.
        music_id: string
            The id of the song.
        song_title: string
            The name of the song.

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by Comment.
            The string is the UUID of this comment in the comment database.
        """
        payload = {'text': text,
                   'music_id': music_id,
                   'song_title': song_title}
        r = requests.post(
            self._url,
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['comment_id']

    def write_comment_text(self, c_id, text):
        """Write the updated comment text.

        Parameters
        ----------
        c_id: string
            The UUID of this comment in the comment database.

        text: string
            Newest comment text.

        Returns
        -------
        number
            The HTTP status code returned by the comment service.
        """
        r = requests.put(
            self._url + 'write_comment_text/' + c_id,
            json={'text': text},
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def read_comment_text(self, c_id):
        """Read the comment text of a comment.

        Parameters
        ----------
        c_id: string
            The UUID of this comment in the comment database.

        Returns
        -------
        status, text

        status: number
            The HTTP status code returned by Comment.
        text:
          If status is 200, the comment text.
          If status is not 200, None.
        """
        r = requests.get(
            self._url + 'read_comment_text/' + c_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None
        item = r.json()
        return r.status_code, item['text']

    def read(self, c_id):
        """Read comment.

        Parameters
        ----------
        c_id: string
            The UUID of this comment in the comment database.

        Returns
        -------
        status, text, music_id, song_title

        status: number
            The HTTP status code returned by Comment.
        text: If status is 200, the comment text.
          If status is not 200, None.
        music_id: If status is 200, the id of the song.
          If status is not 200, None.
        song_title: If status is 200, the name of the song.
          If status is not 200, None.
        """
        r = requests.get(
            self._url + c_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None, None, None

        item = r.json()['Items'][0]
        return (r.status_code, item['text'],
                item['music_id'], item['song_title'])

    def delete(self, c_id):
        """Delete comment.

        Parameters
        ----------
        c_id: string
            The UUID of this comment in the comment database.

        Returns
        -------
        Does not return anything. The comment delete operation
        always returns 200, HTTP success.
        """
        requests.delete(
            self._url + c_id,
            headers={'Authorization': self._auth}
        )
