# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from options.models import Option


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    """Manage configuration options."""

    list_display = ['public_name', 'value']
    search_fields = ['public_name', 'name']
