from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from product.forms import ProductCreationForm, ProductChangeForm
from product.models import Product


class ProductListView(ListView):
    model = Product
    # 'product_list.html', {'product_list': Product.objects.all()}
    paginate_by = 2


def list_product(request):
    product_list = Product.objects.all()                  #DB에 있는 product 전체 가져오기
    context = {'product_list': product_list}                # product_list라는 키로 놓기
    return render(request, 'product/product_list.html', context)     #product/product_list.html에 보내기


def update_product(request, pk):
    if request.method == 'POST':
        form = ProductChangeForm(request.POST)    #form에 있는 내용 가져오기
        if form.is_valid():    #form 검사
            selected_product = Product.objects.get(pk=pk)    #pk로 product에서 하나 꺼내기
            selected_product.name = form.cleaned_data.get('name')    #입력한 내용으로 product 수정
            selected_product.price = form.cleaned_data.get('price')
            selected_product.save()#product 저장
        return redirect('product:detail2', pk=pk)
    else:  # 처음에 선택한 내용을 폼으로 보여주기
        seleted_product = Product.objects.get(pk=pk)     # pk로 product 에서 하나 꺼내기
        form = ProductChangeForm(instance=seleted_product)    # form에 표시
    return render(request, 'product/product_update.html', {'form':form})


class ProductDetailView(DetailView):
    model = Product
    # 'product_detail.html', {'product':Product.objects.get(pk=pk)}


def detail_product(request, pk):
    product = Product.objects.get(pk=pk)      # DB에서 pk가 pk인 product 하나 가져오기
    context = {'product': product}
    return render(request, 'product/product_detail.html', context)    # product_datail.html에게 product 라는 변수로 product 보내기


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'price']  # '__all__'
    template_name_suffix = '_create'  # product_form.html -> product_create.html
    success_url = reverse_lazy('product:list') # 추가 성공하면, 이동할 url 이름


def create_product(request):
    if request.method == 'POST': # 사용자가 입력하고 submit 버튼 눌렀을 때
        form = ProductCreationForm(request.POST, request.FILES) # 주의 files는 request.FILES로 꼭 지정해 줘야 함
        if form.is_valid():    #form을 검사
            form.save()       #form에 있는 점보 저장
        return redirect('product:list2')     #저장하고 product:list2로 넘어가기
    else: #처음에 빈 폼 보여주기
        form = ProductCreationForm()
    return render(request, 'product/product_create.html', {'form': form})


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'price'] # '__all___'
    template_name_suffix = '_update'    # product_from.html -> product_update.html
    # 일반적으로 성공하면 detail로 간다
    # success_url = reverse_lazy('product:list')   # 수정 성공하면, 이동할 url 이름
    
    
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product:list') # 삭제 성공하면, 이동할 url 이름
    # product_confirm_delete.html
