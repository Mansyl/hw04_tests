from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from http import HTTPStatus
from posts.models import Group, Post

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title=('Заголовок тестовой группы'),
            slug='test_slug5',
            description='Тестовое описание'
        )

    def setUp(self):
        self.guest_client = Client()
        # Создаём авторизованный клиент
        self.user = User.objects.create_user(username='Test1')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post(self):
        count_posts = Post.objects.count()
        form_data = {
            'text': 'Данные из формы',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:create'),
            data=form_data,
            follow=True,
        )
        post_1 = Post.objects.get(id=self.group.id)
        author_1 = User.objects.get(username='Test1')
        group_1 = Group.objects.get(title='Заголовок тестовой группы')
        self.assertEqual(Post.objects.count(), count_posts + 1)
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': self.user.username}))
        self.assertTrue(
            Post.objects.filter(
                text='Данные из формы',
                group=self.group.id
            ).exists()
        )
        self.assertEqual(post_1.text, 'Данные из формы')
        self.assertEqual(author_1.username, 'Test1')
        self.assertEqual(group_1.title, 'Заголовок тестовой группы')

    def test_guest_new_post(self):
        # неавторизоанный не может создавать посты
        form_data = {
            'text': 'Пост от неавторизованного пользователя',
            'group': self.group.id
        }
        tasks_count = Post.objects.count()
        self.guest_client.post(
            reverse('posts:create'),
            data=form_data,
            follow=True,
        )
        self.assertNotEqual(Post.objects.count(), tasks_count+1)

    def test_authorized_edit_post(self):
        # авторизованный может редактировать
        form_data = {
            'text': 'Данные из формы',
            'group': self.group.id
        }
        self.authorized_client.post(
            reverse('posts:create'),
            data=form_data,
            follow=True,
        )
        post_2 = Post.objects.get(id=self.group.id)
        self.client.get(f'/Test1/{post_2.id}/edit/')
        form_data = {
            'text': 'Измененный текст',
            'group': self.group.id
        }
        response_edit = self.authorized_client.post(
            reverse('posts:post_edit',
                    kwargs={
                        'post_id': post_2.id
                    }),
            data=form_data,
            follow=True,
        )
        post_2 = Post.objects.get(id=self.group.id)
        self.assertEqual(response_edit.status_code, HTTPStatus.OK)
        self.assertEqual(post_2.text, 'Измененный текст')
