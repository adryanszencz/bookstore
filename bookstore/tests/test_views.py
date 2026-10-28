import hashlib
import hmac
import os
from unittest import mock

from django.test import TestCase
from django.urls import reverse


class HelloWorldTest(TestCase):
    def test_pagina_hello(self):
        response = self.client.get(reverse("hello_world"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hello_world.html")
        self.assertContains(response, "Hello World")


@mock.patch("bookstore.views.git.Repo")
class UpdateServerTest(TestCase):
    def test_get_nao_e_permitido(self, repo):
        response = self.client.get(reverse("update_server"))

        self.assertEqual(response.status_code, 405)
        repo.assert_not_called()

    def test_post_faz_git_pull(self, repo):
        response = self.client.post(reverse("update_server"))

        self.assertEqual(response.status_code, 200)
        repo.return_value.remotes.origin.pull.assert_called_once()

    @mock.patch.dict(os.environ, {"GITHUB_WEBHOOK_SECRET": "segredo-de-teste"})
    def test_assinatura_invalida_da_403(self, repo):
        response = self.client.post(
            reverse("update_server"),
            data=b"{}",
            content_type="application/json",
            HTTP_X_HUB_SIGNATURE_256="sha256=errada",
        )

        self.assertEqual(response.status_code, 403)
        repo.assert_not_called()

    @mock.patch.dict(os.environ, {"GITHUB_WEBHOOK_SECRET": "segredo-de-teste"})
    def test_assinatura_valida_faz_pull(self, repo):
        body = b'{"ref": "refs/heads/main"}'
        assinatura = "sha256=" + hmac.new(b"segredo-de-teste", body, hashlib.sha256).hexdigest()

        response = self.client.post(
            reverse("update_server"), data=body, content_type="application/json", HTTP_X_HUB_SIGNATURE_256=assinatura
        )

        self.assertEqual(response.status_code, 200)
        repo.return_value.remotes.origin.pull.assert_called_once()
