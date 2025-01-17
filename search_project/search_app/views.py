from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product
from .forms import SearchForm

# def search_view(request):
#     form = SearchForm(request.GET)  # フォームのインスタンス化
#     results = None
#     if form.is_valid():
#     # クリーンデータからクエリ取得
#         query = form.cleaned_data['query']
#     # 部分一致検索
#         results = Product.objects.filter(name__icontains=query)
#     return render(request, 'search.html', {'form': form, 'results': results})

# def search_view(request):
#     query = request.GET.get('q')
#     if query:
#         # 検索キーワードに基づくフィルタリング
#         results = Product.objects.filter(name__icontains=query)
#     else:
#         # キーワードが無い場合は空の結果を返す
#         results = Product.objects.none()
#         # ページネーションを追加
#     # 1ページに表示する件数を指定（例: 10件ずつ）
#     paginator = Paginator(results, 10)
#     page_number = request.GET.get('page')
#     # 現在のページ番号をGETリクエストから取得
#     # 指定されたページの結果を取得
#     page_obj = paginator.get_page(page_number)
#     # テンプレートに結果とページ情報を渡す
#     return render(request, 'search.html', {'page_obj': page_obj, 'query': query})


def search_view(request):
    form = SearchForm(request.GET or None)
    results = Product.objects.all()  # クエリセットの初期化
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            results = results.filter(name__icontains=query)  # ここでの filter はクエリセットに適用
    # 価格のフィルタリング（最低価格・最高価格）
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        results = results.filter(price__gte=min_price)
    if max_price:
        results = results.filter(price__lte=max_price)

    # クエリセットをリストに変換せず、直接 Paginator に渡す
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {'form': form, 'page_obj': page_obj})