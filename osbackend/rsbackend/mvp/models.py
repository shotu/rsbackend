# Create your models here.
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

User = get_user_model()


class Test(models.Model):
    title = models.CharField(max_length=255)


class EmissionTemplate(models.Model):
    TEMPLATE_TYPE = (
        ("ONESCOPE"),
        ("CUSTOM",),
        # ('LARGE','Large'),
        # ('EXTRA_LARGE','Extra_Large'),
    )

    TEMPLATE_STATUSES = (
        ("DRAFT", "DRAFT"),
        ("PUBLISHED", "PUBLISHED"),
        # ('NOT_ACTIVE',)
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # other fields
    title = models.CharField(
        "template title", max_length=100, null=False, default="Generic"
    )
    image_url = models.SlugField()
    description = models.TextField(max_length=250, null=False)

    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT
    )  # TODO add logged in user reference
    owner_type = models.TextField()  # TODO add from preconfigured values  TEMPLATE_TYPE

    # Template states
    # status = models.CharField(max_length=50, choices=TEMPLATE_STATUSES, default= TEMPLATE_STATUSES['DRAFT'])
    status = models.CharField(
        max_length=50, choices=TEMPLATE_STATUSES, default="DRAFT", null=False
    )
    is_published = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)  # for soft delete
    is_active = models.BooleanField(default=True)  # Set to
    updated_at = models.DateTimeField(auto_now=True)  # when updated
    created_at = models.DateTimeField(auto_now_add=True)  # when created

    def __str__(self):
        return f"Name:{self.title}"

    # class Meta:
    #     ordering = ["-updated_at"]  # default order when data is returned
    #     app_label = "mvp_apis"  # NA here but If a model is defined outside of an application in INSTALLED_APPS, it must declare which app it belongs to:
    #     db_table = "emission_templates"


# each case is chat user does for a case of partcular type


class Case(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(null=False, max_length=150)
    description = models.TextField()

    template = models.ForeignKey("EmissionTemplate", on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name="cases", blank=True)

    is_deleted = models.BooleanField(default=False)  # for soft delete
    is_active = models.BooleanField(default=True)  # Set to
    updated_at = models.DateTimeField(auto_now=True)  # when updated
    created_at = models.DateTimeField(auto_now_add=True)  # when created

    def __str__(self):
        return f"Case {self.pk} for Template {self.template}"

    # class Meta:
    #     ordering = ["-updated_at"]  # default order when data is returned
    #     app_label = "mvp_apis"  # NA here but If a model is defined outside of an application in INSTALLED_APPS, it must declare which app it belongs to:
    #     db_table = "mvp_cases"


class Message(models.Model):
    MESSAGE_TYPES = (
        ("SYSTEM_SUGGESTED", "SYSTEM_SUGGESTED"),
        ("USER_CREATED", "USER_CREATED"),
        # ('NOT_ACTIVE',)
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(
        Case, on_delete=models.CASCADE, related_name="messages"
    )  # TODO can the Messages exisit without case
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    type = models.CharField(choices=MESSAGE_TYPES, max_length=150)

    content = models.TextField()

    is_deleted = models.BooleanField(default=False)  # for soft delete
    is_active = models.BooleanField(default=True)  # Set to
    updated_at = models.DateTimeField(auto_now=True)  # when updated
    created_at = models.DateTimeField(auto_now_add=True)  # when created

    # timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Message {self.pk} in Case {self.case} for Template {self.case.template}"
        )

    # class Meta:
    #     ordering = ["-updated_at"]  # default order when data is returned
    #     app_label = "mvp_apis"  # NA here but If a model is defined outside of an application in INSTALLED_APPS, it must declare which app it belongs to:
    #     db_table = "mvp_messages"


# TODO Same question can have multiple responses
class LanguageModelResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="model_responses"
    )
    response = models.TextField()

    is_deleted = models.BooleanField(default=False)  # for soft delete
    is_active = models.BooleanField(default=True)  # Set to
    updated_at = models.DateTimeField(auto_now=True)  # when updated
    created_at = models.DateTimeField(auto_now_add=True)  # when created

    def __str__(self):
        return f"LanguageModelResponse {self.pk} for Message {self.message}"

    # class Meta:
    #     # ordering= ["-updated_at"] # default order when data is returned
    #     app_label = "mvp_apis"  # NA here but If a model is defined outside of an application in INSTALLED_APPS, it must declare which app it belongs to:
    #     db_table = "mvp_language_model_responses"

    #     order_with_respect_to = "message"
