from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from lists.models import Item, List

from lists.forms import ItemForm


def home_page(request):
    return render(request, 'index.html', {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == "POST":
        try:
            item = Item.objects.create(text=request.POST['text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            item.delete()
            error = "You can't have an empty list"
    return render(request, 'list.html', {'list': list_, 'error': error, 'form': ItemForm()})


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list"
        return render(request, 'index.html', {'error': error, 'form': ItemForm()})
    return redirect(list_)
