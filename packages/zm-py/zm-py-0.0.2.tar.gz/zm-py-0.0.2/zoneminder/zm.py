"""An API Client to interact with ZoneMinder."""
import logging
from typing import List
from urllib.parse import urljoin

import requests

from zoneminder.monitor import Monitor

_LOGGER = logging.getLogger(__name__)


class ZoneMinder:
    """The ZoneMinder API client itself. Create one of these to begin."""

    DEFAULT_SERVER_PATH = '/zm/'
    DEFAULT_ZMS_PATH = '/zm/cgi-bin/nph-zms'
    DEFAULT_TIMEOUT = 10
    LOGIN_RETRIES = 2
    MONITOR_URL = 'api/monitors.json'

    def __init__(self, server_host, username, password,
                 server_path=DEFAULT_SERVER_PATH,
                 zms_path=DEFAULT_ZMS_PATH, verify_ssl=True) -> None:
        """Create a ZoneMinder API Client."""
        self._server_url = urljoin(server_host, server_path)
        self._username = username
        self._password = password
        self._zms_path = zms_path
        self._verify_ssl = verify_ssl
        self._cookies = None

    def login(self):
        """Login to the ZoneMinder API."""
        _LOGGER.debug("Attempting to login to ZoneMinder")

        login_post = {'view': 'console', 'action': 'login'}
        if self._username:
            login_post['username'] = self._username
        if self._password:
            login_post['password'] = self._password

        req = requests.post(urljoin(self._server_url, '/index.php'),
                            data=login_post, verify=self._verify_ssl)
        self._cookies = req.cookies

        # Login calls returns a 200 response on both failure and success.
        # The only way to tell if you logged in correctly is to issue an api
        # call.
        req = requests.get(
            urljoin(self._server_url, 'api/host/getVersion.json'),
            cookies=self._cookies,
            timeout=ZoneMinder.DEFAULT_TIMEOUT,
            verify=self._verify_ssl)

        if not req.ok:
            _LOGGER.error("Connection error logging into ZoneMinder")
            return False

        return True

    def get_state(self, api_url) -> dict:
        """Perform a GET request on the specified ZoneMinder API URL."""
        return self._zm_request('get', api_url)

    def change_state(self, api_url, post_data) -> dict:
        """Perform a POST request on the specific ZoneMinder API Url."""
        return self._zm_request('post', api_url, post_data)

    def _zm_request(self, method, api_url, data=None) -> dict:
        """Perform a request to the ZoneMinder API."""
        # Since the API uses sessions that expire, sometimes we need to re-auth
        # if the call fails.
        for _ in range(ZoneMinder.LOGIN_RETRIES):
            req = requests.request(
                method, urljoin(self._server_url, api_url), data=data,
                cookies=self._cookies, timeout=ZoneMinder.DEFAULT_TIMEOUT,
                verify=self._verify_ssl)

            if not req.ok:
                self.login()
            else:
                break

        else:
            _LOGGER.error("Unable to get API response from ZoneMinder")

        try:
            return req.json()
        except ValueError:
            _LOGGER.exception('JSON decode exception caught while attempting '
                              'to decode "%s"', req.text)
            return {}

    def get_monitors(self) -> List[Monitor]:
        """Get a list of Monitors from the ZoneMinder API."""
        raw_monitors = self._zm_request('get', ZoneMinder.MONITOR_URL)
        if not raw_monitors:
            _LOGGER.warning("Could not fetch monitors from ZoneMinder")
            return []

        monitors = []
        for i in raw_monitors['monitors']:
            raw_monitor = i['Monitor']

            if raw_monitor['Function'] == 'None':
                _LOGGER.info("Skipping camera %s", raw_monitor['Id'])
                continue

            _LOGGER.info("Initializing camera %s", raw_monitor['Id'])
            monitors.append(
                Monitor(self, raw_monitor))

        return monitors

    def get_zms_url(self) -> str:
        """Get the url to the current ZMS instance."""
        return urljoin(self._server_url, self._zms_path)

    def get_url_with_auth(self, url) -> str:
        """Add the auth credentials to a url (if needed)."""
        if not self._username:
            return url

        url += '&user={:s}'.format(self._username)

        if not self._password:
            return url

        return url + '&pass={:s}'.format(self._password)
