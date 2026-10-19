# API Testing Practice

A beginner API testing project. I tested a public practice API using **Postman** and then automated the checks in **Python** with **requests** and **pytest**.

## What I tested
- **JSONPlaceholder** (`https://jsonplaceholder.typicode.com`): GET, POST, PUT and DELETE requests
- **httpbin.org** (`/bearer`): a bearer token endpoint

## Tools
Postman, Python, requests, pytest

## Test cases

| ID | Scenario | Method + Endpoint | Expected result |
|---|---|---|---|
| TC01 | Get a single post | GET /posts/1 | 200, id is 1, fields present |
| TC02 | Get all posts | GET /posts | 200, 100 posts, response under 5 sec |
| TC03 | Valid and invalid post ids (parametrized, 6 cases) | GET /posts/{id} | 200 for 1, 50, 100; 404 for 0, 101, 9999 |
| TC04 | Filter by query parameter | GET /posts?userId=1 | 200, 10 posts, all with userId 1 |
| TC05 | Create a post | POST /posts | 201, title and userId match, id present |
| TC06 | Update a post | PUT /posts/1 | 200, title updated |
| TC07 | Delete a post | DELETE /posts/1 | 200 |
| TC08 | Header and data types | GET /posts/1 | Content-Type is JSON, id is int, title is str |
| TC09 | Valid bearer token | GET /bearer with token | 200, authenticated is true |
| TC10 | Missing bearer token (negative) | GET /bearer without token | 401 |

TC03 runs 6 times because of parameterization, so pytest shows 15 test runs for 10 test cases.

## How to run

```
pip install -r requirements.txt
pytest -v
```

## Concepts used
- Status code checks (200, 201, 401, 404)
- Response body, header and data type checks
- Positive and negative testing
- Path and query parameters
- `@pytest.mark.parametrize` for multiple inputs
- `@pytest.fixture` for reusable setup
- Bearer token authentication

## Notes
- JSONPlaceholder is a fake API. POST, PUT and DELETE return a success response, but the data is not really saved.
- This is a self-learning project.
