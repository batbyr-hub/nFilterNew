# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export.widgets import ForeignKeyWidget
from import_export import fields
from django.contrib.admin import DateFieldListFilter
from controller.models import *


# class UserAdmin(admin.ModelAdmin):
#     list_display = ('family_name','last_name','first_name','register','birthday','address','city','updated_at','created_at')
#     search_fields = ['register','last_name','first_name']
#
# class PrefixAdmin(admin.ModelAdmin):
#     list_display = ('prefix','category','is_active','updated_at','created_at')
#     search_fields = ['prefix','is_active']
#
# class AdsAdmin(admin.ModelAdmin):
#     list_display = ('name','description','is_active','updated_at','created_at')
#     search_fields = ['name','description','created_at','updated_at']
#
# class TypeOfServiceAdmin(admin.ModelAdmin):
#     list_display = ('name', 'updated_at', 'created_at')
#     search_fields = ['name',  'created_at', 'updated_at']
#
#
# class UnitAdmin(admin.ModelAdmin):
#     list_display = ('name','profile_id','description','day','balance','price','SKU','is_active','updated_at','created_at')
#     search_fields = ['name','profile_id','description','balance','created_at','updated_at']
#
# class DataAdmin(admin.ModelAdmin):
#     list_display = ('name','profile_id','description','day','balance','price','SKU','is_active','updated_at','created_at')
#     search_fields = ['name','profile_id','description','balance','created_at','updated_at']
#
#
# class KioskStatusAdmin(admin.ModelAdmin):
#     list_display = ('name','is_scanner_active','is_carddispenser_active' ,'sim_card_total','is_casher_active','cash_total','is_printer_active','printer_counter','address','updated_at', 'created_at')
#     search_fields = ['name',  'created_at', 'updated_at']
#
# class NumberTypeAdmin(admin.ModelAdmin):
#     list_display = ('name','price','is_active','created_at', 'updated_at')
#
# class AziinDugaarAdmin(admin.ModelAdmin):
#     list_display = ('name','price','created_at', 'updated_at')
#
# class CashLogAdmin(admin.ModelAdmin):
#     list_display = ("money","kiosk",'order','created_at', 'updated_at', 'payment', 'money_charged', 'order_id', 'sim_id')
#
# class LotteryAdmin(admin.ModelAdmin):
#     list_display = ("success", "billId", "date", "mac_address", "kiosk", "register_number", "internal_code", "bill_type", "lottery", "paid", "number", "order", "ttd", "lottery_warning", "sales_type", 'created_at', 'updated_at')
#     search_fields = ["success", "billId", "date", "mac_address", "kiosk", "register_number", "internal_code", "bill_type", "qr_data", "lottery", "paid", "number", "order", "ttd", "lottery_warning", "sales_type"]
#
# class KartInfoAdmin(admin.ModelAdmin):
#     list_display = ("kiosk", "operation", "amount", "trace_no", "db_ref_no", "rrn", "auth_code", "entry_mode", "terminal_id", "merchant_id", "merchant_name", "pan", "card_holder_name", "batch_no", "created_at", "updated_at")
#     search_fields = ["kiosk", "operation", "amount", "trace_no", "db_ref_no", "rrn", "auth_code", "entry_mode", "terminal_id", "merchant_id", "merchant_name", "pan", "card_holder_name", "batch_no"]
#
#
# admin.site.register(Prefix,PrefixAdmin)
# admin.site.register(TypeOfService,TypeOfServiceAdmin)
# admin.site.register(NumberType,NumberTypeAdmin)
#
# admin.site.register(Setup)