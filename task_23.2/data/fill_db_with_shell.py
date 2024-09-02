from random import choice

from django.utils.text import slugify

from catalog.models import Blog, Category, Product

categories_ids = list(range(1, 11))

for i in categories_ids:
    obj = Category(
        title=f"Категория #{i}",
        description=f"[#{i}]: Lipsum generator: Lorem Ipsum - All the facts",
    )
    obj.save()

# ----------------------

filtered = Category.objects.filter(title="Категория #4")
print(filtered.get().title)
print(filtered.get().description)

# ----------------------


for i in range(1, 101):
    category = Category.objects.get(id=choice(categories_ids))
    obj = Product(
        title=f"Товар #{i}",
        description=f"Generated {i * 2} paragraphs, {i * 10} words",
        image="default.png",
        category=category,
        price=choice(range(100, 1001, 100)),
    )
    obj.save()

# ----------------------

for i in range(1, 45):
    obj = Blog.objects.create(
        title=f"Title №{i}",
        slug=slugify(f"Title #{i}"),
        preview="default.png",
    )
    obj.save()
