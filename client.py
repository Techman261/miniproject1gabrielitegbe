import os
import requests

BASE = "https://practice.fhsucyber.com"
TOKEN = os.environ.get("PRACTICE_API_TOKEN")


class PracticeHubClient:
    def __init__(self, base_url, token):
        self.base = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {token}"}

    def create_post(self, title, body="", tags=None):
        resp = requests.post(f"{self.base}/api/v1/posts", headers=self.headers,
                             json={"title": title, "body": body, "tags": tags or []})
        resp.raise_for_status()
        return resp.json()

    def list_posts(self, mine=False, tag=None):
        params = {"mine": mine}
        if tag:
            params["tag"] = tag
        resp = requests.get(f"{self.base}/api/v1/posts", headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json()

    # TODO (Mini Project 1): get_post, update_post, delete_post


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("PRACTICE_API_TOKEN is not set - see 'Set your token' in Week 2.")

    client = PracticeHubClient(BASE, TOKEN)

    everyone = client.list_posts()
    print(f"posts on the hub: {len(everyone)}")

    new_post = client.create_post("Week 3 lab", body="My first created post.")
    print(f"created post {new_post['id']}: {new_post['title']}")

    print(f"posts that are mine: {len(client.list_posts(mine=True))}")