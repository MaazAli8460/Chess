from django import forms

from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            input_type = getattr(widget, "input_type", "")

            if isinstance(widget, forms.Textarea):
                css_class = "form-control"
                widget.attrs.setdefault("rows", 4)
            elif isinstance(widget, forms.Select):
                css_class = "form-select"
            elif input_type == "checkbox":
                css_class = "form-check-input"
            else:
                css_class = "form-control"

            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} {css_class}".strip()

            if input_type != "checkbox":
                widget.attrs.setdefault("placeholder", field.label)

            if field_name == "quote":
                widget.attrs.setdefault("placeholder", "Share the impact in their own words")

    class Meta:
        model = Testimonial
        fields = ("name", "title", "quote", "rating", "is_published", "sort_order")
