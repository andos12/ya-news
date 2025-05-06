import pytest

from news.models import News, Comment

from django.test.client import Client
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from datetime import datetime, timedelta


@pytest.fixture
def anonymous(django_user_model):
    return django_user_model.objects.create(username='Анонимный пользователь')

@pytest.fixture
def news(anonymous):
    news = News.objects.create(
        title='Заголовок',
        text='Просто текст.',
    )
    return news


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Просто текст.'
    )
    return comment


@pytest.fixture
def pk_for_args(comment):
    return (comment.pk,)


@pytest.fixture
def news_count():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title='Заголовок',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def news_comments(author):
    now = timezone.now()
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    comments = []
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            text=f'Tекст {index}',
            created=now + timedelta(days=index),
            author=author
        )
    comments.append(comment)
    return {
        'detail': reverse('news:detail', args=(news.pk,))
    }


@pytest.fixture
def form_data():
    return {'news': 'Заголовок',
            'text': 'Текст'}

