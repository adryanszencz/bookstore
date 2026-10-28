import hashlib
import hmac
import os
from pathlib import Path

import git
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def _assinatura_valida(request):
    """Confere a assinatura do webhook do GitHub, quando GITHUB_WEBHOOK_SECRET estiver configurado."""
    secret = os.environ.get("GITHUB_WEBHOOK_SECRET")
    if not secret:
        return True
    assinatura = request.headers.get("X-Hub-Signature-256", "")
    esperada = "sha256=" + hmac.new(secret.encode(), request.body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(assinatura, esperada)


@csrf_exempt
@require_POST
def update_server(request):
    """Chamado pelo webhook do GitHub a cada push: faz o git pull do projeto no PythonAnywhere."""
    if not _assinatura_valida(request):
        return HttpResponseForbidden("Assinatura do webhook inválida")

    repo = git.Repo(os.environ.get("PROJECT_PATH", Path(settings.BASE_DIR)))
    repo.remotes.origin.pull()
    return HttpResponse("Código atualizado no PythonAnywhere")


def hello_world(request):
    return render(request, "hello_world.html")
