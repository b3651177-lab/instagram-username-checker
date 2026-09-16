"""
Instagram Username Checker
---------------------------
Checks whether Instagram usernames are available (not registered).

Usage:
    python checker.py alice bob c00lname123

Notes:
- Uses Instagram's public profile pages (instagram.com/<username>).
  A 404 response generally means the username is NOT taken.
- Instagram actively rate-limits / blocks automated traffic. This script
  adds randomized delays between requests, but for heavy use you will
  likely need rotating proxies and/or a real browser (Selenium) fallback.
- Respect Instagram's Terms of Service. Use responsibly.
"""

import time
import random
import sys
from dataclasses import dataclass
from typing import Optional

import requests
from bs4 import BeautifulSoup


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


@dataclass
class CheckResult:
    username: str
    available: Optional[bool]  # True = available, False = taken, None = unknown/error
    status_code: Optional[int]
    note: str = ""


class InstagramUsernameChecker:
    def __init__(self, min_delay: float = 2.0, max_delay: float = 5.0, timeout: int = 10):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        })

    def _sleep(self):
        time.sleep(random.uniform(self.min_delay, self.max_delay))

    def is_username_available(self, username: str) -> CheckResult:
        """
        Checks a single username against Instagram's public profile page.
        Returns a CheckResult with available=True/False/None.
        """
        url = f"https://www.instagram.com/{username}/"

        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
        except requests.RequestException as e:
            return CheckResult(username, None, None, note=f"request error: {e}")

        status = response.status_code

        # 404 -> profile page not found -> username likely available
        if status == 404:
            return CheckResult(username, True, status, note="404 Not Found (likely available)")

        # 200 -> page loaded; need to check content, since Instagram may
        # return 200 with a "Sorry, this page isn't available" message too.
        if status == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            page_text = soup.get_text(separator=" ", strip=True).lower()

            not_found_markers = [
                "sorry, this page isn't available",
                "page not found",
            ]
            if any(marker in page_text for marker in not_found_markers):
                return CheckResult(username, True, status, note="taken-page marker found (likely available)")

            return CheckResult(username, False, status, note="profile page loaded (likely taken)")

        if status == 429:
            return CheckResult(username, None, status, note="rate limited (429) - slow down / use proxies")

        return CheckResult(username, None, status, note=f"unexpected status {status}")

    def check_many(self, usernames: list[str]) -> list[CheckResult]:
        results = []
        for i, name in enumerate(usernames):
            result = self.is_username_available(name)
            results.append(result)
            print(self._format_result(result))
            if i < len(usernames) - 1:
                self._sleep()
        return results

    @staticmethod
    def _format_result(result: CheckResult) -> str:
        if result.available is True:
            tag = "AVAILABLE"
        elif result.available is False:
            tag = "TAKEN"
        else:
            tag = "UNKNOWN"
        return f"[{tag}] {result.username} (status={result.status_code}, {result.note})"


def main():
    if len(sys.argv) < 2:
        print("Usage: python checker.py <username1> [username2] ...")
        sys.exit(1)

    usernames = sys.argv[1:]
    checker = InstagramUsernameChecker()
    checker.check_many(usernames)


if __name__ == "__main__":
    main()
