"""
Python  API for the user service.
"""

# Standard library modules

# Installed packages
import requests


class User():
    """Python API for the user service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the user service. Often
        'http://cmpt756s1:30000/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the user service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def create(self, email, fname, lname):
        """Create user.

        Parameters
        ----------
        email: string
            The email of the user.
        fname: string
            The first name of the user.
        lname: string
            The last name of the user.

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by User.
            The string is the UUID of this user in the user database.
        """
        payload = {'email': email, 'fname': fname, 'lname': lname}
        r = requests.post(
            self._url,
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['user_id']

    def read(self, u_id):
        """Read user info.

        Parameters
        ----------
        u_id: string
            The UUID of this user in the user database.

        Returns
        -------
        status, email, fname, lname

        status: number
            The HTTP status code returned by User.
        email: If status is 200, the email of the user.
          If status is not 200, None.
        fname: If status is 200, the first name of the user.
          If status is not 200, None.
        lname: If status is 200, the last name of the user..
          If status is not 200, None.
        """
        r = requests.get(
            self._url + u_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None, None, None

        item = r.json()['Items'][0]
        return r.status_code, item['email'], item['fname'], item['lname']

    def delete(self, u_id):
        """Delete user.

        Parameters
        ----------
        u_id: string
            The UUID of this user in the user database.

        Returns
        -------
        Does not return anything. The user delete operation
        always returns 200, HTTP success.
        """
        requests.delete(
            self._url + u_id,
            headers={'Authorization': self._auth}
        )
