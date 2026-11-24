from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.cache import cache
from azblog.models import Post

class SecurityAuditTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user1 = User.objects.create_user(username='author1', password='password123')
        self.user2 = User.objects.create_user(username='author2', password='password123')
        self.admin = User.objects.create_superuser(username='admin_user', password='password123')

        self.published_post = Post.objects.create(
            title='Public Post',
            slug='public-post',
            excerpt='Public excerpt',
            content='Public content',
            status='published',
            author=self.user1
        )
        self.draft_post = Post.objects.create(
            title='Draft Post User1',
            slug='draft-post-user1',
            excerpt='Draft excerpt',
            content='Secret Draft Content',
            status='draft',
            author=self.user1
        )

    def test_idor_anonymous_cannot_access_draft(self):
        """Anonymous user should receive 404 when trying to view a draft post."""
        response = self.client.get(f'/post/{self.draft_post.pk}')
        self.assertEqual(response.status_code, 404)

    def test_idor_other_user_cannot_access_draft(self):
        """Another non-author user should receive 404 when trying to view User1's draft."""
        self.client.login(username='author2', password='password123')
        response = self.client.get(f'/post/{self.draft_post.pk}')
        self.assertEqual(response.status_code, 404)

    def test_author_can_access_own_draft(self):
        """Author should be able to view their own draft."""
        self.client.login(username='author1', password='password123')
        response = self.client.get(f'/post/{self.draft_post.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Secret Draft Content')

    def test_admin_can_access_draft(self):
        """Staff/Admin can view draft posts for moderation."""
        self.client.login(username='admin_user', password='password123')
        response = self.client.get(f'/post/{self.draft_post.pk}')
        self.assertEqual(response.status_code, 200)

    def test_public_post_accessible_by_all(self):
        """Public post is accessible to anonymous users."""
        response = self.client.get(f'/post/{self.published_post.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Public content')

    def test_login_rate_limiting(self):
        """Repeated failed login POST attempts should be rate-limited (HTTP 429)."""
        cache.clear()
        for i in range(5):
            res = self.client.post('/admin/login/', {'username': 'test', 'password': 'wrong'})
            self.assertIn(res.status_code, [200, 302])

        # 6th attempt should be blocked with 429
        blocked_res = self.client.post('/admin/login/', {'username': 'test', 'password': 'wrong'})
        self.assertEqual(blocked_res.status_code, 429)
        self.assertIn(b"Too many login attempts", blocked_res.content)
