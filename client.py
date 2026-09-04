# INF601 - Advanced Programming in Python
# Gabriel Itegbe
# Mini Project 1
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
    def get_post(self,id=0,tag=None):
        params = {"id": id}
        resp = requests.get(f"{self.base}/api/v1/posts/{id}", headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json()
    def update_post(self, title, body="", tags=None, id = 0, mine = False):
        params = {"mine" : mine}
        if tags:
            params['tags'] = tags
        resp = requests.patch(f"{self.base}/api/v1/posts/{id}", headers=self.headers, params=params,json={"title": title, "body": body, "tags": tags or []})
        resp.raise_for_status()
        return resp.json()
    def delete_post(self, id = 0, mine = False):
        params = {"mine": mine}
        resp = requests.delete(f"{self.base}/api/v1/posts/{id}", headers=self.headers, params=params)
        resp.raise_for_status()
        return {"message" : "post deleted successfully"}
if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("PRACTICE_API_TOKEN is not set - see 'Set your token' in Week 2.")
    client = PracticeHubClient(BASE, TOKEN)
    everyone = client.list_posts()
    print(f"posts on the hub: {len(everyone)}")
    #new_post = client.create_post("Week 3 lab", body="My first created post.")
    #print(f"created post {new_post['id']}: {new_post['title']}")
    #print(f"posts that are mine: {len(client.list_posts(mine=True))}")
    post_id=1
    post_by_id=client.get_post(id=post_id)
    print(post_by_id)

    # post_id = 8
    # title = "Week 3 Lab"
    # body = "Updating my first post."
    # updated_post = client.update_post(title, body=body, id = post_id, mine=True)
    # print(updated_post)
    post_id = 5
    delete_post = client.delete_post(id=post_id, mine=True)
    print(delete_post)