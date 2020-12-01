from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from wagtail.core.models import Page, Site as WagtailSite
from wagtail.tests.utils import WagtailTestUtils

from django_comments_xtd.models import XtdComment


class TestUpdate(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

        page = Page(title="Test Page")

        root = WagtailSite.objects.get().root_page
        root.add_child(instance=page)

        self.comment = XtdComment.objects.create(
            content_type=ContentType.objects.get_for_model(Page),
            object_pk=page.pk,
            site=Site.objects.get_current(),
        )

    def test_unpublish(self):
        response = self.client.get(
            reverse(
                "wagtail_comments_xtd_publication",
                kwargs={
                    "page_pk": self.comment.object_pk,
                    "comment_pk": self.comment.pk,
                    "action": "unpublish",
                },
            ),
            follow=True,
        )

        self.comment.refresh_from_db()

        self.assertEqual(200, response.status_code)
        self.assertFalse(self.comment.is_public)

    def test_publish(self):

        self.comment.is_public = False

        response = self.client.get(
            reverse(
                "wagtail_comments_xtd_publication",
                kwargs={
                    "page_pk": self.comment.object_pk,
                    "comment_pk": self.comment.pk,
                    "action": "publish",
                },
            ),
            follow=True,
        )

        self.comment.refresh_from_db()

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.comment.is_public)

    def test_hide(self):
        response = self.client.get(
            reverse(
                "wagtail_comments_xtd_publication",
                kwargs={
                    "page_pk": self.comment.object_pk,
                    "comment_pk": self.comment.pk,
                    "action": "hide",
                },
            ),
            follow=True,
        )

        self.comment.refresh_from_db()

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.comment.is_removed)

    def test_show(self):
        self.comment.is_removed = True

        response = self.client.get(
            reverse(
                "wagtail_comments_xtd_publication",
                kwargs={
                    "page_pk": self.comment.object_pk,
                    "comment_pk": self.comment.pk,
                    "action": "show",
                },
            ),
            follow=True,
        )

        self.comment.refresh_from_db()

        self.assertEqual(200, response.status_code)
        self.assertFalse(self.comment.is_removed)

class TestUpdateThreadedComment(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

        page = Page(title="Test Page")

        root = WagtailSite.objects.get().root_page
        root.add_child(instance=page)

        self.comment_parent = XtdComment.objects.create(
            content_type=ContentType.objects.get_for_model(Page),
            object_pk=page.pk,
            site=Site.objects.get_current(),
        )

        self.comment_child_1 = XtdComment.objects.create(
            content_type=ContentType.objects.get_for_model(Page),
            object_pk=page.pk,
            site=Site.objects.get_current(),
            parent_id=self.comment_parent.pk,
        )

        self.comment_child_2 = XtdComment.objects.create(
            content_type=ContentType.objects.get_for_model(Page),
            object_pk=page.pk,
            site=Site.objects.get_current(),
            parent_id=self.comment_parent.pk,
        )

    def test_unpublish(self):
        response = self.client.get(
            reverse(
                "wagtail_comments_xtd_publication",
                kwargs={
                    "page_pk": self.comment_parent.object_pk,
                    "comment_pk": self.comment_parent.pk,
                    "action": "unpublish",
                },
            ),
            follow=True,
        )

        self.comment_parent.refresh_from_db()
        self.comment_child_1.refresh_from_db()
        self.comment_child_2.refresh_from_db()

        self.assertEqual(200, response.status_code)
        self.assertFalse(self.comment_parent.is_public)
        self.assertFalse(self.comment_child_1.is_public)
        self.assertFalse(self.comment_child_2.is_public)

    def test_publish(self):

        self.comment_parent.is_public = False
        self.comment_child_1.is_public = False
        self.comment_child_2.is_public = False

        response = self.client.get(
            reverse(
                "wagtail_comments_xtd_publication",
                kwargs={
                    "page_pk": self.comment_parent.object_pk,
                    "comment_pk": self.comment_parent.pk,
                    "action": "publish",
                },
            ),
            follow=True,
        )

        self.comment_parent.refresh_from_db()
        self.comment_child_1.refresh_from_db()
        self.comment_child_2.refresh_from_db()

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.comment_parent.is_public)
        self.assertTrue(self.comment_child_1.is_public)
        self.assertTrue(self.comment_child_2.is_public)

    def test_hide(self):
        response = self.client.get(
            reverse(
                "wagtail_comments_xtd_publication",
                kwargs={
                    "page_pk": self.comment_parent.object_pk,
                    "comment_pk": self.comment_parent.pk,
                    "action": "hide",
                },
            ),
            follow=True,
        )

        self.comment_parent.refresh_from_db()
        self.comment_child_1.refresh_from_db()
        self.comment_child_2.refresh_from_db()

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.comment_parent.is_removed)
        self.assertTrue(self.comment_child_1.is_removed)
        self.assertTrue(self.comment_child_2.is_removed)

    def test_show(self):
        self.comment_parent.is_removed = True
        self.comment_child_1.is_removed = True
        self.comment_child_2.is_removed = True

        response = self.client.get(
            reverse(
                "wagtail_comments_xtd_publication",
                kwargs={
                    "page_pk": self.comment_parent.object_pk,
                    "comment_pk": self.comment_parent.pk,
                    "action": "show",
                },
            ),
            follow=True,
        )

        self.comment_parent.refresh_from_db()
        self.comment_child_1.refresh_from_db()
        self.comment_child_2.refresh_from_db()

        self.assertEqual(200, response.status_code)
        self.assertFalse(self.comment_parent.is_removed)
        self.assertFalse(self.comment_child_1.is_removed)
        self.assertFalse(self.comment_child_2.is_removed)
