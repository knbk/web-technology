from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})