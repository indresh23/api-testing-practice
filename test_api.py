"""
API tests for:
  1. JSONPlaceholder (https://jsonplaceholder.typicode.com) - a public practice API
  2. A bearer token endpoint on httpbin.org

Run all tests:  pytest -v
"""
import pytest
import requests

BASE = "https://jsonplaceholder.typicode.com"
BEARER_URL = "https://httpbin.org/bearer"
TIMEOUT = 10  # seconds


# Fixture: reusable setup, gives the base URL to any test that asks for it
@pytest.fixture
def base_url():
    return BASE


# TC01 - GET a single post (positive test)
def test_get_single_post(base_url):
    r = requests.get(f"{base_url}/posts/1", timeout=TIMEOUT)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == 1
    for field in ("userId", "title", "body"):
        assert field in data


# TC02 - GET all posts, check count and response time
def test_get_all_posts(base_url):
    r = requests.get(f"{base_url}/posts", timeout=TIMEOUT)
    assert r.status_code == 200
    assert len(r.json()) == 100
    assert r.elapsed.total_seconds() < 5


# TC03 - Parameterization: valid ids give 200, invalid ids give 404
@pytest.mark.parametrize("post_id, expected_status", [
    (1, 200),
    (50, 200),
    (100, 200),
    (0, 404),
    (101, 404),
    (9999, 404),
])
def test_post_status_by_id(base_url, post_id, expected_status):
    r = requests.get(f"{base_url}/posts/{post_id}", timeout=TIMEOUT)
    assert r.status_code == expected_status


# TC04 - Query parameter: filter posts by userId
def test_filter_posts_by_user(base_url):
    r = requests.get(f"{base_url}/posts", params={"userId": 1}, timeout=TIMEOUT)
    assert r.status_code == 200
    posts = r.json()
    assert len(posts) == 10
    assert all(post["userId"] == 1 for post in posts)


# TC05 - POST creates a new post (expects 201 Created)
def test_create_post(base_url):
    body = {"title": "hello", "body": "my first post", "userId": 1}
    r = requests.post(f"{base_url}/posts", json=body, timeout=TIMEOUT)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "hello"
    assert data["userId"] == 1
    assert "id" in data


# TC06 - PUT replaces a post
def test_update_post_put(base_url):
    body = {"id": 1, "title": "updated title", "body": "updated body", "userId": 1}
    r = requests.put(f"{base_url}/posts/1", json=body, timeout=TIMEOUT)
    assert r.status_code == 200
    assert r.json()["title"] == "updated title"


# TC07 - DELETE removes a post
def test_delete_post(base_url):
    r = requests.delete(f"{base_url}/posts/1", timeout=TIMEOUT)
    assert r.status_code == 200


# TC08 - Check response header and data types
def test_headers_and_data_types(base_url):
    r = requests.get(f"{base_url}/posts/1", timeout=TIMEOUT)
    assert "application/json" in r.headers["Content-Type"]
    data = r.json()
    assert isinstance(data["id"], int)
    assert isinstance(data["title"], str)


# TC09 - Bearer token: valid token gives 200
def test_bearer_with_token():
    headers = {"Authorization": "Bearer abc123"}
    r = requests.get(BEARER_URL, headers=headers, timeout=TIMEOUT)
    assert r.status_code == 200
    assert r.json()["authenticated"] is True


# TC10 - Bearer token: missing token gives 401 (negative test)
def test_bearer_without_token():
    r = requests.get(BEARER_URL, timeout=TIMEOUT)
    assert r.status_code == 401
