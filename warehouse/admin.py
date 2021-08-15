from django.contrib import admin
from .models import *
# Register your models here.

class AttachmentFileAdmin(admin.StackedInline):
    model = TransferFileAttachment


admin.site.register(Warehouse)
admin.site.register(Item)
admin.site.register(MovingItem)
admin.site.register(Transfer)
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Contact)
admin.site.register(Checkin)
admin.site.register(Checkout)
admin.site.register(Adjustment)
admin.site.register(Variant)
admin.site.register(ItemVariant)
admin.site.register(BaseUnit)
admin.site.register(ParentCategory)
admin.site.register(Option)
admin.site.register(Type)
admin.site.register(Tag)
admin.site.register(Inventory)

