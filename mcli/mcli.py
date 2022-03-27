"""
Simple command-line interface to service

"""

# Standard library modules
import argparse
import cmd
import re

# Installed packages
import requests

# The services check only that we pass an authorization,
# not whether it's valid
DEFAULT_AUTH = 'Bearer A'


def parse_args():
    argp = argparse.ArgumentParser(
        'mcli',
        description='Command-line query interface to music service'
        )
    argp.add_argument(
        'name',
        help="DNS name or IP address of music server"
        )
    argp.add_argument(
        'port',
        type=int,
        help="Port number of music server"
        )
    argp.add_argument(
        'service',
        help="Microservice name"
        )
    return argp.parse_args()


def get_url(name, port, service):
    return "http://{}:{}/api/v1/{}/".format(name, port,service)


def parse_quoted_strings(arg):
    """
    Parse a line that includes words and '-, and "-quoted strings.
    This is a simple parser that can be easily thrown off by odd
    arguments, such as entries with mismatched quotes.  It's good
    enough for simple use, parsing "-quoted names with apostrophes.
    """
    mre = re.compile(r'''([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})|(\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*)|(\w+)|'([^']*)'|"([^"]*)"''')
    args = mre.findall(arg)
    return [''.join(a) for a in args]


class Mcli(cmd.Cmd):
    def __init__(self, args):
        self.name = args.name
        self.port = args.port
        self.service = args.service
        cmd.Cmd.__init__(self)
        self.prompt = 'mql: '
        self.intro = """
Command-line interface to music service.
Enter 'help' for command list.
'Tab' character autocompletes commands.
"""

    def do_read(self, arg):
        """
        Read a single song or list all songs.

        Parameters
        ----------
        song:  music_id (optional)
            The music_id of the song to read. If not specified,
            all songs are listed.

        Examples
        --------
        read 6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea
            Return "The Last Great American Dynasty".
        read
            Return all songs (if the server supports this).

        Notes
        -----
        Some versions of the server do not support listing
        all songs and will instead return an empty list if
        no parameter is provided.
        """
        url = get_url(self.name, self.port, self.service)

        # Connect music service
        if self.service == "music":
            r = requests.get(
                url+arg.strip(),
                headers={'Authorization': DEFAULT_AUTH}
                )
            if r.status_code != 200:
                print("Non-successful status code:", r.status_code)
            items = r.json()
            if 'Count' not in items:
                print("0 items returned")
                return
            print("{} items returned".format(items['Count']))
            for i in items['Items']:
                print("{}  {:20.20s} {}".format(
                    i['music_id'],
                    i['Artist'],
                    i['SongTitle']))

        # Connect user service
        elif self.service == "user":
            r = requests.get(
                url + arg.strip(),
                headers={'Authorization': DEFAULT_AUTH}
            )
            if r.status_code != 200:
                print("Non-successful status code: {}, {}"
                      .format(r.status_code, r.json()["error"]))
            items = r.json()
            if 'Count' not in items:
                print("0 items returned")
                return
            print("{} items returned".format(items['Count']))
            for i in items['Items']:
                print("{}  {} {} {}".format(
                    i['user_id'],
                    i['fname'],
                    i['lname'],
                    i["email"]))

         # Connect comment service
        elif self.service == "comment":
            r = requests.get(
                url + arg.strip(),
                headers={'Authorization': DEFAULT_AUTH}
            )
            if r.status_code != 200:
                print("Non-successful status code: {}, {}"
                      .format(r.status_code, r.json()["error"]))
            items = r.json()
            if 'Count' not in items:
                print("0 items returned")
                return
            print("{} items returned".format(items['Count']))
            for i in items['Items']:
                print("{}  {} {} {}".format(
                    i['comment_id'],
                    i['text'],
                    i['music_id'],
                    i["song_title"]))

    def do_create(self, arg):
        """
        Add a song to the database.

        Parameters
        ----------
        artist: string
        title: string

        Both parameters can be quoted by either single or double quotes.

        Examples
        --------
        create 'Steely Dan'  "Everyone's Gone to the Movies"
            Quote the apostrophe with double-quotes.

        create Chumbawamba Tubthumping
            No quotes needed for single-word artist or title name.
        """
        url = get_url(self.name, self.port, self.service)
        args = parse_quoted_strings(arg)
        if self.service == "music":
            if len(args) != 2:
                print("Not enough args provided {}".format(len(args)))
                return

            payload = {
                'Artist': args[0],
                'SongTitle': args[1]
            }
            r = requests.post(
                url,
                json=payload,
                headers={'Authorization': DEFAULT_AUTH}
            )
            print(r.json())

        elif self.service == "user":
            if len(args) != 3:
                print("Not enough or too many args provided {}".format(len(args)))
                return

            payload = {
                'fname': args[0],
                'lname': args[1],
                'email': args[2]
            }
            r = requests.post(
                url,
                json=payload,
                headers={'Authorization': DEFAULT_AUTH}
            )
            print(r.json())

        elif self.service == "comment":
            if len(args) != 3:
                print("Not enough or too many args provided {}".format(len(args)))
                return

            payload = {
                'test': args[0],
                'music_id': args[1],
                'song_title': args[2]
            }
            r = requests.post(
                url,
                json=payload,
                headers={'Authorization': DEFAULT_AUTH}
            )
            print(r.json())

    def do_delete(self, arg):
        """
        Delete a song.

        Parameters
        ----------
        song: music_id
            The music_id of the song to delete.

        Examples
        --------
        delete 6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea
            Delete "The Last Great American Dynasty".
        """
        url = get_url(self.name, self.port, self.service)
        args = parse_quoted_strings(arg)
        if self.service == "music":
            r = requests.delete(
                url+arg.strip(),
                headers={'Authorization': DEFAULT_AUTH}
                )
            if r.status_code != 200:
                print("Non-successful status code: {}, {}"
                      .format(r.status_code, r.json()["error"]))

        elif self.service == "user":
            r = requests.delete(
                url + arg.strip(),
                headers={'Authorization': DEFAULT_AUTH}
            )
            if r.status_code != 200:
                print("Non-successful status code: {}, {}"
                      .format(r.status_code, r.json()["error"]))

        elif self.service == "comment":
            r = requests.delete(
                url + arg.strip(),
                headers={'Authorization': DEFAULT_AUTH}
            )
            if r.status_code != 200:
                print("Non-successful status code: {}, {}"
                      .format(r.status_code, r.json()["error"]))

    def do_quit(self, arg):
        """
        Quit the program.
        """
        return True

    def do_test(self, arg):
        """
        Run a test stub on the music server.
        """
        url = get_url(self.name, self.port, self.service)
        r = requests.get(
            url+'test',
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)

    def do_shutdown(self, arg):
        """
        Tell the music cerver to shut down.
        """
        url = get_url(self.name, self.port,self.service)
        r = requests.get(
            url+'shutdown',
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)


if __name__ == '__main__':
    args = parse_args()
    Mcli(args).cmdloop()
