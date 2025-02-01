from django.shortcuts import render , redirect
from .forms import MyCollectionForm
from django.contrib import messages
from .models import MyCollection
from django.contrib.auth.decorators import login_required


@login_required
def collection_home(request):
    mycollections = MyCollection.objects.filter(user=request.user)

    return render(request, 'home.html', {'mycollections': mycollections})

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