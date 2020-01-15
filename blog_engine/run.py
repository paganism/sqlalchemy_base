from models import User, Post, Tag, tags_posts_table
from settings import session
from  logic import create_user, create_posts, get_user_object, create_tag_post, get_posts_by_user


if __name__ == "__main__":

    users_list = ['petya', 'vasya', 'john smith', 'masha', 'dasha']
    posts = ['The last day of humanity', 'Solar Echoes', 'Eternity in the Abyss', 'Endless space', 'Entropy', 'Aurora', 'Far Centaurus']
    
    for user in users_list:
        print(create_user(user))

    user_obj = get_user_object('petya')
    if user_obj:
        print(create_posts(posts, user_obj.id))
      
    tags = ['sun', 'space', 'solar_system']

    for tag in tags:
        print(create_tag_post(tag, 'Solar Echoes'))


    # Direct keys
    p = session.query(Post).join(User, Post.user_id == User.id).first()
    print(p.user.username)  

    # Indirect keys
    p = session.query(Post).join(User).first()
    print(p.user.username) 


    p = session.query(Tag).join(User, Tag.id == User.id).first()
    print(p)

    p = session.query(Tag, User).join(User, Tag.id == User.id).first()
    print(p)

    # Counting
    p = session.query(Tag, User).count()
    print(p)


    # FILETR по FK
    # petya posts (join function)
    print(get_posts_by_user('petya'))
    
    # M2M filtering
    tag_id = session.query(Tag.id).filter(Tag.name=='space').scalar()
    print(tag_id)
    posts = session.query(Post).join(tags_posts_table).filter(
        tags_posts_table.c.tag_id == tag_id,
    )
    for post in posts:
        print(post)