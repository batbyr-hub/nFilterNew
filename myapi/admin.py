# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from myapi.models import *
import csv
from django.http import HttpResponse
from django.contrib.admin import DateFieldListFilter
# from daterangefilter.filters import PastDateRangeFilter, FutureDateRangeFilter

# Register your models here.
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sms_from', 'sms_to', 'sms_text', 'sms_response', 'received_at', 'responded_at', 'status')
    list_filter = (('received_at', DateFieldListFilter), 'status')
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([unicode(getattr(obj, field)).encode("utf-8", "replace") for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

admin.site.register(UserMessage353, UserMessageAdmin)
admin.site.disable_action('delete_selected')
