from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):

    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())

    # print(list(posts_map))
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):

    res = client.get("/posts/")
    res.status_code == 401

def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/9999999999999999")
    res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    # print(res.json())
    post = schemas.PostOut(**res.json()[0])

    assert post.Post.id == test_posts[0].id

@pytest.mark.parametrize("title, content, published", [
    ("awesome people_1", "awesome 1_1", True),
    ("awesome people_2", "awesome 2_2", False),
    ("awesome people_3", "awesome 2_2", True)
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title":title,"content": content,"publish": published})
    
    created_post = schemas.Post(**res.json())
    # print(created_post)
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.publish == published
    assert created_post.owner_id == test_user['id']
    

def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post(
        "/posts/", json={"title":"title","content": "content"})
    
    created_post = schemas.Post(**res.json())
    # print(created_post)
    assert res.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.publish == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client, test_posts):
    res = client.post("/posts/", json={"title":"title",
                                       "content": "content"})
    res.status_code == 401