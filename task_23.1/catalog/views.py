from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from catalog.forms import ProductForm, ProductForModeratorForm, VersionForm
from catalog.models import Blog, Contact, Product, Version


class IndexView(TemplateView):
    template_name = "index.html"


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "products/list.html"
    login_url = "/users/login/"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all().order_by("-id")
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    template_name = "products/detail.html"
    login_url = "/users/login/"

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        product = Product.objects.get(pk=pk)
        return render(
            request,
            self.template_name,
            context={"product": product},
        )


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/form.html"
    success_url = reverse_lazy("product_list")
    login_url = "/users/login/"

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.author = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/form.html"
    login_url = "/users/login/"

    def get_success_url(self):
        return reverse(
            "product_detail",
            args=(self.kwargs.get("pk"),),
        )

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        product_formset = inlineformset_factory(
            Product,
            Version,
            VersionForm,
            extra=1,
        )
        if self.request.method == "POST":
            data["formset"] = product_formset(
                self.request.POST,
                instance=self.object,
            )
        else:
            data["formset"] = product_formset(
                instance=self.object,
            )
        return data

    def form_valid(self, form):
        data = self.get_context_data()
        formset = data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    formset=formset,
                ),
            )

    def get_form_class(self):
        permissions_data = (
            "catalog.can_cancel_publication",
            "catalog.can_change_description",
            "catalog.can_change_category",
        )

        user = self.request.user
        if user == self.object.author:
            return ProductForm
        if all(user.has_perm(permission) for permission in permissions_data):
            return ProductForModeratorForm
        raise PermissionDenied(
            "У вас недостаточно прав для выполнения этого действия",
        )


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "products/delete.html"
    success_url = reverse_lazy("product_list")


class ContactView(View):
    template_name = "contacts.html"

    def get(self, request, *args, **kwargs):
        data = {"contacts": Contact.objects.all()}
        return render(
            request,
            self.template_name,
            context=data,
        )

    def post(self, request, *args, **kwargs):
        data = request.POST
        new_contact = Contact.objects.create(
            name=data.get("name"),
            phone=data.get("phone"),
            message=data.get(
                "message",
            ),
        )
        new_contact.save()
        return redirect("contacts")


class BlogListView(ListView):
    model = Blog
    template_name = "blog/list.html"


class BlogDetailView(DetailView):
    model = Blog
    template_name = "blog/detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return super().get_object()


class BlogCreateView(CreateView):
    model = Blog
    fields = (
        "title",
        "preview",
    )
    template_name = "blog/form.html"
    success_url = reverse_lazy("blog_list")

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ("title",)
    template_name = "blog/form.html"

    def get_success_url(self):
        return reverse("blog_detail", args=(self.kwargs.get("pk"),))


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = "blog/delete.html"
    success_url = reverse_lazy("blog_list")
