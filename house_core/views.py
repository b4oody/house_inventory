from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login

from house_core.forms import UserRegistrationForm
from house_core.models import Item, Apartment, Room


def pagination(request, model_of_list):
    """
    :param request:
    :param model_of_list:
    :return:
    """
    paginator = Paginator(model_of_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


def index_page_view(request: HttpRequest) -> HttpResponse:
    return render(request, "index/index.html")


@login_required
def items_page_view(request: HttpRequest) -> HttpResponse:
    context = {
        "items": Item.objects.all(),
    }
    return render(
        request,
        "items/items.html",
        context=context
    )


@login_required
def apartments_page_view(request: HttpRequest) -> HttpResponse:
    exclude = {"id", "user", "created_at"}
    apartments = Apartment.objects.all()
    page_obj = pagination(request, apartments)

    fields = [
        field for field in Apartment._meta.concrete_fields
        if field.name not in exclude
    ]

    context = {
        "apartments_fields": fields,
        "page_obj": page_obj,
        "apartments": page_obj
    }
    return render(
        request,
        "apartments/apartments.html",
        context=context
    )


@login_required
def apartment_page_view(request: HttpRequest, pk: id) -> HttpResponse:
    apartment = Apartment.objects.get(pk=pk)

    exclude = {"id", "apartment", "created_at"}
    rooms = Room.objects.filter(apartment=apartment)
    page_obj = pagination(request, rooms)

    fields = [
        field for field in Room._meta.concrete_fields
        if field.name not in exclude
    ]

    context = {
        "apartment": apartment,
        "room_fields": fields,
        "page_obj": page_obj,
        "rooms": page_obj
    }
    return render(
        request,
        "apartments/apartment.html",
        context=context
    )


class ApartmentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Apartment
    template_name = "apartments/update_apartment_form.html"
    fields = [
        "apartment_name",
        "address",
        "apartment_description",
        "purchase_price"
    ]

    def get_success_url(self):
        return reverse_lazy(
            "house_core:pk_apartment_view",
            kwargs={"pk": self.object.pk}
        )


class ApartmentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Apartment
    template_name = "apartments/delete_apartment_form.html"
    success_url = reverse_lazy("house_core:apartments_view")


class UserRegistrationView(generic.CreateView):
    form_class = UserRegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("house_core:apartments_view")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ApartmentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Apartment
    template_name = "apartments/create_apartment_form.html"
    fields = [
        "apartment_name",
        "address",
        "apartment_description",
        "purchase_price"
    ]

    def get_success_url(self):
        return reverse_lazy(
            "house_core:pk_apartment_view",
            kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
