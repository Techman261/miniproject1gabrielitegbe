# INF601 - Advanced Programming in Python
# Gabriel Itegbe
# Mini Project 1

import os
import requests

BASE = "https://practice.fhsucyber.com"
TOKEN = os.environ.get("PRACTICE_API_TOKEN")


# --- Exceptions ------------------------------------------------------------
class ApiError(Exception):
    """Base class for any error returned by the PracticeHub API."""

    def __init__(self, message, status=None):
        super().__init__(message)
        self.message = message
        self.status = status


class AuthError(ApiError):
    """401 - the token is missing, expired, or not valid."""


class ForbiddenError(ApiError):
    """403 - authenticated, but this post belongs to someone else."""


class NotFoundError(ApiError):
    """404 - no post with that id."""


class ValidationError(ApiError):
    """422 - the server understood the request but the data was invalid."""

    def __init__(self, message, status=None, errors=None):
        super().__init__(message, status)
        self.errors = errors or []


def server_detail(resp):
    """Pull a message out of the error body, if there is one."""
    try:
        payload = resp.json()
    except ValueError:
        return "", None
    if isinstance(payload, dict):
        for key in ("detail", "message", "error"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip(), payload
    return "", payload


def field_errors(payload):
    """Flatten 422 field errors into 'field: problem' strings."""
    problems = []
    if not isinstance(payload, dict):
        return problems

    errors = payload.get("errors")
    if isinstance(errors, dict):
        for field, messages in errors.items():
            if isinstance(messages, (list, tuple)):
                for message in messages:
                    problems.append(f"{field}: {message}")
            else:
                problems.append(f"{field}: {messages}")
    elif isinstance(errors, list):
        for item in errors:
            if isinstance(item, dict):
                field = item.get("field", "request")
                problems.append(f"{field}: {item.get('message', item)}")
            else:
                problems.append(str(item))

    detail = payload.get("detail")
    if isinstance(detail, list):
        for item in detail:
            if isinstance(item, dict):
                loc = item.get("loc") or []
                field = ".".join(str(p) for p in loc[1:]) or "request"
                problems.append(f"{field}: {item.get('msg', 'invalid value')}")

    return problems


def check(resp, what=""):
    """Raise the matching ApiError instead of letting raise_for_status crash."""
    if resp.status_code < 400:
        return

    detail, payload = server_detail(resp)
    where = f" ({what})" if what else ""

    if resp.status_code == 401:
        raise AuthError(
            detail or "Not authenticated. Check that PRACTICE_API_TOKEN is set and current.",
            401,
        )
    if resp.status_code == 403:
        raise ForbiddenError(
            detail or f"You don't have permission to do that{where}. "
                      "Posts can only be changed by the account that created them.",
            403,
        )
    if resp.status_code == 404:
        raise NotFoundError(detail or f"Nothing found{where}.", 404)
    if resp.status_code == 422:
        raise ValidationError(
            detail or "The server rejected the data that was sent.",
            422,
            field_errors(payload),
        )
    raise ApiError(
        detail or f"Unexpected response from the server (HTTP {resp.status_code}).",
        resp.status_code,
    )


def report(exc):
    """Print an ApiError the way a user should see it - no traceback."""
    print(f"[{exc.status or 'error'}] {exc.message}")
    for problem in getattr(exc, "errors", []):
        print(f"        - {problem}")


class PracticeHubClient:
    def __init__(self, base_url, token):
        self.base = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {token}"}

    def create_post(self, title, body="", tags=None):
        resp = requests.post(f"{self.base}/api/v1/posts", headers=self.headers,
                             json={"title": title, "body": body, "tags": tags or []})
        check(resp, "creating a post")
        return resp.json()

    def list_posts(self, mine=False, tag=None):
        params = {"mine": mine}
        if tag:
            params["tag"] = tag
        resp = requests.get(f"{self.base}/api/v1/posts", headers=self.headers, params=params)
        check(resp, "listing posts")
        return resp.json()

    # TODO (Mini Project 1): get_post, update_post, delete_post
    def get_post(self, id=0, tag=None):
        params = {"id": id}
        resp = requests.get(f"{self.base}/api/v1/posts/{id}", headers=self.headers, params=params)
        check(resp, f"post {id}")
        return resp.json()

    def update_post(self, title, body="", tags=None, id=0, mine=False):
        params = {"mine": mine}
        if tags:
            params['tags'] = tags
        resp = requests.patch(f"{self.base}/api/v1/posts/{id}", headers=self.headers, params=params,
                              json={"title": title, "body": body, "tags": tags or []})
        check(resp, f"post {id}")
        return resp.json()

    def delete_post(self, id=0, mine=False):
        params = {"mine": mine}
        resp = requests.delete(f"{self.base}/api/v1/posts/{id}", headers=self.headers, params=params)
        check(resp, f"post {id}")
        return {"message": "post deleted successfully"}


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("PRACTICE_API_TOKEN is not set - see 'Set your token' in Week 2.")
    client = PracticeHubClient(BASE, TOKEN)

    try:
        everyone = client.list_posts()
        print(f"posts on the hub: {len(everyone)}")

        #new_post = client.create_post("Week 3 lab", body="My first created post.")
        #print(f"created post {new_post['id']}: {new_post['title']}")
        #print(f"posts that are mine: {len(client.list_posts(mine=True))}")

        post_id = 1
        post_by_id = client.get_post(id=post_id)
        print(post_by_id)

        # post_id = 8
        # title = "Week 3 Lab"
        # body = "Updating my first post."
        # updated_post = client.update_post(title, body=body, id = post_id, mine=True)
        # print(updated_post)

        post_id = 5
        delete_post = client.delete_post(id=post_id, mine=True)
        print(delete_post)

    except AuthError as exc:
        report(exc)
    except ForbiddenError as exc:
        report(exc)
    except NotFoundError as exc:
        report(exc)
    except ValidationError as exc:
        report(exc)
    except ApiError as exc:
        report(exc)
    except requests.exceptions.RequestException as exc:
        print(f"[network] Could not reach {BASE}: {exc}")