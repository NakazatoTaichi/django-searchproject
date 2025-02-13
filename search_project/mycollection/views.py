from django.shortcuts import render, get_object_or_404, redirect
from .forms import CollectionSearchForm, MyCollectionForm, CollectionCategoryForm
from django.contrib import messages
from .models import MyCollection
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def collection_home(request):
    mycollections = MyCollection.objects.order_by('-created_at').filter(user=request.user)

    # コレクション名検索
    query = request.GET.get('query')
    if query:
        mycollections = mycollections.filter(name__icontains=query)

    # 絞り込み検索
    form = CollectionSearchForm(user=request.user, data=request.GET)
    if form.is_valid():
        category = form.cleaned_data.get('collection_category')
        if category:
            mycollections = mycollections.filter(collection_category=category)

    get_date = request.GET.get('get_date')
    if get_date:
        mycollections = mycollections.filter(get_date__exact=get_date)

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min and price_max:
        mycollections = mycollections.filter(price__gte=price_min, price__lte=price_max)
    elif price_min:
        mycollections = mycollections.filter(price__gte=price_min)
    elif price_max:
        mycollections = mycollections.filter(price__lte=price_max)

    # 並び替え順
    order = request.GET.get('order')
    if order == 'name_order':
        mycollections = mycollections.order_by('name')
    elif order == 'register_order_des':
        mycollections = mycollections.order_by('-created_at')
    elif order == 'register_order_asc':
        mycollections = mycollections.order_by('created_at')

    # ページネーション
    paginator = Paginator(mycollections, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'form': form, 'page_obj': page_obj})

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
def collection_edit(request, pk):
    mycollection = get_object_or_404(MyCollection, pk=pk)
    if request.method == 'POST':
        form = MyCollectionForm(request.POST, request.FILES , user=request.user, instance=mycollection)
        if form.is_valid():
            form.save()
            messages.success(request, 'コレクションが編集されました。')
            return redirect('mycollection:home')
    else:
        form = MyCollectionForm(user=request.user , instance=mycollection)

    return  render(request,  'collection_edit.html',  {'form':  form})

@login_required
def collection_delete(request, pk):
    mycollection = get_object_or_404(MyCollection, pk=pk)

    if request.method == 'POST':
        mycollection.delete()
        messages.success(request, 'コレクションが削除されました。')
        return redirect('mycollection:home')

    return redirect('mycollection:home')

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