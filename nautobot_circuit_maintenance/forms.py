"""Forms for Circuit Maintenance."""
from django import forms
from django_filters.widgets import BooleanWidget
from nautobot.circuits.models import Circuit, Provider
from nautobot.utilities.forms import (
    BootstrapMixin,
    DateTimePicker,
    DynamicModelMultipleChoiceField,
    StaticSelect2,
    StaticSelect2Multiple,
)
from nautobot.utilities.forms.constants import BOOLEAN_WITH_BLANK_CHOICES
from nautobot.extras.forms import (
    AddRemoveTagsForm,
    CustomFieldBulkEditForm,
    CustomFieldFilterForm,
    CustomFieldModelForm,
    CustomFieldModelCSVForm,
    RelationshipModelForm,
)
from .choices import CircuitMaintenanceStatusChoices
from .models import (
    CircuitImpact,
    CircuitMaintenance,
    Note,
    NotificationSource,
    RawNotification,
)


BLANK_CHOICE = (("", "---------"),)


class CircuitImpactForm(BootstrapMixin, CustomFieldModelForm, RelationshipModelForm):
    """Form for creating new circuit ID info."""

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        """Metaclass attributes for CircuitMaintenanceCircuitImpactAddForm."""

        model = CircuitImpact
        fields = ["maintenance", "circuit", "impact"]
        widgets = {"maintenance": forms.HiddenInput()}


class CircuitImpactCSVForm(CustomFieldModelCSVForm):
    """Form for creating bulk Circuit Impact."""

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        model = CircuitImpact
        fields = CircuitImpact.csv_headers


class CircuitImpactBulkEditForm(BootstrapMixin, AddRemoveTagsForm, CustomFieldBulkEditForm):
    """Form for bulk editing Circuit Impact."""

    pk = forms.ModelMultipleChoiceField(queryset=CircuitImpact.objects.all(), widget=forms.MultipleHiddenInput)

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        nullable_fields = ["impact"]


class CircuitMaintenanceForm(BootstrapMixin, CustomFieldModelForm, RelationshipModelForm):
    """Filter Form for CircuitMaintenance instances."""

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        """Metaclass attributes for CircuitMaintenanceAddForm."""

        model = CircuitMaintenance
        fields = ["name", "start_time", "end_time", "description", "status", "ack"]
        widgets = {"start_time": DateTimePicker(), "end_time": DateTimePicker()}


class CircuitMaintenanceFilterForm(BootstrapMixin, CustomFieldFilterForm):
    """Form for filtering CircuitMaintenance instances."""

    model = CircuitMaintenance

    q = forms.CharField(required=False, label="Search")
    ack = forms.NullBooleanField(required=False, widget=StaticSelect2(choices=BOOLEAN_WITH_BLANK_CHOICES))
    status = forms.MultipleChoiceField(
        choices=CircuitMaintenanceStatusChoices, required=False, widget=StaticSelect2Multiple()
    )
    provider = DynamicModelMultipleChoiceField(
        queryset=Provider.objects.all(),
        to_field_name="slug",
        required=False,
    )
    circuit = DynamicModelMultipleChoiceField(
        queryset=Circuit.objects.all(),
        required=False,
    )
    start_time = forms.DateTimeField(label="Start time after", required=False, widget=DateTimePicker())
    end_time = forms.DateTimeField(label="End time before", required=False, widget=DateTimePicker())


class CircuitMaintenanceCSVForm(CustomFieldModelCSVForm):
    """Form for creating bulk Circuit Maintenances."""

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        model = CircuitMaintenance
        fields = CircuitMaintenance.csv_headers


class CircuitMaintenanceBulkEditForm(BootstrapMixin, AddRemoveTagsForm, CustomFieldBulkEditForm):
    """Form for bulk editing Circuit Maintenances."""

    pk = forms.ModelMultipleChoiceField(queryset=CircuitMaintenance.objects.all(), widget=forms.MultipleHiddenInput)
    status = forms.CharField(max_length=200, required=False)
    ack = forms.BooleanField(required=False, widget=BooleanWidget())
    description = forms.CharField(max_length=200, required=False)

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        nullable_fields = ["status", "ack", "description"]


class NoteForm(BootstrapMixin, CustomFieldModelForm, RelationshipModelForm):
    """Form for creating new maintenance note."""

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        """Metaclass attributes for NoteForm."""

        model = Note
        fields = ["maintenance", "title", "comment", "level"]
        widgets = {"maintenance": forms.HiddenInput()}


class NoteBulkEditForm(BootstrapMixin, AddRemoveTagsForm, CustomFieldBulkEditForm):
    """Form for bulk editing Notes."""

    pk = forms.ModelMultipleChoiceField(queryset=Note.objects.all(), widget=forms.MultipleHiddenInput)
    title = forms.CharField(max_length=200)
    level = forms.CharField(max_length=50, required=False)
    comment = forms.CharField(max_length=200)

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        nullable_fields = ["level"]


class NoteCSVForm(CustomFieldModelCSVForm):
    """Form for creating bulk Notes."""

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        model = Note
        # Omit the `last_updated` field from the CSV form, as it can't be set by the user.
        fields = Note.csv_headers[:-1]


class RawNotificationFilterSetForm(BootstrapMixin, CustomFieldFilterForm):
    """Form for filtering Raw Notification instances."""

    model = RawNotification

    q = forms.CharField(required=False, label="Search")
    provider = DynamicModelMultipleChoiceField(queryset=Provider.objects.all(), to_field_name="slug", required=False)
    sender = forms.CharField(required=False)
    source = DynamicModelMultipleChoiceField(
        queryset=NotificationSource.objects.all(), to_field_name="slug", required=False
    )
    parsed = forms.NullBooleanField(required=False, widget=StaticSelect2(choices=BOOLEAN_WITH_BLANK_CHOICES))
    since = forms.DateTimeField(required=False, widget=DateTimePicker())


class NotificationSourceForm(BootstrapMixin, forms.ModelForm):
    """Form for creating new NotificationSource."""

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        """Metaclass attributes for NotificationSourceForm."""

        model = NotificationSource
        fields = ["providers"]


class NotificationSourceCSVForm(CustomFieldModelCSVForm):
    """Form for creating bulk NotificationSource."""

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        model = NotificationSource
        fields = NotificationSource.csv_headers


class NotificationSourceBulkEditForm(BootstrapMixin, AddRemoveTagsForm, CustomFieldBulkEditForm):
    """Form for bulk editing NotificationSources."""

    pk = forms.ModelMultipleChoiceField(queryset=NotificationSource.objects.all(), widget=forms.MultipleHiddenInput)

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        nullable_fields = ["providers"]


class NotificationSourceFilterSetForm(BootstrapMixin, forms.ModelForm):
    """Form for filtering Notification Sources."""

    q = forms.CharField(required=False, label="Search")

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        model = NotificationSource
        fields = ["q"]
