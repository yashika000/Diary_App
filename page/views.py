from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (ListView,DetailView,CreateView,UpdateView,DeleteView)
from .models import Note
from django.urls import reverse_lazy




def logout_request(request):
        logout(request)
        messages.info(request,"logged out....")
        return redirect("page:homepage")


def login_request(request):
        if request.method=="POST":
            form=AuthenticationForm(request,data=request.POST)
            if form.is_valid():
                username=form.cleaned_data.get('username')
                password=form.cleaned_data.get('password')
                user=authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    messages.info(request,f"You are loged in as {username}")
                    return redirect("page:homepage")
                else:
                    messages.error(request,"Invalid username or password")
            else:
                    messages.error(request,"Invalid username or password")
        form=AuthenticationForm()
        return render(request,"page/login.html",{"form":form})



def homepage(request):
    return render(request,'page/home.html',context={"Notes": Note.objects.all})
     
def register(request):
    if request.method=="POST":
        form=NewUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"New Account Created:{username}")
            login(request,user)
            messages.info(request,f"You are loged in as {username}")
            return redirect("page:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request,f"{msg}:{form.error_messages[msg]}")

            return render(request = request,template_name = "page/register.html",context={"form":form})



    form=NewUserForm
    return render(request = request,template_name = "page/register.html",context={"form":form})


def pagedetail(request):
    context = {
        'Notes': Note.objects.all()
    }
    return render(request, 'page/page-create.html', context)


class PageCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = 'page/page-create.html'
    fields = ['title', 'content']
    success_url=reverse_lazy('page:homepage')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PageUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = 'page/page-create.html'
    fields = ['title', 'content']
    success_url=reverse_lazy('page:all_page')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PageDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    success_url=reverse_lazy('page:all_page')
    template_name = 'page/page-confirm-delete.html'



class UserPageListView(ListView):
    model = Note
    template_name = 'page/all_page.html'  
    context_object_name = 'Notes'
    paginate_by = 4

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user).order_by('-date_posted')
