from django.shortcuts import render, redirect

from . import util
import markdown2
from random import randint


def index(request):
    content = {
        "index_title" : "All Pages",
        "entries": util.list_entries()
        }

    return render(request, "encyclopedia/index.html", content)

def wiki(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return render(request, "encyclopedia/apology.html", {"message":"No entry with the given title!"})

    entry_content = markdown2.markdown(entry)

    content = {
        "title" : title,
        "page_content" : entry_content
    }

    return render(request, "encyclopedia/wiki.html", content)

def search(request):
    search_text = request.POST["q"]

    result_pages = []

    for page in util.list_entries():
        if search_text.lower() == page.lower():
            return redirect('wiki', title=search_text)
        if search_text.lower() in page.lower():
            result_pages.append(page)

    print(result_pages)

    if result_pages:
        content = {
            "title": "Search results",
            "results": result_pages
        }
        return render(request, "encyclopedia/search.html", content)

    return render(request, "encyclopedia/apology.html", {"message":"No entry with the given title!"})

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        text = request.POST["text"]

        for entry in util.list_entries():
            if entry.lower() == title.lower():
                return render(request, "encyclopedia/apology.html", {"message": "Entry title already exists!"})

        util.save_entry(title, text)
        return redirect('wiki', title=title)

    else:
        return render(request, "encyclopedia/create.html", {})

def edit(request):
    title = request.POST["title"]
    text = util.get_entry(title)

    content = {
        "title": title,
        "text": text
    }
    return render(request, "encyclopedia/edit.html", content)


def save(request):
    title = request.POST["title"]
    text = request.POST["text"]
    util.save_entry(title, text)
    return redirect('wiki', title=title)

def random(request):
    entry_list = util.list_entries()
    page_index_to_show = randint(0, len(entry_list) - 1)
    return redirect('wiki', title=entry_list[page_index_to_show])
