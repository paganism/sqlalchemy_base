from models import User, Post, Tag
from settings import session


def create_user(name):
    count_users_by_name = session.query(User).filter(User.username==name).count()
    if count_users_by_name > 0:
        return 'User Already Exists'
    user = User(username=name)
    session.add(user)
    session.commit()
    return f'Successfully Added user {name}'


def create_posts(posts_list, userid):
    for post in posts_list:
        post_to_insert = Post(title=post, user_id=userid)
        session.add(post_to_insert)
        session.commit()
    return f'Successfully Added posts {", ".join(posts_list)}'


def get_user_object(name):
    return session.query(User).filter(User.username==name).first()


def get_post_object(title):
    return session.query(Post).filter(Post.title==title).first()


def get_tag_object(name):
    return session.query(Tag).filter(Tag.name==name).first()

def get_posts_by_user(username):
    return session.query(Post).join(User).filter(User.username == username).all()

def create_tag(tag):
    tag_to_insert = Tag(name=tag)
    session.add(tag_to_insert)
    session.commit()
    return f'Successfully Added tag {tag}'


def create_tag_post(tag, post):
    """Function creates combination tag and post in db and checks existance of tag"""
    # get tag
    tag_object = get_tag_object(tag)

    if not tag_object:
        tag_to_insert = Tag(name=tag)
        session.add(tag_to_insert)

        # get post
        post_object = get_post_object(post)

        if post_object:
            tag_to_insert.posts.append(post_object)
            session.commit()
            return f'Successfully Added tag {tag} to post {post}'
    
    return f'Incorrect combination'
