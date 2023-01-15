from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from main.models import Settings
from . import forms
from . import utils
from .models import GeneratedImageModel

# Create your views here.

DEFAULT_VARIATE = 5
DEFAULT_INITIAL = {"size": forms.DalleForm.SIZES[2], "amount": 1}


@login_required
def ai_page(request):
    context = {}
    saved_imgs = utils.get_saved_imgs(request.user, 20)
    if saved_imgs:
        context["gallery"] = saved_imgs
        context["gallery_message"] = "Saved images:"
    
    if request.method == "POST":
        form = forms.DalleForm(request.POST)
        print(f"\n\n\n{form.data} {form.is_valid()}\n\n\n")
        
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]
            amount = form.cleaned_data["amount"]
            size = form.cleaned_data["size"]
            
            key = Settings.objects.get(user=request.user).openai_key
            data = {"form": form,
                    "generated": utils.get_generated_imgs(key, prompt, amount, size),
                    "prompt": prompt,
                    "amount": amount,
                    "size": size,
                    }
            context.update(data)
            return render(request=request, template_name="ai_page.html", context=context)
    
    context["form"] = forms.DalleForm(initial=DEFAULT_INITIAL)
    return render(request=request, template_name="ai_page.html", context=context)


@login_required
def variate(request, url, prompt, size, amount):
    key = Settings.objects.get(user=request.user).openai_key
    initial = {"prompt": prompt, "size": size, "amount": amount}
    context = {"generated": utils.variate_image(key, url, DEFAULT_VARIATE),
               "form": forms.DalleForm(initial=initial)}
    context.update(initial)
    return render(request=request, template_name="ai_page.html", context=context)


@login_required
def save_page(request, url, prompt, size):
    utils.save_image_to_db(request, url, prompt, size)
    return render(request=request, template_name="save.html")


@login_required
def resolution_page(request, url, prompt, size):
    return render(request=request, template_name="resolution.html",
                  context={"result": utils.increase_image_resolution(url), "prompt": prompt, "size": size})


@login_required
def gallery_page(request):
    gallery = utils.get_saved_imgs(request.user)
    if gallery:
        context = {
            "gallery_message": "Wow, you have wonderful collection!",
            "gallery": gallery,
        }
    else:
        context = {"message": "Nothing is here... But magic is coming! Try Dall-E"}
    return render(request=request, template_name="gallery_page.html", context=context)


@login_required
def download_page(request, url, prompt, size):
    return render(request=request, template_name="download.html",
                  context={"url": url, "prompt": prompt, "size": size})


@login_required
def image_page(request, pk):
    try:
        image = GeneratedImageModel.objects.get(pk=pk)
    except GeneratedImageModel.DoesNotExist:
        return render(request=request, template_name="image_page.html", context={"message": "Error 404: Not found."})
    
    if image.user != request.user and not request.user.is_superuser:
        message = "This is private picture, you don't have permissions to view it"
        return render(request=request, template_name="image_page.html", context={"message": message})
    
    context = {"image": image, "size": utils.get_resolution(image.resolution)}
    return render(request=request, template_name="image_page.html", context=context)


@login_required
def delete_image_page(request, pk):
    try:
        image = GeneratedImageModel.objects.get(pk=pk)
    except GeneratedImageModel.DoesNotExist:
        return render(request=request, template_name="image_page.html", context={"message": "Error 404: Not found."})
    
    if image.user != request.user and not request.user.is_superuser:
        message = "This is private picture, you don't have permissions to delete it"
        return render(request=request, template_name="image_page.html", context={"message": message})

    image.delete()
    return redirect(to="gallery")