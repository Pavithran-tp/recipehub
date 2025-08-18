from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from .models import Collection
from recipes.models import Recipe 


class CollectionViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='testpassword123')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword123')

        self.collection1 = Collection.objects.create(user=self.user1, name='My First Collection')
        self.collection2 = Collection.objects.create(user=self.user1, name='My Second Collection')

        self.collection3 = Collection.objects.create(user=self.user2, name='User2 Collection')

        self.list_url = reverse('collections:collection-list')
        self.detail_url_1 = reverse('collections:collection-detail', kwargs={'collection_id': self.collection1.pk})
        self.detail_url_2 = reverse('collections:collection-detail', kwargs={'collection_id': self.collection2.pk})
        self.detail_url_3 = reverse('collections:collection-detail', kwargs={'collection_id': self.collection3.pk})

    def test_collection_list_view_redirects_unauthenticated_user(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/collections/')

    def test_collection_list_view_loads_for_authenticated_user(self):
        self.client.login(username='testuser1', password='testpassword123')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'collections/collection_list.html')
        self.assertContains(response, self.collection1.name)
        self.assertContains(response, self.collection2.name)

    def test_collection_list_view_only_shows_current_users_collections(self):
        self.client.login(username='testuser1', password='testpassword123')
        response = self.client.get(self.list_url)
        retrieved_collections = list(response.context['collections'])
        expected_collections = [self.collection1, self.collection2]
        self.assertCountEqual(retrieved_collections, expected_collections)
        self.assertNotContains(response, self.collection3.name)

    def test_collection_detail_view_redirects_unauthenticated_user(self):
        response = self.client.get(self.detail_url_1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/collections/collection/{self.collection1.pk}/')

    def test_collection_detail_view_loads_for_authenticated_user(self):
        self.client.login(username='testuser1', password='testpassword123')
        response = self.client.get(self.detail_url_1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'collections/collection_detail.html')
        self.assertContains(response, self.collection1.name)

    def test_collection_detail_view_denies_access_to_other_users_collections(self):
        self.client.login(username='testuser1', password='testpassword123')
        response = self.client.get(self.detail_url_3)
        self.assertEqual(response.status_code, 404)
