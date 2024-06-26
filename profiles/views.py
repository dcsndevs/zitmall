from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.views import generic

from .models import UserProfile
from .forms import UserProfileForm, UserFullnameEmailForm

from checkout.models import Order


@login_required
def view(request):
    """Display the user's profile."""
    profile = get_object_or_404(UserProfile, user=request.user)

    orders = profile.orders.all()

    template = "profiles/profile-view.html"
    context = {"profile": profile, "orders": orders, "on_profile_page": True}

    return render(request, template, context)


@login_required
def profile_address(request):
    """Display the user's profile."""
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            profile_url = reverse_lazy("profile_view")
            return HttpResponseRedirect(profile_url)
        else:
            messages.error(
                request,
                "Update failed. Please ensure the form is valid.")
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = "profiles/profile-address.html"
    context = {"form": form, "orders": orders, "on_profile_page": True}

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(
        request,
        (
            f"This is a past confirmation for order number {order_number}. "
            "A confirmation email was sent on the order date."
        ),
    )

    template = "checkout/checkout_success.html"
    context = {
        "order": order,
        "from_profile": True,
    }

    return render(request, template, context)


class persona(generic.UpdateView):
    form_class = UserFullnameEmailForm
    template_name = "profiles/persona.html"
    success_url = reverse_lazy("profile_view")
    success_message = "User updated"

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(
            self.request, "Your Member profile has been successfully updated!"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            messages.ERROR,
            "Something went wrong...Please try again."
        )
        return redirect("home")


class PasswordsChangeView(PasswordChangeView):
    """
    View for changing profile member password.
    **Context**
    """

    form_class = PasswordChangeForm
    success_url = reverse_lazy("profile_view")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Your Password has been successfully updated!")
        return super().form_valid(form)
