from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.utils.timezone import now, timedelta
from .models import InvitationCode

class InvitationCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'created_at', 'expires_at', 'used_by', 'used_at')
    actions = ['generate_10_invitation_codes']

    # Custom admin action
    def generate_10_invitation_codes(self, request, queryset=None):
        for _ in range(10):
            InvitationCode.objects.create(
                expires_at=now() + timedelta(days=30)
            )
        self.message_user(request, "10 new invitation codes generated.")
        return redirect(request.path)

    generate_10_invitation_codes.short_description = "Generate 10 new invitation codes"

    # Add a custom button on top
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate_invitation_codes/', self.admin_site.admin_view(self.generate_10_invitation_codes_view)),
        ]
        return custom_urls + urls

    def generate_10_invitation_codes_view(self, request):
        self.generate_10_invitation_codes(request)
        return redirect('..')

    # Display the button on the admin page
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['generate_codes_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(InvitationCode, InvitationCodeAdmin)
