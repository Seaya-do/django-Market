from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework import mixins

from django.views.generic import ListView,DeleteView
from django.views.generic.edit import FormView
from scuser.decorators import login_required, admin_required
from .models import Product
from .forms import RegisterForm
from order.forms import RegisterForm as OrderForm
from .serializers import ProductSerializer


class ProductListAPI(generics.GenericAPIView,mixins.ListModelMixin):
    serializer_class = ProductSerializer
    def get_queryset(self):
        return Product.objects.all().order_by('id')
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

#mixins.RetrieveModelMixin상세보기를 위한 모델
class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer
    def get_queryset(self):
        return Product.objects.all().order_by('id')
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)


class ProductList(ListView):
    model = Product
    paginate_by = 6
    template_name = 'product.html'
    context_object_name = 'product_list'

    #페이지네이션 커스텀
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page -1 )/ page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context



@method_decorator(admin_required, name='dispatch')
class ProductCreate(FormView):
    model = Product
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        product = Product(
            name=form.data.get('name'),
            price=form.data.get('price'),
            description=form.data.get('description'),
            stuck=form.data.get('stuck')
        )
        product.save()
        return super().form_valid(form)


class ProductDetail(DeleteView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm(self.request)
        return context