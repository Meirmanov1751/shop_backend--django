from django.contrib import admin

from .models import Shop, ShopItem, ShopSchedule, ShopItemImage, ShopItemDetail, ShopWorkTime

admin.site.register(Shop)
admin.site.register(ShopSchedule)
admin.site.register(ShopItem)
admin.site.register(ShopItemDetail)
admin.site.register(ShopItemImage)
admin.site.register(ShopWorkTime)

