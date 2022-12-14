from django.contrib import admin
import datetime
from .forms import SubRubricForm

from .models import AdvUser, SubRubric, Rubric, SuperRubric, Bb, AdditionalImage, Comment
from .utilities import send_activation_notification


# Register your models here.


def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, "Letters with requirements have been sent")


send_activation_notifications.short_description = 'Sending emails with activation requirements'


class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Activated'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'done'),
            ('threedays', 'not activated 3 days'),
            ('week', 'More week not activated')
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            days = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=days)

        elif val == 'week':
            days = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=days)


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (('username', 'email'), ('first_name', 'last_name'),
              ('send_messages', 'is_active', 'is_activated'),
              ('is_staff', 'is_superuser'),
              'groups', 'user_permissions',
              ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)


admin.site.register(AdvUser, AdvUserAdmin)


class SubRubricInLine(admin.TabularInline):
    model = SubRubric


class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInLine,)


class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm


admin.site.register(SuperRubric, SuperRubricAdmin)

admin.site.register(SubRubric, SubRubricAdmin)


class AdditionImageInline(admin.TabularInline):
    model = AdditionalImage


class BbAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'content', 'title', 'author', 'created_at')
    fields = (('rubric', 'author'), 'title', 'content', 'price', 'contacts', 'image', 'is_active')
    inlines = (AdditionImageInline,)


admin.site.register(Bb, BbAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at', 'is_active')
    list_display_links = ('author', 'content')
    list_filter = ('is_active',)
    search_fields = ('author', 'content',)
    date_hierarchy = 'created_at'
    fields = ('author', 'content', 'is_active', 'created_at')
    readonly_fields = ('created_at',)


admin.site.register(Comment, CommentAdmin)
