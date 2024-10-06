from django.shortcuts import redirect, render, get_object_or_404

from catalog.models import Contact, Product


def index(request):
    products = Product.objects.all().order_by("-id")
    return render(request, "index.html", context={"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = {
        "product": product
    }
    return render(request, "products/detail.html", context=data)


def contacts(request):
    if request.method == "POST":
        data = request.POST
        # print(data.get("name"), data.get("phone"), data.get("message"))
        new_contact = Contact.objects.create(
            name=data.get("name"),
            phone=data.get("phone"),
            message=data.get("message"),
        )
        new_contact.save()
        return redirect("contacts")

    all_contacts = Contact.objects.all()

    return render(
        request,
        "contacts.html",
        context={"contacts": all_contacts},
    )
