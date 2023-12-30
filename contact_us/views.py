# contactus/views.py
from django.shortcuts import render, redirect
from .forms import ContactForm  # Create this form in the next step

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (you can save to the database if needed)
            # For example: form.save()
            return redirect('contact_us_success')
    else:
        form = ContactForm()

    return render(request, 'contact_us/contact_us.html', {'form': form})

def contact_us_success(request):
    return render(request, 'contact_us/contact_us_success.html')
