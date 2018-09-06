from pysrc.file_management.file_parser import create_json_entry, file_parser_json, update_json_entry
from pysrc.webmention.mentioner import send_mention
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.ini')

# configuration
DATABASE = config.get('Global', 'Database')
DEBUG = config.get('Global', 'Debug')
SECRET_KEY = config.get('Global', 'DevKey')
USERNAME = config.get('SiteAuthentication', "Username")
PASSWORD = config.get('SiteAuthentication', 'password')
DOMAIN_NAME = config.get('Global', 'DomainName')
# the url to use for showing recent bulk uploads


def bridgy_twitter(location):
    """send a twitter mention to brid.gy"""
    location = 'http://' + DOMAIN_NAME + location
    r = send_mention(
        location,
        'https://brid.gy/publish/twitter',
        endpoint='https://brid.gy/publish/webmention'
    )
    syndication = r.json()
    data = file_parser_json('data/' + location.split('/e/')[1] + ".json", md=False)
    old_entry = data
    if data['syndication']:
        print syndication
        if type(data['syndication']) is unicode:
            data['syndication'] = data['syndication'].split(',')
        data['syndication'].append(syndication['url'])
    else:
        try:
            data['syndication'] = [syndication['url']]
        except KeyError:
            raise KeyError("There was no url! {0}".format(syndication))
    data['twitter'] = {'url': syndication['url'], 'id': syndication['id']}
    update_json_entry(data=data, old_entry=old_entry, g=None)


