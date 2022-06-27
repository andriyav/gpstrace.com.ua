from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from .models import Item, Category
from .forms import RegisterUserForm, LoginUserForm
from django.urls import reverse_lazy


class HomeView(ListView):
    model = Item
    template_name = "store/items.html"
    context_object_name = 'items'

    def get_queryset(self):
        if '1000' in self.request.GET:
            return Item.objects.filter(battery='1000 мАгод')
        elif '5000' in self.request.GET:
            return Item.objects.filter(battery='5000 мАгод')
        elif '10000' in self.request.GET:
            return Item.objects.filter(battery='10000 мАгод')
        elif '20000' in self.request.GET:
            return Item.objects.filter(battery='20000 мАгод')

        else:
            if 'pricerange' in self.request.GET:
                price_range = self.request.GET['pricerange']
                f = price_range.split(',')
                price_min = float(f[0])
                price_max = float(f[1])
                return Item.objects.filter(price__lte=price_max, price__gte=price_min)
        if 'dropdown' in self.request.GET:
            filter = self.request.GET['dropdown']
        else:
            return Item.objects.all()
        if filter == 'popular':
            return Item.objects.order_by('-label')
        elif filter == 'price':
            return Item.objects.order_by('price')
        elif filter == 'discount':
            return Item.objects.order_by('-discount')


class ShowItem(DetailView):
    model = Item
    template_name = 'store/product.html'
    slug_url_kwarg = 'item_slug'
    context_object_name = 'item_view'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['item_view']
        return context


class CategoryTracker(ListView):
    model = Item
    template_name = 'store/items.html'
    context_object_name = 'items'
    allow_empty = False

    def get_queryset(self):
        return Item.objects.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категорія -' + str(context['items'][0].cat)
        return context


class ShowCategory(ListView):
    model = Category
    template_name = 'store/store.html'
    context_object_name = 'cats'

class CheckOutView(ListView):
    model = Item
    template_name = "store/checkout.html"
    context_object_name = 'ordered_items'


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'store/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    forms_class = LoginUserForm
    template_name = 'store/login.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def logout_user(request):
    logout(request)
    return redirect('home')

