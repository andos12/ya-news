import pytest

from django.urls import reverse
from django.conf import settings

from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(client, news_count):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert sorted_dates == all_dates


def test_comments_order(client, news_comments):
    url = news_comments['detail']
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert sorted_timestamps == all_timestamps


def test_anonymous_client_has_no_form(client, news_comments):
    url = news_comments['detail']
    response = client.get(url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news_comments):
    url = news_comments['detail']
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
