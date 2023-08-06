"""
Tools for using a fake implementation of Vuforia.
"""

import email.utils
import re
import uuid
from contextlib import ContextDecorator
from typing import Optional, Tuple, Union
from urllib.parse import urljoin

from requests_mock.mocker import Mocker

from ._constants import States
from ._mock_web_query_api import MockVuforiaWebQueryAPI
from ._mock_web_services_api import MockVuforiaWebServicesAPI
from ._version import get_versions


class MockVWS(ContextDecorator):
    """
    Route requests to Vuforia's Web Service APIs to fakes of those APIs.

    This creates a mock which uses access keys from the environment.
    See the README to find which secrets to set.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        base_vws_url: str = 'https://vws.vuforia.com',
        base_vwq_url: str = 'https://cloudreco.vuforia.com',
        real_http: bool=False,
        state: States=States.WORKING,
        server_access_key: Optional[str]=None,
        server_secret_key: Optional[str]=None,
        client_access_key: Optional[str]=None,
        client_secret_key: Optional[str]=None,
        database_name: Optional[str]=None,
        processing_time_seconds: Union[int, float]=0.5,
        query_recognizes_deletion_seconds: Union[int, float]=3,
    ) -> None:
        """
        Args:
            real_http: Whether or not to forward requests to the real server if
                they are not handled by the mock.
                See
                http://requests-mock.readthedocs.io/en/latest/mocker.html#real-http-requests
            state: The state of the services being mocked.
            database_name: The name of the mock VWS target manager database.
                By default this is a random string.
            server_access_key: A VWS server access key for the mock.
            server_secret_key: A VWS server secret key for the mock.
            client_access_key: A VWS client access key for the mock.
            client_secret_key: A VWS client secret key for the mock.
            processing_time_seconds: The number of seconds to process each
                image for. In the real Vuforia Web Services, this is not
                deterministic.
            base_vwq_url: The base URL for the VWQ API.
            base_vws_url: The base URL for the VWS API.
            query_recognizes_deletion_seconds: The number of seconds after a
                target has been deleted that the query endpoint will return a
                500 response for on a match.


        Attributes:
            server_access_key (str): A VWS server access key for the mock.
            server_secret_key (str): A VWS server secret key for the mock.
            database_name (str): The name of the mock VWS target manager
                database.
        """
        super().__init__()

        if database_name is None:
            database_name = uuid.uuid4().hex

        if server_access_key is None:
            server_access_key = uuid.uuid4().hex

        if server_secret_key is None:
            server_secret_key = uuid.uuid4().hex

        if client_access_key is None:
            client_access_key = uuid.uuid4().hex

        if client_secret_key is None:
            client_secret_key = uuid.uuid4().hex

        self._real_http = real_http
        self._mock = Mocker()
        self._state = state
        self._processing_time_seconds = processing_time_seconds

        self.server_access_key = server_access_key
        self.server_secret_key = server_secret_key
        self.client_access_key = client_access_key
        self.client_secret_key = client_secret_key
        self.database_name = database_name

        self._base_vws_url = base_vws_url
        self._base_vwq_url = base_vwq_url

        self._query_recognizes_deletion_seconds = (
            query_recognizes_deletion_seconds
        )

    def __enter__(self) -> 'MockVWS':
        """
        Start an instance of a Vuforia mock with access keys set from
        environment variables.

        Returns:
            ``self``.
        """
        mock_vws_api = MockVuforiaWebServicesAPI(
            database_name=self.database_name,
            server_access_key=self.server_access_key,
            server_secret_key=self.server_secret_key,
            state=self._state,
            processing_time_seconds=self._processing_time_seconds,
        )

        mock_vwq_api = MockVuforiaWebQueryAPI(
            client_access_key=self.client_access_key,
            client_secret_key=self.client_secret_key,
            mock_web_services_api=mock_vws_api,
            query_recognizes_deletion_seconds=(
                self._query_recognizes_deletion_seconds
            ),
        )

        date = email.utils.formatdate(None, localtime=False, usegmt=True)

        headers = {
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Server': 'nginx',
            'Date': date,
        }

        with Mocker(real_http=self._real_http) as mock:
            for route in mock_vws_api.routes:
                url_pattern = urljoin(
                    base=self._base_vws_url,
                    url=route.path_pattern + '$',
                )

                for http_method in route.http_methods:
                    mock.register_uri(
                        method=http_method,
                        url=re.compile(url_pattern),
                        text=getattr(mock_vws_api, route.route_name),
                        headers=headers,
                    )

            for route in mock_vwq_api.routes:
                url_pattern = urljoin(
                    base=self._base_vwq_url,
                    url=route.path_pattern + '$',
                )

                for http_method in route.http_methods:
                    mock.register_uri(
                        method=http_method,
                        url=re.compile(url_pattern),
                        text=getattr(mock_vwq_api, route.route_name),
                        headers=headers,
                    )

        self._mock = mock
        self._mock.start()
        return self

    def __exit__(self, *exc: Tuple[None, None, None]) -> bool:
        """
        Stop the Vuforia mock.

        Returns:
            False
        """
        # __exit__ needs this to be passed in but vulture thinks that it is
        # unused, so we "use" it here.
        for _ in (exc, ):
            pass

        self._mock.stop()
        return False


__version__ = get_versions()['version']  # type: ignore
del get_versions
