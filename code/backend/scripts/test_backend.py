#!/usr/bin/env python3
"""End-to-end smoke tests for the running dashboard backend."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from http.client import HTTPResponse
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


@dataclass
class ApiResponse:
    status: int
    body: object
    headers: dict[str, str]


class SmokeTest:
    def __init__(self, base_url: str, timeout: float, keep_data: bool, verbose: bool) -> None:
        """
            Define -
            Entry -
            Exit -
        """
        self.base_url = base_url
        self.timeout = timeout
        self.keep_data = keep_data
        self.verbose = verbose
        self.user_id: int | None = None
        self.discord_primary_id: int | None = None
        self.passed = 0

    def request(
        self,
        method: str,
        path: str,
        *,
        payload: object | None = None,
        token: str | None = None,
        expected: int | tuple[int, ...] = 200,
    ) -> ApiResponse:
        """
            Define -
            Entry -
            Exit -
        """
        expected_statuses = (expected,) if isinstance(expected, int) else expected
        headers = {"Accept": "application/json, text/html"}
        body = None
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"

        request = Request(
            urljoin(self.base_url, path.lstrip("/")),
            data=body,
            headers=headers,
            method=method,
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                result = self._response(response, expected_statuses, method, path, payload)
                self._print_request(method, path, result.status)
                return result
        except HTTPError as error:
            return self._response(error, expected_statuses, method, path, payload)
        except (URLError, TimeoutError) as error:
            raise RuntimeError(f"{method} {path} could not connect: {error}") from error

    @staticmethod
    def _response(
        response: HTTPResponse,
        expected_statuses: tuple[int, ...],
        method: str,
        path: str,
        payload: object | None,
    ) -> ApiResponse:
        """
            Define -
            Entry -
            Exit -
        """
        raw_body = response.read()
        text = raw_body.decode("utf-8", errors="replace")
        try:
            body = json.loads(text) if text else None
        except json.JSONDecodeError:
            body = text
        if response.status not in expected_statuses:
            request_fields = (
                ", ".join(payload.keys())
                if isinstance(payload, dict)
                else "none"
            )
            diagnosis = ""
            if method == "POST" and path == "/users" and response.status == 500:
                diagnosis = (
                    "\nDiagnosis: check PostgreSQL user_id_seq. The database may "
                    "generate an ID that already exists in the user table."
                )
            raise AssertionError(
                f"{method} {path}: expected {expected_statuses}, "
                f"got {response.status}: {text[:500]}\n"
                f"Request JSON fields: {request_fields}{diagnosis}"
            )
        return ApiResponse(response.status, body, dict(response.headers.items()))

    def _print_request(self, method: str, path: str, status: int) -> None:
        """
            Define -
            Entry -
            Exit -
        """
        if self.verbose:
            print(f"  {method:<6} {path:<28} -> {status}")

    def check(self, label: str, condition: bool, detail: str = "") -> None:
        """
            Define -
            Entry -
            Exit -
        """
        if not condition:
            raise AssertionError(f"{label}: {detail or 'assertion failed'}")
        self.passed += 1
        print(f"PASS  {label}")

    def wait_until_ready(self, attempts: int) -> None:
        """
            Define -
            Entry -
            Exit -
        """
        for attempt in range(1, attempts + 1):
            try:
                response = self.request("GET", "/", expected=200)
                if isinstance(response.body, str) and "Wunderbar Dashboard API" in response.body:
                    print(f"Backend ready at {self.base_url}")
                    return
            except (AssertionError, RuntimeError):
                pass
            if attempt < attempts:
                time.sleep(1)
        raise RuntimeError(
            f"Backend did not become ready after {attempts} seconds at {self.base_url}"
        )

    def run(self) -> None:
        """
            Define -
            Entry -
            Exit -
        """
        suffix = str(time.time_ns())[-10:]
        email = f"backend-smoke-{suffix}@example.test"
        username = f"backend_smoke_{suffix}"
        password = "SmokeTestPassword123!"
        updated_password = "UpdatedSmokePassword123!"
        user_payload = {
            "username": username,
            "email": email,
            "password": password,
            "first_name": "Backend",
            "last_name": "Smoke",
        }

        self._public_routes()
        try:
            created = self.request("POST", "/users", payload=user_payload, expected=201).body
            self.user_id = created["id"]
            self.check("create user", created["username"] == username)
            self.check("created user does not expose password", "password_hash" not in created)

            duplicate = self.request("POST", "/users", payload=user_payload, expected=409)
            self.check("duplicate user rejected", duplicate.body["detail"])

            listed = self.request("GET", "/users").body
            self.check("list users", any(user["id"] == self.user_id for user in listed))

            fetched = self.request("GET", f"/users/{self.user_id}").body
            self.check("get user", fetched["id"] == self.user_id)

            token_response = self.request(
                "POST", "/users/login", payload={"email": email, "password": password}
            ).body
            token = token_response["access_token"]
            self.check("login", bool(token))

            current = self.request("GET", "/users/me", token=token).body
            self.check("get current user", current["id"] == self.user_id)
            self.request("GET", "/users/me", token="invalid-token", expected=401)
            self.check("invalid token rejected", True)

            updated = self.request(
                "PATCH",
                f"/users/{self.user_id}",
                payload={
                    "username": f"{username}_updated",
                    "email": f"updated-{email}",
                    "password": updated_password,
                    "first_name": "Updated",
                    "last_name": "User",
                    "status": "active",
                },
            ).body
            self.check("update user", updated["first_name"] == "Updated")

            updated_login = self.request(
                "POST",
                "/users/login",
                payload={"email": f"updated-{email}", "password": updated_password},
            ).body
            self.check("login with updated credentials", bool(updated_login["access_token"]))

            self._discord_routes()

            self.request("DELETE", f"/users/{self.user_id}", expected=204)
            self.user_id = None
            self.request("GET", f"/users/{created['id']}", expected=404)
            self.check("deleted user returns 404", True)
        finally:
            self.cleanup()

    def _public_routes(self) -> None:
        """
            Define -
            Entry -
            Exit -
        """
        root = self.request("GET", "/").body
        self.check("root endpoint", isinstance(root, str) and "Status: running" in root)
        about = self.request("GET", "/about.json").body
        self.check("about endpoint", isinstance(about, dict) and "server" in about)
        services = about["server"]["services"]
        widget_names = {
            widget["name"]
            for service in services
            for widget in service["widgets"]
        }
        self.check(
            "about endpoint lists widgets",
            {"discord_profile", "discord_banner", "steam_profile", "steam_currentgame", "steam_lastgame", "meteo"}
            <= widget_names,
        )
        self.request("GET", "/auth/")
        self.check("auth details endpoint", True)
        discord_status = self.request("GET", "/auth/discord/").body
        self.check("Discord status endpoint", discord_status == {"service": "discord", "status": "implemented"})
        steam_status = self.request("GET", "/auth/steam/").body
        self.check("Steam status endpoint", steam_status == {"service": "steam", "status": "not implemented"})
        weather_status = self.request("GET", "/auth/weather/").body
        self.check("Weather status endpoint", weather_status == {"service": "weather", "status": "implemented"})
        openapi = self.request("GET", "/openapi.json").body
        self.check("OpenAPI endpoint", isinstance(openapi, dict) and "paths" in openapi)

    def _discord_routes(self) -> None:
        """
            Define -
            Entry -
            Exit -
        """
        payload = {
            "id": int(str(time.time_ns())[-9:]),
            "username": "backend-smoke",
            "global_name": "Backend Smoke",
            "email": "backend-smoke@example.test",
            "avatar": "smoke-avatar",
        }
        created = self.request("POST", "/discord", payload=payload, expected=201).body
        self.discord_primary_id = created["primary_id"]
        self.check("create Discord record", created["id"] == payload["id"])

        listed = self.request("GET", "/discord").body
        self.check("list Discord records", any(item["primary_id"] == self.discord_primary_id for item in listed))
        exists = self.request("GET", f"/discord/{self.discord_primary_id}/exists").body
        self.check("Discord exists endpoint", exists == {"exists": True})
        fetched = self.request("GET", f"/discord/{self.discord_primary_id}").body
        self.check("get Discord record", fetched["primary_id"] == self.discord_primary_id)

        updated = self.request(
            "PATCH",
            f"/discord/{self.discord_primary_id}",
            payload={
                "username": "backend-smoke-updated",
                "global_name": "Backend Smoke Updated",
                "email": "backend-smoke-updated@example.test",
                "avatar": "updated-avatar",
            },
        ).body
        self.check("update Discord record", updated["username"] == "backend-smoke-updated")

        self.request("DELETE", f"/discord/{self.discord_primary_id}", expected=204)
        self.discord_primary_id = None

    def cleanup(self) -> None:
        """
            Define -
            Entry -
            Exit -
        """
        if self.keep_data:
            return
        if self.discord_primary_id is not None:
            try:
                self.request("DELETE", f"/discord/{self.discord_primary_id}", expected=(204, 404))
            except (AssertionError, RuntimeError):
                pass
        if self.user_id is not None:
            try:
                self.request("DELETE", f"/users/{self.user_id}", expected=(204, 404))
            except (AssertionError, RuntimeError):
                pass


def parse_args() -> argparse.Namespace:
    """
        Define -
        Entry -
        Exit -
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        default=os.getenv("BACKEND_URL", "http://localhost:8080"),
        help="Backend base URL (default: BACKEND_URL or http://localhost:8080)",
    )
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds")
    parser.add_argument("--wait", type=int, default=30, help="Seconds to wait for backend startup")
    parser.add_argument(
        "--keep-data",
        action="store_true",
        help="Keep the generated user and Discord record instead of cleaning them up",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print every HTTP request and response status",
    )
    return parser.parse_args()


def main() -> int:
    """
        Define -
        Entry -
        Exit -
    """
    args = parse_args()
    smoke_test = SmokeTest(args.base_url, args.timeout, args.keep_data, args.verbose)
    try:
        smoke_test.wait_until_ready(args.wait)
        smoke_test.run()
    except (AssertionError, RuntimeError, KeyError, TypeError) as error:
        print(f"FAIL  {error}", file=sys.stderr)
        return 1
    print(f"\n{smoke_test.passed} checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
