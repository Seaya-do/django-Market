from django.db import transaction
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import FormView
from product.models import Product
from scuser.decorators import login_required
from scuser.models import Scuser
from .forms import RegisterForm
from .models import Order
from .forms import RegisterForm

@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        with transaction.atomic():
            prod = Product.objects.get(pk=form.data.get('product'))
            order = Order(
                quantity=form.data.get('quantity'),
                product=prod,
                scuser=Scuser.objects.get(email=self.request.session.get('user'))
            )
            order.save()
            prod.stuck -= int(form.data.get('quantity'))
            prod.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('/product/' + str(form.data.get('product')))

    def get_form_kwargs(self,**kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request' : self.request
        })
        return kw

@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    template_name = 'order.html'
    context_object_name = 'order_list'

    #queryset으로 내물품 나만(id) 보게하기
    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(scuser__email=self.request.session.get('user'))
        return queryset
