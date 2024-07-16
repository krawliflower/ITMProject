from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, TutorForm, UserUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        tutor_form = TutorForm(request.POST)
        
        if form.is_valid() and tutor_form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            
            if role == 'tutor':
                profile = profile.objects.create(user=user, role=role)
                selected_subjects = tutor_form.cleaned_data.get('subject')
                profile.subjects.set(selected_subjects)
                profile.facebook_username = tutor_form.cleaned_data.get('facebook_username')
                profile.contact_number = tutor_form.cleaned_data.get('contact_number')
                profile.save()
                
            messages.success(request, 'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
        tutor_form = TutorForm()
    
    return render(request, 'users/register.html', {
        'form': form,
        'tutor_form': tutor_form,
    })

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }

    return render(request, 'users/profile.html', context)
