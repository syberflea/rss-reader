from django.views.generic import ListView

from .models import Article


class HomePageView(ListView):
    template_name = "homepage.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.filter().order_by("-pub_date")[:10]
        return context
