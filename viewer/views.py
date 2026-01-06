from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect, render
from .models import Article
from services import save


class HomePageView(ListView):
    template_name = "viewer/index.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.filter().order_by("-pub_date")
        return context


def renew(request):
    save.fetch_4pda_articles()
    return redirect("viewer:homepage", permanent=True)
