import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship


Base = declarative_base()

tags_posts_table = sqlalchemy.Table('tags_posts', Base.metadata,
    sqlalchemy.Column('post_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('posts.id')),
    sqlalchemy.Column('tag_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('tags.id')),
)


class User(Base):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)

    posts = relationship("Post", back_populates="user")


class Tag(Base):
    __tablename__ = 'tags'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)

    posts = relationship("Post", secondary=tags_posts_table, back_populates="tags")


class Post(Base):
    __tablename__ = 'posts'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    title = sqlalchemy.Column(sqlalchemy.String(16))
    text = sqlalchemy.Column(sqlalchemy.Text)
    is_publised = sqlalchemy.Column(sqlalchemy.Boolean)
    user = relationship("User", back_populates="posts", lazy='joined')
    tags = relationship("Tag", secondary=tags_posts_table, back_populates="posts")




# echo - режим дебага
engine = sqlalchemy.create_engine('sqlite:///blog.db', echo=False)
Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()



# создание 1-го поста
# post_info = {'id': 1, 'title': 'foo post'}
# session.add(Post(**post_info))
# session.commit()


# Добавляем данные
# Пользователи
user = User(username='petya')
session.add(user)
session.commit()
# Посты
post = Post(title='First post', user_id=user.id)
session.add(post)
session.commit()

# Явное указание ключей
p = session.query(Post).join(User, Post.user_id == User.id).first()
print(p.user.username)  # john

# Неявное указание ключей
p = session.query(Post).join(User).first()
print(p.user.username)  # john

# Добавляем тэг
tag = Tag(name='python')
session.add(tag)

p = session.query(Tag).join(User, Tag.id == User.id).first()
print(p) # <__main__.Tag object at 0x103471630>

p = session.query(Tag, User).join(User, Tag.id == User.id).first()
print(p)  # (<__main__.Tag object at 0x1036aea58>, <__main__.User object at 0x1036aec50>)

# Добавляем еще 1 тэг и 1 пользователя
session.add(User(username='vasya'))
session.add(Tag(name='java'))
session.commit()

# Количество
p = session.query(Tag, User).count()
print(p)  # 4

# Добавим еще пост не john
post = Post(title='New', user_id=2)
# Тэг python
post.tags.append(tag)
session.add(post)
session.commit()

# FILETR по FK
# Посты пользователя john
posts = session.query(Post).join(User).filter(User.username == 'petya').all()
print('petya posts:', posts)


# Без join
posts = session.query(Post, User).filter(User.username == 'petya').all()
print(posts)

# Filter m2m
tag_id = session.query(Tag.id).filter(Tag.name=='python').scalar()
posts = session.query(Post).join(tags_posts_table).filter(
    tags_posts_table.c.tag_id == tag_id,
)
