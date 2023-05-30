from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Webpage
from django.contrib.auth.forms import UserCreationForm
from .forms import WebpageForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from .razorpay_integration import create_razorpay_order

def razorpay_integration_view(request):
    if request.method == 'POST':
        # Get the amount from the form or any other source
        amount = float(request.POST.get('amount', 0))
        order_id = create_razorpay_order(amount)
        return render(request, 'payment.html', {'order_id': order_id, 'amount': amount})
    else:
        return render(request, 'form.html')


def home(request):
    all_posts = Webpage.objects.all()
    return render(request, 'home.html', {'all_posts':all_posts})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        print("erros in th eform ")
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def create_webpage(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        webpage = Webpage.objects.create(
            title=title, content=content, owner=request.user)
        # Redirect to the newly created webpage or an appropriate page
        return redirect('page_detail', page_id=webpage.id)
    return render(request, 'create_webpage.html')


@login_required
def duplicate_webpage(request, page_id):
    original_webpage = Webpage.objects.get(id=page_id)
    if request.method == 'POST':
        form = WebpageForm(request.POST)
        if form.is_valid():
            new_webpage = form.save(commit=False)
            new_webpage.owner = request.user
            new_webpage.save()
            return redirect('page_detail', page_id=new_webpage.id)
    else:
        initial_data = {'title': f"Copy of {original_webpage.title}", 'content': original_webpage.content}
        form = WebpageForm(initial=initial_data)

    context = {
        'form': form,
        'webpage': original_webpage  # Pass the original webpage object to the template context
    }
    return render(request, 'duplicate_webpage.html', context)


@login_required
def edit_webpage(request, page_id):
    webpage = Webpage.objects.get(id=page_id)
    if request.method == 'POST':
        form = WebpageForm(request.POST, instance=webpage)
        if form.is_valid():
            form.save()
            return redirect('page_detail', page_id=webpage.id)
    else:
        form = WebpageForm(instance=webpage)
    return render(request, 'edit_webpage.html', {'form': form})


@login_required
def publish_webpage(request, page_id):
    webpage = Webpage.objects.get(id=page_id)
    webpage.is_published = True
    webpage.save()
    # Redirect to the published webpage or an appropriate page
    return redirect('page_detail', page_id=webpage.id)


@login_required
def page_detail(request, page_id):
    webpage = Webpage.objects.get(id=page_id)

    # Check if the current user is the owner of the webpage
    is_owner = request.user == webpage.owner

    if request.user == webpage.owner:
        owner_articles = Webpage.objects.filter(
            owner=webpage.owner).exclude(id=page_id)

        other_articles = Webpage.objects.exclude(
            owner=webpage.owner)
        
    else:
        owner_articles = Webpage.objects.filter(
            owner=request.user)
        other_articles = Webpage.objects.exclude(
            owner=request.user)

    if request.method == 'POST':
        if 'duplicate' in request.POST:
            # Duplicate the webpage for the current user
            new_webpage = Webpage.objects.create(
                title=f"Copy of {webpage.title}",
                content=webpage.content,
                owner=request.user
            )
            # Redirect to the edit page for the duplicated webpage
            return redirect('edit_webpage', page_id=new_webpage.id)

    return render(request, 'page_detail.html', {'webpage': webpage, 'is_owner': is_owner, 'other_articles': other_articles, 'owner_articles':owner_articles
                                                })
