from django.shortcuts import render, redirect

from catalog.models import Contact


def index(request):
    return render(request, "index.html")


def contacts(request):
    if request.method == "POST":
        data = request.POST
        # print(data.get("name"), data.get("phone"), data.get("message"))
        new_contact = Contact.objects.create(
            name=data.get("name"),
            phone=data.get("phone"),
            message=data.get("message")
        )
        new_contact.save()
        return redirect("/")
    return render(request, "contacts.html")
