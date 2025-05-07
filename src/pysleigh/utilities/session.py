import requests
from typing import Optional
from pysleigh.utilities.logger import AoCLogger
from pysleigh.utilities.config import AoCConfig


class AoCSession:
    logger = AoCLogger().get_logger()

    def __init__(self, config: Optional[AoCConfig] = None) -> None:
        config = config or AoCConfig()
        self.session_cookie = config.config.get("session_cookie", {}).get(
            "session_cookie", ""
        )

        if not self.session_cookie:
            self.logger.warning("No session cookie provided. AoC requests may fail.")

        self.session = self.build_session()

    def build_session(self) -> requests.Session:
        session = requests.Session()
        session.cookies.set("session", self.session_cookie)
        session.headers.update({"User-Agent": "PySleigh/0.1"})
        self.logger.info("Built authenticated AoC Session")
        return session

    def get(self, url: str, **kwargs) -> requests.Response:
        """
        Make a GET request to the specified URL with the session's cookies and headers.

        Args:
            url (str): The URL to send the GET request to.
            **kwargs: Additional keyword arguments to pass to the requests.get() method.

        Returns:
            requests.Response: The response object from the GET request.
        """
        self.logger.debug(f"Making GET request to {url}")
        response = self.session.get(url, **kwargs)
        self.logger.info(f"GET {url} - Status {response.status_code}")
        return response

    def post(
        self, url: str, data: Optional[dict] = None, **kwargs
    ) -> requests.Response:
        """
        Make a POST request to the specified URL with the session's cookies and headers.

        Args:
            url (str): The URL to send the POST request to.
            data (dict, optional): The data to send in the POST request. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the requests.post() method.

        Returns:
            requests.Response: The response object from the POST request.
        """
        self.logger.debug(f"Making POST request to {url} with data: {data}")
        response = self.session.post(url, data=data, **kwargs)
        self.logger.info(f"POST {url} - Status {response.status_code}")
        return response
