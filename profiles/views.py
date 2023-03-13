from typing import Union

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
)
from django.http import HttpRequest, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


class LoginView(DjangoLoginView):
    """A view that handles user authentication and login.

    Attributes:
        template_name: A string representing the name of the template to use for rendering the login form.

    Methods:
        get: A method that handles GET requests to the view. If the user is already authenticated,
             they will be redirected to the purchase page.
        get_success_url: A method that returns the URL to redirect to after a successful login.

    """
    template_name = "profiles/login.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> Union[TemplateResponse, HttpResponsePermanentRedirect]:
        """Handles GET requests to the view.

        If the user is already authenticated, they will be redirected to the purchase page.

        Args:
            request: An HttpRequest object representing the incoming request.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            A TemplateResponse or HttpResponsePermanentRedirect object.

        """
        if request.user.is_authenticated:
            return redirect("shopping:purchase")
        return super().get(request=request, args=args, kwargs=kwargs)

    def get_success_url(self):
        """Returns the URL to redirect to after a successful login.

       Returns:
           A string representing the URL to redirect to.

       """
        return reverse_lazy("shopping:purchase")


@method_decorator(login_required, name='dispatch')
class LogoutView(DjangoLogoutView):
    """A view that handles user logout.

   Attributes:
       next_page: A string representing the URL to redirect to after a successful logout.

   """
    next_page = reverse_lazy("profiles:login")
