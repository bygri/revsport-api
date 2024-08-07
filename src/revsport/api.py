from bs4 import BeautifulSoup
import pyotp
import requests


class RevSportAPI:
    """
    Usage:

    >>> api = RevSportAPI("my-portal-name")
    >>> api.login_old("username", "password")
    >>> data = api.fetch_members()
    >>> print(data)
    """

    portal_name = None
    session = requests.Session()

    def __init__(self, portal: str) -> None:
        self.portal_name = portal

    def login(self, username: str, password: str, tfa: str) -> None:
        """
        Log in to RS using two-factor authentication.

        `tfa` is 2FA string in the format `otpauth://totp/...`

        If using only old-design functions, you can use `login_old()` instead.
        """
        get = self.session.get(
            f"https://portal.revolutionise.com.au/{self.portal_name}/login"
        )
        soup = BeautifulSoup(get.text, "html.parser")
        # Username/password
        token = soup.find("input", attrs={"name": "_token"})["value"]
        post = self.session.post(
            f"https://portal.revolutionise.com.au/{self.portal_name}/login",
            data={
                "_token": token,
                "username": username,
                "password": password,
            },
        )
        soup = BeautifulSoup(post.text, "html.parser")
        # 2FA
        token = soup.find("input", attrs={"name": "_token"})["value"]
        self.session.post(
            f"https://portal.revolutionise.com.au/{self.portal_name}/tfa",
            data={
                "_token": token,
                "authentication-code": pyotp.parse_uri(tfa).now(),
            },
        )
        # Also authenticate with the old design
        self.login_old(username, password)

    def login_old(self, username: str, password: str) -> None:
        """
        Log in to RS without using two-factor authentication. Only old-design
        functions will work.
        """
        get = self.session.get(
            "https://client.revolutionise.com.au/?clientName="
            f"{self.portal_name}&page=/{self.portal_name}/"
        )
        soup = BeautifulSoup(get.text, "html.parser")
        # Username/password
        token = soup.find("input", attrs={"name": "_csrf"})["value"]
        self.session.post(
            "https://client.revolutionise.com.au/"
            f"{self.portal_name}/scripts/login/client/",
            data={
                "_csrf": token,
                "redirect": f"/{self.portal_name}/",
                "user": username,
                "password": password,
            },
        )

    def fetch_members(
        self,
        *,
        address_format: str = "separate",
        name_order: str = "split",
        season_id: int = 0,
    ) -> str:
        """
        Retrieve a full list of members in CSV format.

        Requires `login_old()` to be called first.

        `season_id` must be sourced from RevSport's UI, or omit to use the
        current season.
        """
        get = self.session.get(
            "https://client.revolutionise.com.au/"
            f"{self.portal_name}/members/reports/"
        )
        soup = BeautifulSoup(get.text, "html.parser")
        token = soup.find("input", attrs={"name": "_csrf"})["value"]
        # TODO: find the `name` of all inputs with name like `custom[33724]` or
        # `accred[2132]` or `course[1219]` and set them in post data
        # NB with courses, the value is not 1 but the course ID number e.g. 1219
        post = self.session.post(
            "https://client.revolutionise.com.au/"
            f"{self.portal_name}/reports/members/download/",
            data={
                "_csrf": token,
                "file_format": "csv",
                "season_id": season_id,
                "filterby": "",
                "orderby": "nationalMemberID",
                "direction": "asc",
                "nameorder": name_order,
                "addressformat": address_format,
                # Basic details
                "parentID": "1",
                "fullname": "1",
                "dateofbirth": "1",
                "gender": "1",
                "joindate": "1",
                # Contact details
                "address": "1",
                "homephone": "1",
                "mobile": "1",
                "email": "1",
                "email_other": "1",
                # Payment information
                "paymentstatus": "1",
                "paymentmethod": "1",
                "paymentdate": "1",
                "paymentreceipt": "1",
                "paymentwho": "1",
                # Administrative information
                "teams": "1",
                "primary_family_member": "1",
                "username": "1",
                "perms": "1",
                "last_updated": "1",
            },
        )
        return post.text
