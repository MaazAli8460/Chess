from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class StyledFormMixin:
    def _apply_field_styles(self) -> None:
        first_focus_set = False
        for field_name, field in self.fields.items():
            widget = field.widget
            input_type = getattr(widget, "input_type", "")

            if isinstance(widget, forms.Textarea):
                css_class = "form-control"
                widget.attrs.setdefault("rows", 4)
            elif input_type == "checkbox":
                css_class = "form-check-input"
            elif isinstance(widget, forms.Select):
                css_class = "form-select"
            else:
                css_class = "form-control"

            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} {css_class}".strip()

            if input_type != "checkbox":
                widget.attrs.setdefault("placeholder", field.label)

            if not first_focus_set and input_type != "checkbox":
                widget.attrs.setdefault("autofocus", "autofocus")
                first_focus_set = True

            if field_name == "username":
                widget.attrs.setdefault("autocomplete", "username")
            elif field_name == "email":
                widget.attrs.setdefault("autocomplete", "email")
            elif field_name in {"password1", "password2"}:
                widget.attrs.setdefault("autocomplete", "new-password")
            elif field_name == "chess_com_username":
                widget.attrs.setdefault("autocomplete", "nickname")

            if field_name == "bio":
                widget.attrs.setdefault("placeholder", "Share your chess goals")


class SignUpForm(StyledFormMixin, UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_field_styles()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "role",
            "chess_com_username",
            "password1",
            "password2",
        )


class ProfileForm(StyledFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_field_styles()

    class Meta:
        model = User
        fields = ("email", "chess_com_username", "bio")
