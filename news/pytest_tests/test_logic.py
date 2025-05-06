from django.urls import reverse

from news.models import Comment
from news.forms import BAD_WORDS, WARNING

from http import HTTPStatus


def test_anonymous_user_cant_create_comment(client, news, form_data):
    url = reverse('news:detail', args=(news.pk,))
    response = client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(author_client, author, news, form_data):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.news == news
    assert comment.author == author
    assert comment.text == form_data['text']


def test_user_cant_use_bad_words(author_client, news):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.post(url, data=bad_words_data)
    assert 'form' in response.context
    form = response.context['form']
    assert WARNING in form.errors['text']
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, comment, form_data):
    url = reverse('news:delete', args=(comment.pk,))
    response = author_client.post(url, form_data)
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(author_client, comment, form_data):
    url = reverse('news:edit', args=(comment.pk,))
    new_text = form_data['text']
    response = author_client.post(url, form_data)
    comment.refresh_from_db()
    assert comment.text == new_text


def test_user_cant_edit_comment_of_another_user(
        not_author_client, comment, form_data):
    url = reverse('news:edit', args=(comment.pk,))
    current_text = comment.text
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == current_text


def test_user_cant_delete_comment_of_another_user(
        not_author_client, comment, form_data):
    url = reverse('news:delete', args=(comment.pk,))
    comment_count = Comment.objects.count()
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment_count == 1