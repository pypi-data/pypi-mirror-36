#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhangyue'

from django import template
from bee_django_coin.exports import filter_local_datetime,get_user_coin


register = template.Library()


# 本地化时间
@register.filter
def local_datetime(_datetime):
    return filter_local_datetime(_datetime)


# 求两个值的差的绝对值
@register.filter
def get_difference_abs(a, b):
    return abs(a - b)

# 获取用户的M币数量
@register.filter
def get_coin(user):
    coin = get_user_coin(user)
    return coin
