from django.shortcuts import render , redirect
from .forms import MyCollectionForm
from django.contrib import messages
from .models import MyCollection
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def collection_home(request):
    mycollections = MyCollection.objects.filter(user=request.user)

    # ページネーション
    paginator = Paginator(mycollections, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'page_obj': page_obj})

@login_required
def collection_register(request):
    if request.method == 'POST':
        form = MyCollectionForm(request.POST, request.FILES)
        if form.is_valid():
            mycollection = form.save(commit=False)
            mycollection.user = request.user
            mycollection.save()
            messages.success(request, 'コレクションが登録されました。')
            return redirect('mycollection:home')
    else:
        form = MyCollectionForm()

    return render(request, 'collection_register.html', {'form': form})