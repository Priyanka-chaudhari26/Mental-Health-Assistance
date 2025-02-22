from django.contrib import admin
import nested_admin
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError

from django.core.exceptions import ValidationError

# Register your models here.
# from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    CustomUser, Assessment, Question, Option,
    UserAssessment, SelfCareContent, Challenge, UserChallenge
)

class OptionInline(nested_admin.NestedTabularInline):
    model = Option
    extra = 3
    min_num = 1
    fk_name = 'question'
    validate_min = True

class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1  # Show 1 empty question field by default
    show_change_link = True
    inlines = [OptionInline]  # Add options inside questions
    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     if not obj.options.exists():
    #         raise ValidationError("Each question must have at least one option.")
    # def clean(self):
    #     super().clean()
    #     for form in self.forms:
    #         if not form.cleaned_data.get('DELETE', False):  # Check if the form is not marked for deletion
    #             question = form.instance
    #             if not question.options.exists():
    #                 raise ValidationError("Each question must have at least one option.")


    # def get_inline_instances(self, request, obj=None):
    #     # This allows nesting OptionInline under QuestionInline
    #     inline_instances = super().get_inline_instances(request, obj)
    #     for inline in inline_instances:
    #         if isinstance(inline, QuestionInline):
    #             inline.inlines = [OptionInline]
    #     return inline_instances

# Customizing the admin for CustomUser
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('anon_username', 'email', 'total_score', 'streak', 'level', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('anon_username', 'email')
    ordering = ('anon_username',)

    fieldsets = (
        (None, {'fields': ('anon_username', 'password')}),
        ('Personal Info', {'fields': ('email', 'total_score', 'streak', 'level')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # 'fields': ('anon_username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
            'fields': ('anon_username', 'email', 'password',  'is_active', 'is_staff', 'is_superuser')}
        ),
    )

# Registering all models
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Assessment)
# class AssessmentAdmin(nested_admin.NestedModelAdmin):
#     inlines = [QuestionInline]
#     list_display = ['title', 'description', 'created_at']
# =================================
    # def save_related(self, request, form, formsets, change):
    #     # Save questions first
    #     super().save_related(request, form, formsets, change)
    # =================================
    # def save_related(self, request, form, formsets, change):
    #     super().save_related(request, form, formsets, change)
    #     # Now validate each question after saving options
    #     for question in form.instance.questions.all():
    #         if not question.options.exists():
    #             raise ValidationError(f"The question '{question.text}' must have at least one option.")
class AssessmentAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'description', 'created_at']

    # def save_model(self, request, obj, form, change):
    #     # Wrap save in a transaction to prevent partial saves
    #     try:
    #         with transaction.atomic():
    #             super().save_model(request, obj, form, change)
    #     except IntegrityError as e:
    #         raise ValidationError(f"Database error: {e}")

    # def save_related(self, request, form, formsets, change):
    #     # Wrap related saves in the same transaction
    #     try:
    #         with transaction.atomic():
    #             # super().save_related(request, form, formsets, change)
    #             # form.save()
    #             assessment = form.save(commit=False)
    #             assessment.save()

    #         # Then save related formsets (Questions & Options)
    #             for formset in formsets:
    #                 instances = formset.save(commit=False)
    #                 # formset.save()
    #                 for instance in instances:
    #                 # Assign the parent (assessment) to the child before saving
    #                     if isinstance(instance, Question):
    #                         instance.assessment = assessment
    #                     instance.save()
    #                 formset.save_m2m()


    #             # Validate after saving all related objects
    #             for question in form.instance.questions.all():
    #                 if not question.options.exists():
    #                     raise ValidationError(f"The question '{question.text}' must have at least one option.")
    #     except IntegrityError as e:
    #         raise ValidationError(f"Foreign Key error: {e}")
# admin.site.register(Assessment)
# admin.site.register(Question)
admin.site.register(Option)
admin.site.register(UserAssessment)
admin.site.register(SelfCareContent)
admin.site.register(Challenge)
admin.site.register(UserChallenge)
