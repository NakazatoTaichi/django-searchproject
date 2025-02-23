from django.shortcuts import render, get_object_or_404, redirect
from .forms import CollectionSearchForm, MyCollectionForm, CollectionCategoryForm, CollectionTagForm, CollectionFavoriteForm
from django.contrib import messages
from .models import MyCollection , CollectionFavorite
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import io
from PIL import Image
from pillow_heif import open_heif
from django.core.files.uploadedfile import InMemoryUploadedFile

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
        uploaded_image = request.FILES.get('image_path')

        if uploaded_image and uploaded_image.name.lower().endswith('.heic'):
            uploaded_image = heic_to_jpeg(uploaded_image)

        form = MyCollectionForm(request.POST, {'image_path': uploaded_image}, user=request.user)
        if form.is_valid():
            mycollection = form.save(commit=False)
            mycollection.user = request.user
            mycollection.save()
            form.save_m2m()
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
        uploaded_image = request.FILES.get('image_path')

        if uploaded_image and uploaded_image.name.lower().endswith('.heic'):
            uploaded_image = heic_to_jpeg(uploaded_image)

        form = MyCollectionForm(request.POST,  {'image_path': uploaded_image} , user=request.user, instance=mycollection)
        if form.is_valid():
            mycollection = form.save(commit=False)
            mycollection.user = request.user
            mycollection.save()
            form.save_m2m()
            messages.success(request, 'コレクションが編集されました。')
            return redirect('mycollection:home')
    else:
        form = MyCollectionForm(user=request.user , instance=mycollection)

    return  render(request,  'collection_edit.html',  {'form':  form})

# HEICをJPGに変更
def heic_to_jpeg(uploaded_image):
    heif_file = open_heif(uploaded_image)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride
    )

    output_io = io.BytesIO()
    image.save(output_io, format="JPEG")
    output_io.seek(0)

    # Django の InMemoryUploadedFile に変換
    return InMemoryUploadedFile(
        output_io,
        'image',
        uploaded_image.name.replace('.HEIC', '.jpg').replace('.heic', '.jpg'),
        'image/jpeg',
        output_io.getbuffer().nbytes,
        None
    )

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

@login_required
def collection_tag_register(request):
    if request.method == 'POST':
        form = CollectionTagForm(request.POST)
        if form.is_valid():
            collection_tag = form.save(commit=False)
            collection_tag.user = request.user
            collection_tag.save()
            messages.success(request, 'タグが登録されました。')
            return redirect('mycollection:collection_tag_register')
    else:
        form = CollectionTagForm()

    return render(request, 'collection_tag_register.html', {'form': form})

@login_required
def collection_add_favorite(request):
    if request.method == 'POST':
        form = CollectionFavoriteForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, 'お気に入りに登録されました。')
            return redirect('mycollection:home')
    return redirect('mycollection:home')

@login_required
def collection_remove_favorite(request):
    if request.method == 'POST':
        favorite = CollectionFavorite.objects.get(user=request.user, mycollection=request.POST.get('mycollection'))
        favorite.delete()
        messages.success(request, 'お気に入りが解除されました。')
        return redirect('mycollection:home')
    return redirect('mycollection:home')

@login_required
def collection_favorites(request):
    favorite_mycollections = MyCollection.objects.filter(
        id__in=CollectionFavorite.objects.filter(user=request.user).values_list('mycollection', flat=True)
    )
    # ページネーション
    paginator = Paginator(favorite_mycollections, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'collection_favorites.html', {'page_obj': page_obj})