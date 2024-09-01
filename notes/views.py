from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import NoteForm
from .models import Note
from django.contrib.auth import authenticate, login
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.forms import AuthenticationForm


def home_view(request):
    auth_form = AuthenticationForm()
    note_form = NoteForm(data=request.POST)
    notes = Note.objects.filter(user=request.user) if request.user.is_authenticated else []

    if request.method == 'POST':
        if auth_form.is_valid():
            username = auth_form.cleaned_data.get('username')
            password = auth_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('')
        else:
            return redirect('')

        if 'add_note' in request.POST and note_form.is_valid():
            note = note_form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('home')
    else:
        auth_form = AuthenticationForm()
        note_form = NoteForm()

    return render(request, 'home.html', {
        'auth_form': auth_form,
        'note_form': note_form,
        'notes': notes
    })


class NoteListView(ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class NoteDetailView(DetailView):
    model = Note
    template_name = 'note_detail.html'
    context_object_name = 'note'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note_detail', kwargs={'pk': model.pk})

    def get_success_url(self):
        return reverse_lazy('note_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note_detail', kwargs={'pk': model.pk})

    def get_success_url(self):
        return reverse_lazy('note_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
