from functools import wraps

from django import forms
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url
from django.utils.inspect import func_supports_parameter
from django.utils.translation import ugettext as _, ugettext_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from authlib.email import decode, send_registration_mail


REDIRECT_COOKIE_NAME = "authlib-next"


def set_next_cookie(view):
    @wraps(view)
    def fn(request, *args, **kwargs):
        response = view(request, *args, **kwargs)
        if request.GET.get("next"):
            response.set_cookie(REDIRECT_COOKIE_NAME, request.GET["next"], max_age=600)
        return response

    return fn


def retrieve_next(request):
    next = request.COOKIES.get(REDIRECT_COOKIE_NAME)
    if func_supports_parameter(is_safe_url, "allowed_hosts"):  # Django 1.11
        kw = {"allowed_hosts": {request.get_host()}}
    else:
        kw = {"host": request.get_host()}
    return next if is_safe_url(url=next, **kw) else None


def post_login_response(request, new_user):
    response = redirect(retrieve_next(request) or settings.LOGIN_REDIRECT_URL)
    response.delete_cookie(REDIRECT_COOKIE_NAME)
    return response


@never_cache
@sensitive_post_parameters()
@set_next_cookie
def login(
    request,
    template_name="registration/login.html",
    authentication_form=AuthenticationForm,
    post_login_response=post_login_response,
):

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)

        if form.is_valid():
            auth.login(request, form.get_user())
            return post_login_response(request, new_user=False)
    else:
        form = authentication_form(request)

    return render(request, template_name, {"form": form})


@never_cache
def oauth2(request, client_class, post_login_response=post_login_response):
    User = auth.get_user_model()
    client = client_class(request)

    if all(key not in request.GET for key in ("code", "oauth_token")):
        return redirect(client.get_authentication_url())

    user_data = client.get_user_data()

    if user_data.get("email"):
        email = user_data.pop("email")
        _u, new_user = User.objects.get_or_create(email=email, defaults=user_data)
        if new_user:
            messages.success(request, _("Welcome! Please fill in your details."))

        user = auth.authenticate(email=email)
        if user and user.is_active:
            auth.login(request, user)
        else:
            messages.error(request, _("No user with email address %s found.") % email)

        return post_login_response(request, new_user=new_user)

    else:
        messages.error(request, _("Did not get an email address. Please try again."))

    return redirect("login")


class EmailRegistrationForm(forms.Form):
    email = forms.EmailField(label=ugettext_lazy("email"))

    def __init__(self, *args, **kwargs):
        self._request = kwargs.pop("request")
        super(EmailRegistrationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        User = auth.get_user_model()
        email = self.cleaned_data.get("email")
        if email:
            if (
                self._request.user.is_authenticated
                and email != self._request.user.email
            ):
                raise forms.ValidationError(
                    _(
                        "The email you entered (%(input)s) does not match the"
                        " email of the account you're logged in as currently"
                        " (%(current)s)."
                    )
                    % {"input": email, "current": self._request.user.email}
                )
            if User.objects.filter(email=email, is_active=False).exists():
                raise forms.ValidationError(
                    _("This email address belongs to an inactive account.")
                )
        return email


@never_cache
def email_registration(
    request,
    code=None,
    registration_form=EmailRegistrationForm,
    post_login_response=post_login_response,
    max_age=3600 * 3,
):
    User = auth.get_user_model()

    if code is None:
        if request.method == "POST":
            form = registration_form(request.POST, request=request)
            if form.is_valid():
                send_registration_mail(
                    form.cleaned_data["email"],
                    request=request,
                    user=request.user
                    if request.user.is_authenticated
                    else None,  # noqa
                )

                messages.success(request, _("Please check your mailbox."))
                return redirect(".")

        else:
            form = registration_form(request=request)

        return render(request, "registration/email_registration.html", {"form": form})

    else:
        try:
            email, _user = decode(code, max_age=max_age)
        except ValidationError as exc:
            [messages.error(request, msg) for msg in exc.messages]
            return redirect("../")

        _u, new_user = User.objects.get_or_create(email=email)
        if new_user:
            messages.success(request, _("Welcome! Please fill in your details."))

        user = auth.authenticate(email=email)
        if user and user.is_active:
            auth.login(request, user)

        return post_login_response(request, new_user=new_user)


@never_cache
def logout(request):
    auth.logout(request)
    messages.success(request, _("You have been signed out."))
    return redirect("login")
