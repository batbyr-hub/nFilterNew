# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class NumberType(models.Model):
    id = models.AutoField('id', primary_key=True, db_index=True)
    name = models.CharField(null=True,max_length=255, verbose_name='Нэр')
    price = models.IntegerField(null=True,verbose_name='Үнэ')
    description = models.ImageField(upload_to="new_number/", blank=True, verbose_name="Үйлчилгээний нөхцөл")
    is_active = models.BooleanField(default=1, verbose_name='Одоо худалдаалагдаж байгаа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Бүртгүүлсэн')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Шинэчлэсэн')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "numbertype"
        verbose_name = 'Шинэ дугаарын төрөл'
        verbose_name_plural = "Шинэ дугаарын төрлүүд"

class AziinDugaar(models.Model):
    id = models.AutoField('id', primary_key=True, db_index=True)
    name = models.CharField(null=True,max_length=255, verbose_name='Нэр')
    price = models.IntegerField(null=True,verbose_name='Үнэ')
    type = models.IntegerField(null=True, verbose_name='Төрөл')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Бүртгүүлсэн')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Шинэчлэсэн')

    def __str__(self):
        return self.id

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "aziin_dugaar"
        verbose_name = 'Азын дугаарын төрөл'
        verbose_name_plural = "Азын дугаарын төрлүүд"

class TypeOfService(models.Model):
    id = models.AutoField('id', primary_key=True, db_index=True)
    name = models.CharField(max_length=200,null=True,verbose_name='Үйлчилгээний төрөл')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Бүртгүүлсэн')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Шинэчлэсэн')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "type0fservice"
        verbose_name = 'Урьдчилсан төлбөрт үйлчилгээний төрөл'
        verbose_name_plural = "Урьдчилсан төрбөрт үйлчилгээний төрлүүд"



class Setup(models.Model):
    id = models.AutoField('id', primary_key=True, db_index=True)
    name = models.CharField(null=True,max_length=200,verbose_name='КИОСК машины дугаар')
    card_dispenser_comm_open_code = models.IntegerField(null=True,default=0,verbose_name='card dispenser: port open address')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Бүртгүүлсэн')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Шинэчлэсэн')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "setup"
        verbose_name = 'Setup'
        verbose_name_plural = "Setup"




class PrefixOLD(models.Model):
    id = models.AutoField('id', primary_key=True, db_index=True)
    prefix = models.IntegerField(null=True,verbose_name='Prefix')
    category = models.ForeignKey(NumberType,on_delete=models.CASCADE,null=True,blank=True, verbose_name='Дугаарын төрөл')
    is_active = models.BooleanField(default=1, verbose_name='Одоо худалдаалагдаж байгаа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Бүртгүүлсэн')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Шинэчлэсэн')

    def __str__(self):
        return str(self.prefix)

    def __unicode__(self):
        return str(self.prefix)

    class Meta:
        db_table = "prefix"
        verbose_name = 'Prefix'
        verbose_name_plural = "Prefixes"

class Prefix(models.Model):
    id = models.AutoField('id', primary_key=True, db_index=True)
    prefix = models.IntegerField(null=True,verbose_name='Prefix')
    category = models.ForeignKey(NumberType,on_delete=models.CASCADE,null=True,blank=True, verbose_name='Дугаарын төрөл')
    is_active = models.BooleanField(default=1, verbose_name='Одоо худалдаалагдаж байгаа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Бүртгүүлсэн')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Шинэчлэсэн')

    def __str__(self):
        return str(self.prefix)

    def __unicode__(self):
        return str(self.prefix)

    class Meta:
        db_table = "prefixab"
        verbose_name = 'Prefix'
        verbose_name_plural = "Prefixes"

class UserMessage353(models.Model):
    id = models.BigAutoField(primary_key=True)
    operator = models.CharField(max_length=20, blank=True, null=True)
    sms_from = models.CharField(max_length=20, blank=True, null=True)
    sms_to = models.CharField(max_length=20, blank=True, null=True)
    sms_text = models.CharField(max_length=255, blank=True, null=True)
    sms_response = models.CharField(max_length=600, blank=True, null=True)
    received_at = models.DateTimeField(blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_message_353'
        # verbose_name = 'Мессежээр дугаар хайх'
        # verbose_name_plural = "Мессежээр дугаар хайх жагсаалт"
