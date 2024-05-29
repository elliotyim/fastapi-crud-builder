from app.domain.entity import Post, User
from app.main import app
from starlette.testclient import TestClient


class TestPostRequest:
    """
    URL: /posts
    """

    def test_creating_post(self, test_client: TestClient, dummy_users: list[User]):
        response = test_client.post(
            url=app.url_path_for("create_post"),
            json={
                "title": "test_title",
                "content": "test_content",
                "author_id": dummy_users[0].id,
            },
        )

        assert response.status_code == 201

        result = response.json()
        assert result["title"] == "test_title"
        assert result["content"] == "test_content"

        assert "author" in result
        assert result["author"]["id"] == dummy_users[0].id
        assert result["author"]["name"] == dummy_users[0].name

    def test_retrieving_post(
        self, test_client: TestClient, dummy_users: list[User], dummy_posts: list[Post]
    ):
        response = test_client.get(
            url=app.url_path_for("get_post", id=dummy_posts[0].id)
        )

        assert response.status_code == 200

        result = response.json()
        assert result["id"] == dummy_posts[0].id
        assert result["title"] == dummy_posts[0].title
        assert result["content"] == dummy_posts[0].content

        assert "author" in result
        assert result["author"]["id"] == dummy_users[0].id
        assert result["author"]["name"] == dummy_users[0].name

    def test_updating_post(self, test_client: TestClient, dummy_posts: list[Post]):
        response = test_client.patch(
            url=app.url_path_for("patch_post", id=dummy_posts[0].id),
            json={"title": "changed_title"},
        )

        assert response.status_code == 200

        result = response.json()
        assert result["id"] == dummy_posts[0].id
        assert result["title"] == "changed_title"
        assert result["content"] == dummy_posts[0].content

    def test_updating_post_all(self, test_client: TestClient, dummy_posts: list[Post]):
        response = test_client.put(
            url=app.url_path_for("put_post", id=dummy_posts[0].id),
            json={"title": "changed_title"},
        )

        assert response.status_code == 200

        result = response.json()
        assert result["id"] == dummy_posts[0].id
        assert result["title"] == "changed_title"
        assert result["content"] is None

    def test_deleting_post(self, test_client: TestClient, dummy_posts: list[Post]):
        response = test_client.delete(
            url=app.url_path_for("delete_post", id=dummy_posts[0].id)
        )

        assert response.status_code == 204
