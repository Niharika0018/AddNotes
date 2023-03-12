from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm, NotesForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Notes

def homepage(request):
    item_list = Notes.objects.filter(user=request.user.id)
    return render(request, 'home.html', context={'list': item_list})

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("Addnotes:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, 'register.html', context={'register_form': form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("Addnotes:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, template_name='login.html', context={'login_form': form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("Addnotes:homepage")

def notes(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = NotesForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect('Addnotes:homepage')
        form = NotesForm()
        return render(request, 'notes.html', context={'notes_form': form})
    else:
        return redirect("Addnotes:login")

def remove(request, item_id):
    item = Notes.objects.get(id=item_id)
    item.delete()
    messages.info(request, "Notes removed !!!")
    return redirect('Addnotes:homepage')

# def delete_note(request, pk):
#     note = get_object_or_404(Notes, pk=pk)
#     if note.user != request.user:
#         messages.error(request, 'You are not authenticated to perform this action')
#         return redirect("Addnotes:homepage")
#     note.delete()
#     messages.success(request, 'Note deleted successfully!')
#     return redirect("Addnotes:homepage"
