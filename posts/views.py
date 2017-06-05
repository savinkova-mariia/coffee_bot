from django.shortcuts import render, get_object_or_404
from django.db.models import Max
from .models import Table


def index(request):

    tables = Table.objects.annotate(
        max_created=Max("posts__created")
    ).order_by("-max_created")
    return render(request, "index.html", {
        "tables": tables,
    })


def tables(request, slug):

    order = get_object_or_404(Table, slug=slug)

    return render(request, "tables.html", {
        "tables": order,
        "posts": order.posts.order_by("-created"),
    })
