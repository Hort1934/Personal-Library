from .models import Author, book
from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseNotFound
from .forms import AuthorForm


def all_authors(request):
    user = request.user
    if user and user.is_authenticated and user.get_role_name() == 'librarian':
        form = AuthorForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            author = form.save()
            messages.success(request, f"Author {author.name} {author.surname} created.")
            return redirect("all_authors")
        authors = Author.objects.all()
        return render(request, 'author/all_authors.html', {'authors': authors, 'form': form})
    else:
        return HttpResponseNotFound("page not found")



def create_author(request):
    user = request.user
    if user and user.is_authenticated and user.get_role_name() == 'librarian':
        form = AuthorForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            author = form.save()
            messages.success(request, f"Author {author.name} {author.surname} created.")
            return redirect("all_authors")
        return render(request, 'author/create_author.html', {'form': form})
    else:
        return HttpResponseNotFound("page not found")

        
def delete_author(request, id):
    author = get_object_or_404(Author, id=id)
    if author:
        if author.books.count() > 0:
            messages.error(request, "Cannot delete author with books.")
        else:
            author.delete()
            messages.success(request, f"Author {author.name} {author.surname} deleted." )
        return redirect("all_authors")
