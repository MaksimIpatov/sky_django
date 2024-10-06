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

from catalog.models import Blog, Contact, Product


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all().order_by("-id")
        return context


class ProductDetailView(DetailView):
    template_name = "products/detail.html"

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        product = Product.objects.get(pk=pk)
        return render(
            request,
            self.template_name,
            context={"product": product},
        )


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

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_published=True)
        return queryset


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
