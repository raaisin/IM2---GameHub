from django.shortcuts import render, redirect
from .models import Book
from .forms import BorrowBookForm

# Create your views here.

def book_list(request):
    books = Book.objects.all()
    if request.method == 'POST':
        form = BorrowBookForm(request.POST)
        if form.is_valid():
            book_id = request.POST.get('book_id')
            book = Book.objects.get(id=book_id)
            book.borrowed_by = form.cleaned_data['borrowed_by']
            book.due_date = form.changed_data['due_date']
            book.save()
            return redirect('book_list')

    else:
        form = BorrowBookForm()
    return render(request, 'books/book_list.html', {'books': books, 'form': form})
