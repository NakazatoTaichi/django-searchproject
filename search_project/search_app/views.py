from django.shortcuts import render
from .models import Product
def search_view(request):
    query = request.GET.get('q')  # 'q'は検索キーワード
    if query:
        # 部分一致検索
        results = Product.objects.filter(name__icontains=query)
    else:
        # クエリが空の場合は空の結果
        results = Product.objects.none()
    # 結果をテンプレートに渡す
    return render(request, 'search.html', {'results': results})
