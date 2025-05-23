# users views
from django.http import HttpResponseRedirect , HttpResponse
from django.shortcuts import render , redirect , get_object_or_404
from django.urls import reverse_lazy 
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView , UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreationFormCostum , ProfileForm
from .models import Profile , FriendRequest

# imports for the custoum password reset view ---------
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
# ---------------------------------------------------

# Create your views here.
def home(request):
    return redirect('blog:b-home')

# login view
class Login(LoginView):
    template_name = 'users/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('blog:b-home')
    
# Register view
class Register(CreateView):
    template_name = 'users/register.html'
    model = User
    form_class = UserCreationFormCostum
    
    def form_valid(self, form):
        # Create a profile when a new user is created instead of using signals
        new_user = form.save()
        user_profile = Profile()
        user_profile.user = new_user
        user_profile.save()
        # authenticate the user and redirect him to a main page
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username , password=password)
        if user is not None:
            login(self.request , user)
            # send mail to user that he's now registered
            email_body = render(self.request, 'users/registered-email.txt', {
                            'user': user,
                        }).content.decode('utf-8')
            send_mail(
                        'Welcome to Fakebook 🚀',
                        email_body,
                        'fakebook.projet.l2@gmail.com', 
                        [user.email],
                        fail_silently=False,
                    )
        # redirect
        return HttpResponseRedirect(reverse_lazy('blog:b-home'))
    
# costum reset password view
def custom_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:

                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)

                    reset_url = f"{request.scheme}://{request.get_host()}/password-reset-confirm/{uid}/{token}"

                    email_subject = 'Reset Password on Fakebook'
                    email_body = render(request, 'users/password-reset-email.txt', {
                        'user': user,
                        'reset_url': reset_url,
                    }).content.decode('utf-8')
                    send_mail(
                        email_subject,
                        email_body,
                        'fakebook.projet.l2@gmail.com', 
                        [email],
                        fail_silently=False,
                    )

                return redirect('user:password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'users/password-reset.html', {'form': form})

# profile views
@login_required
def profile(request , username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    # check if user is friend with the profile user
    is_friend = profile.friends.contains(request.user)
    # we also gonna pass user posts in the context when the blog app is ready
    context = {'profile':profile , 'is_friend':is_friend}
    return render(request , 'users/profile.html' , context)


class UpdateProfile(LoginRequiredMixin , UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'users/profile-update.html'

    def get_success_url(self):
        profile_id = self.kwargs['pk']
        profile = Profile.objects.get(id=profile_id)
        username = profile.user.username
        return reverse_lazy('user:u-profile' , kwargs={'username':username})

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()  
        return context
    

# friends views

@login_required  
def send_friend_request(request, pk):
    user = request.user
    requested_user = get_object_or_404(User , id=pk)
    user_profile = Profile.objects.get(user=user)
    # if requested user is already a friend
    if user_profile.friends.contains(requested_user):
        return HttpResponse('requested user is already your friend!')
    # if friend request was already sent
    elif FriendRequest.objects.filter(from_user=user , to_user=requested_user).exists():
        return HttpResponse('friend request was already sent')
    else:
        friend_request = FriendRequest(from_user=user , to_user=requested_user)
        friend_request.save()
        return HttpResponseRedirect(reverse_lazy('user:u-profile' , kwargs = {'username':requested_user.username}))
    

@login_required
def accept_friend_request(request , pk):
    friend_request = FriendRequest.objects.get(id=pk)
    # if the request concern the user
    if friend_request.to_user == request.user:
        friend_request.from_user.profile.friends.add(friend_request.to_user)
        friend_request.to_user.profile.friends.add(friend_request.from_user)
        # delete the friend request 
        friend_request.delete()
        return HttpResponseRedirect(reverse_lazy('user:u-profile' , kwargs = {'username':request.user.username}))
    else:
        return HttpResponse('Error')
    

@login_required
def remove_friend(request , pk):
    friend = get_object_or_404(User , id=pk)
    user = request.user
    if user.profile.friends.contains(friend):
        user.profile.friends.remove(friend)
        friend.profile.friends.remove(user)
        return HttpResponseRedirect(reverse_lazy('user:u-profile' , kwargs = {'username':request.user.username}))
    else:
        return HttpResponse('Error: user was not found in your friends list')    

@login_required
def friend_requests_list(request , username):
    user = get_object_or_404(User, username=username)
    if user != request.user:
        return HttpResponse('Error occured')
    friend_requests = FriendRequest.objects.filter(to_user=user)
    context = {'requests':friend_requests}
    return render(request , 'users/friend-requests-list.html' , context)

@login_required
def friends_list(request , username):
    user = get_object_or_404(User, username=username)
    friends = user.profile.friends.all()
    context = {'friends':friends , 'this_user':user}
    return render(request , 'users/friends-list.html' , context)