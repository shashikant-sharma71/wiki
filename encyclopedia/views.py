import markdown2
import random
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util

# Helper: Convert Markdown to HTML
def convert_md_to_html(title):
    content = util.get_entry(title)
    if content is None:
        return None
    else:
        return markdown2.markdown(content)

# Index Page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Entry Page
def entry(request, title):
    html = convert_md_to_html(title)
    if html is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html
    })

# Search Page
def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    if query in entries:
        return HttpResponseRedirect(reverse("entry", args=[query]))

    results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query
    })

# Create New Page
def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message": "An entry with this title already exists."
            })
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    return render(request, "encyclopedia/create.html")

# Edit Page
def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

# Random Page
def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return HttpResponseRedirect(reverse("entry", args=[title]))