from django.shortcuts import render , redirect
from .forms import MyCollectionForm, CollectionCategoryForm
from django.contrib import messages
from .models import MyCollection
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def collection_home(request):
    mycollections = MyCollection.objects.filter(user=request.user)

    query = request.GET.get('query')
    if query:
        mycollections = mycollections.filter(name__icontains=query)

    # ページネーション
    paginator = Paginator(mycollections, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'page_obj': page_obj})

@login_required
def collection_register(request):
    if request.method == 'POST':
        form = MyCollectionForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            mycollection = form.save(commit=False)
            mycollection.user = request.user
            mycollection.save()
            messages.success(request, 'コレクションが登録されました。')
            return redirect('mycollection:home')
        else:
            print("フォームエラー:", form.errors)
    else:
        form = MyCollectionForm(user=request.user)

    return render(request, 'collection_register.html', {'form': form})

@login_required
def collection_category_register(request):
    if request.method == 'POST':
        form = CollectionCategoryForm(request.POST)
        if form.is_valid():
            collection_category = form.save(commit=False)
            collection_category.user = request.user
            collection_category.save()
            messages.success(request, 'カテゴリが登録されました。')
            return redirect('mycollection:collection_category_register')
    else:
        form = CollectionCategoryForm()

    return render(request, 'collection_category_register.html', {'form': form})