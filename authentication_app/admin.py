from django.contrib import admin
from authentication_app import models
from django.contrib.auth.admin import UserAdmin
from django import forms

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('email','password','user_type')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    list_display = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('email', 'password','user_type')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'is_superuser', 'is_staff', 'is_active')}
            ),
        )

    filter_horizontal = ()

    

# Register your models here.
admin.site.register(models.User,CustomUserAdmin)
admin.site.register(models.user_info)