from django import forms

from .models import Course


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        first_focus_set = False
        for field_name, field in self.fields.items():
            widget = field.widget
            input_type = getattr(widget, "input_type", "")

            if isinstance(widget, forms.Textarea):
                css_class = "form-control"
                widget.attrs.setdefault("rows", 5)
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

            if not first_focus_set and input_type != "checkbox":
                widget.attrs.setdefault("autofocus", "autofocus")
                first_focus_set = True

            if field_name == "description":
                widget.attrs.setdefault("placeholder", "Describe who this course is for and what they will master")
            elif field_name == "title":
                widget.attrs.setdefault("autocomplete", "off")

    class Meta:
        model = Course
        fields = ("title", "description", "category", "difficulty", "price", "is_published")
