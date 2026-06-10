import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.utils.markdown import render_markdown
from features.jobs.forms import JobDescriptionForm
from features.jobs.validators import MAX_DESCRIPTION_LENGTH


class RenderMarkdownSanitizationTests(TestCase):
    def test_strips_script_tags(self):
        html = render_markdown("Hello <script>alert(1)</script> world")
        self.assertNotIn("<script", html)
        self.assertNotIn("alert(1)", html)

    def test_strips_event_handlers(self):
        html = render_markdown('<img src="x" onerror="alert(1)">')
        self.assertNotIn("onerror", html)

    def test_strips_javascript_links(self):
        html = render_markdown("[click](javascript:alert(1))")
        self.assertNotIn("javascript:", html)

    def test_strips_iframes(self):
        html = render_markdown('<iframe src="https://evil.example"></iframe>')
        self.assertNotIn("<iframe", html)

    def test_preserves_headings_and_emphasis(self):
        html = render_markdown("# Title\n\nSome **bold** text")
        self.assertIn("<h1>Title</h1>", html)
        self.assertIn("<strong>bold</strong>", html)

    def test_preserves_links_with_rel(self):
        html = render_markdown("[site](https://example.com)")
        self.assertIn('href="https://example.com"', html)
        self.assertIn("noopener", html)

    def test_preserves_fenced_code_and_tables(self):
        html = render_markdown(
            "```\nprint('hi')\n```\n\n| a | b |\n| - | - |\n| 1 | 2 |"
        )
        self.assertIn("<code>", html)
        self.assertIn("<table>", html)


class JobDescriptionFormValidationTests(TestCase):
    def make_form(self, description, title="Engineer"):
        return JobDescriptionForm(
            data={"title": title, "description": description}
        )

    def test_accepts_normal_markdown(self):
        form = self.make_form("# Role\n\nWe are hiring a **great** engineer.")
        self.assertTrue(form.is_valid(), form.errors)

    def test_rejects_script_tag(self):
        form = self.make_form("Hi <script>alert(1)</script>")
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)

    def test_rejects_event_handler(self):
        form = self.make_form('<img src="x" onerror="alert(1)">')
        self.assertFalse(form.is_valid())

    def test_rejects_javascript_uri(self):
        form = self.make_form("[click](javascript:alert(1))")
        self.assertFalse(form.is_valid())

    def test_rejects_overlong_description(self):
        form = self.make_form("a" * (MAX_DESCRIPTION_LENGTH + 1))
        self.assertFalse(form.is_valid())

    def test_rejects_whitespace_only_description(self):
        form = self.make_form("   \n\t  ")
        self.assertFalse(form.is_valid())

    def test_rejects_whitespace_only_title(self):
        form = self.make_form("Valid description", title="   ")
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)


class AdminJobPreviewEndpointTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="pass1234"
        )
        self.client.force_login(user)
        self.url = reverse("admin_panel:job_preview")

    def post_markdown(self, markdown_text):
        return self.client.post(
            self.url,
            data=json.dumps({"markdown": markdown_text}),
            content_type="application/json",
        )

    def test_renders_sanitized_html(self):
        response = self.post_markdown("# Hi\n<script>alert(1)</script>")
        self.assertEqual(response.status_code, 200)
        html = response.json()["html"]
        self.assertIn("<h1>Hi</h1>", html)
        self.assertNotIn("<script", html)

    def test_rejects_oversized_payload(self):
        response = self.post_markdown("a" * (MAX_DESCRIPTION_LENGTH + 1))
        self.assertEqual(response.status_code, 400)
