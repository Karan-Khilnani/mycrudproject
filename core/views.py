from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from .forms import RegisterForm, NoteForm
from .models import Note


def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def dashboard_view(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    notes = Note.objects.filter(user=request.user)

    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if category:
        notes = notes.filter(category=category)

    total = Note.objects.filter(user=request.user).count()
    pinned = Note.objects.filter(user=request.user, is_pinned=True).count()

    context = {
        'notes': notes,
        'query': query,
        'category': category,
        'total': total,
        'pinned': pinned,
        'categories': Note.CATEGORY_CHOICES,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def note_create_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'Note created successfully!')
            return redirect('dashboard')
    else:
        form = NoteForm()
    return render(request, 'core/note_form.html', {'form': form, 'action': 'Create'})


@login_required
def note_update_view(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully!')
            return redirect('dashboard')
    else:
        form = NoteForm(instance=note)
    return render(request, 'core/note_form.html', {'form': form, 'action': 'Update', 'note': note})


@login_required
def note_delete_view(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('dashboard')
    return render(request, 'core/note_confirm_delete.html', {'note': note})