from django.db import models
from django.core.validators import RegexValidator
from django.db.models.base import Model
from datetime import datetime
from django.core.exceptions import ValidationError
# Create your models here.

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+9999999999")


class TransferAttachment(models.Model):
    file = models.FileField(upload_to='static/files/transfer/', null=True, blank=True)



class Warehouse(models.Model):    
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=12, blank=True)
    # logo = models.ImageField(height_field=None, blank=True, null=True)
    image = models.ImageField(upload_to = 'static/files/warehouse/', height_field=None,blank=True, null=True)
    address = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if (Inventory.objects.filter(warehouse = self)).exists():
            pass
        else:
            Inventory.objects.create(warehouse = self)
        if Warehouse.objects.filter(pk = self.pk).exists():
            w = Warehouse.objects.filter(code = self.code)
            if w.count() > 1:
                    raise ValidationError('Warehouse with this code exists already', code='invalid')
            
        else:
            if Warehouse.objects.filter(code = self.code).exists():
                    raise ValidationError('Warehouse with this code exists already', code='invalid')
    
    def update(self, *args, **kwargs):               
        #self.item.save(file_name, self.image, save = False)  
        # if Warehouse.objects.filter(code = self.code).exists():
        #     raise ValidationError('Warehouse with this code exists already', code='invalid')

        super().save(*args, **kwargs) 
        return self.id

class ParentCategory(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
           verbose_name_plural = 'ParentCategories'
    def __str__(self):
        return self.name

# def CheckUniqueCode(obj, ):
#     code = obj.code
    
#     if obj.
        

class Category(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    image = models.ImageField(upload_to = 'static/files/category/', blank=True, null=True)
    parent_category = models.ForeignKey(ParentCategory, on_delete=models.PROTECT, null=True, blank=True)
    class Meta:
           verbose_name_plural = 'Categories'    

    def __str__(self):       
        return self.name

    def save(self, *args, **kwargs):
        if Category.objects.filter(pk = self.pk).exists():
            c = Category.objects.filter(code = self.code)
            if c.count() > 1:
                    raise ValidationError('Category with this code exists already', code='invalid')
            super().save(*args, **kwargs)
        else:
            if Category.objects.filter(code = self.code).exists():
                    raise ValidationError('Category with this code exists already', code='invalid')
            super().save(*args, **kwargs)

    def update(self, *args, **kwargs):               
        #self.item.save(file_name, self.image, save = False)  
        # if Category.objects.filter(code = self.code).exists():
        #     raise ValidationError('Category with this code exists already', code='invalid')

        super().save(*args, **kwargs) 
        return self.id   
        
class BaseUnit(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) :
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=30)
    base_unit = models.ForeignKey(BaseUnit, on_delete = models.PROTECT, blank=True, null=True)
    def __str__(self) :
        return self.name
    def save(self, *args, **kwargs):
        if Unit.objects.filter(code = self.code).exists():
                raise ValidationError('Unit with this code exists already', code='invalid')
        super().save(*args, **kwargs)
    
    def update(self, *args, **kwargs):               
        #self.item.save(file_name, self.image, save = False)  
        if Unit.objects.filter(code = self.code).exists():
            raise ValidationError('Unit with this code exists already', code='invalid')

        super().save(*args, **kwargs) 
        return self.id

Barcode_Symbology = [
    ('CODE128','CODE128'),
    ('CODE39','CODE39'),
    ('EAN-5','EAN-5'),
    ('EAN-8','EAN-8'),
    ('EAN-13','EAN-13'),
    ('UPC-A','UPC-A'),
]
class Option(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) :
        return self.name

class Variant(models.Model):
    name = models.CharField(max_length=100)
    option = models.ManyToManyField(Option)
    def __str__(self) :
        return self.name

class ItemVariant(models.Model):
    #name = models.CharField(max_length=100)
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT)
    option = models.ForeignKey(Option, on_delete=models.PROTECT)
    def __str__(self) :
        return self.variant.name

# class ItemVariantCollection(models.Model):
#     item_variants = models.ManyToManyField(ItemVariant)
#     # def __str__(self) :
#     #     return self.id

class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    code = models.CharField(max_length=30)
    tag = models.CharField(max_length=100, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, blank=True, null=True)
    barcode_symbology = models.CharField(choices=Barcode_Symbology,max_length=20, blank=True)
    rack_location = models.CharField(max_length=50, blank=True)
    SKU = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to = 'static/files/item/', blank=True, null=True)
    details = models.TextField(blank=True)
    track_quantity = models.BooleanField(default=True)
    track_weight = models.BooleanField(default=False)
    track_variant = models.BooleanField(default=False)
    variant = models.ManyToManyField(Variant, blank=True, null=True)
    low_stock_alert_quantity = models.IntegerField(null=True, blank=True)    

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if Item.objects.filter(pk = self.pk).exists():
            c = Item.objects.filter(code = self.code)
            if c.count() > 1:
                    raise ValidationError('Item with this code exists already', code='invalid')
            super().save(*args, **kwargs)
        else:
            if Item.objects.filter(code = self.code).exists():
                    raise ValidationError('Item with this code exists already', code='invalid')
            super().save(*args, **kwargs)
    
    def update(self, *args, **kwargs):               
        #self.item.save(file_name, self.image, save = False)  
        # if Item.objects.filter(code = self.code).exists():
        #     raise ValidationError('Item with this code exists already', code='invalid')

        super().save(*args, **kwargs) 
        return self.id   


class MovingItem(models.Model):
    item = models.ForeignKey(Item, on_delete = models.PROTECT)
    variant = models.ManyToManyField(ItemVariant)
    #variant = models.ForeignKey(ItemVariantCollection, on_delete=models.PROTECT)
    #option = models.ForeignKey(Option, on_delete=models.PROTECT)
    unit = models.ForeignKey(Unit, on_delete = models.PROTECT)
    quantity = models.IntegerField()
    weight = models.IntegerField(blank=True, null=True)
    #warehouse = models.ForeignKey(Warehouse, on_delete=)
    def __str__(self):
            return self.item.name

class Inventory(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    items = models.ManyToManyField(MovingItem)
    # quantity = models.BigIntegerField()
    # weight = models.IntegerField(null=True, blank=True)
    # count = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.warehouse.name 

def attachment_location(instance, filename):
    case_name = instance.name.lower().replace(" ", "-")
    file_name = filename.lower().replace(" ", "-")
    return "attachment/{}/{}".format(case_name, file_name)


class Transfer(models.Model):
    date = models.DateField(default=datetime.now)
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='from_warehouse')
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='to_warehouse')
    reference = models.CharField(max_length=30)
    item = models.ManyToManyField(MovingItem)
    details = models.TextField(blank=True)
    attachment = models.FileField(upload_to='static/files/transfers/', blank=True)
    is_draft = models.BooleanField(default=False)

    def __str__(self):
        return self.reference

    def save(self, *args, **kwargs):
        if(self.from_warehouse == self.to_warehouse):
                raise ValidationError('To Warehouse should not be same as From warehouse', code='invalid')
        if Transfer.objects.filter(pk = self.pk).exists():
            c = Transfer.objects.filter(reference = self.reference)
            if c.count() > 1:
                    raise ValidationError('Transfer with this reference exists already', code='invalid')
            super().save(*args, **kwargs)
        else:            
            super().save(*args, **kwargs)
        
    
    def update(self, *args, **kwargs):               
        #self.item.save(file_name, self.image, save = False)   
        # if Transfer.objects.filter(reference = self.reference).exists():
        #         raise ValidationError('Transfer with this reference exists already', code='invalid')            
        super().save(*args, **kwargs) 
        return self.id         

class TransferFileAttachment(models.Model):
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to=attachment_location, null=True, blank=True)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=12)
    details = models.TextField(blank=True)
    def __str__(self):
        return self.name



class Checkin(models.Model):
    date = models.DateField(default=datetime.now)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)
    reference = models.CharField(max_length=30)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    items = models.ManyToManyField(MovingItem)    
    attachment = models.FileField(upload_to='static/files/checkins/', blank=True)
    details = models.TextField(blank=True)
    is_draft = models.BooleanField(default=False)
    def __str__(self):
        return self.reference

    def save(self, *args, **kwargs):        
        
        if Checkin.objects.filter(pk = self.pk).exists():
            c = Checkin.objects.filter(reference = self.reference)
            if c.count() > 1:
                    raise ValidationError('Checkin with this code exists already', code='invalid')
            super().save(*args, **kwargs)
            try:
                for item in self.items.all():
                    # m = MovingItem.object.get(item = item)
                    # #m.quantity = 
                    # print(item)
                    pass
                inv = Inventory.objects.filter(warehouse = self.warehouse)
                item_list = []
                if inv.exists():             
                        for item in self.items.all():
                            inv[0].items.add(item.pk)
                            #inv.items.add(item)
                            #item_list.append(item)
                            #new_mi = MovingItem.objects.filter(pk = mi.pk).update(quantity = quantity)
                        
                else:
                     new_inv = Inventory.objects.create(warehouse = self.warehouse)       
                     for item in self.items.all():
                            new_inv.items.add(item)
                            
            except Exception as e:
                print("An exception occurred: ", e)
        else:   
                super().save(*args, **kwargs)    
                if self.items.all().count() > 0:
                    w = Inventory.objects.create(warehouse = self.warehouse)
                    for items in self.items.all():
                        w.items.add(items) 
                    
                
            

    def update(self, *args, **kwargs):               
        #self.item.save(file_name, self.image, save = False)           
        super().save(*args, **kwargs) 

        return self.id        

class Checkout(models.Model):
    date = models.DateField(default=datetime.now)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)
    reference = models.CharField(max_length=30)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    items = models.ManyToManyField(MovingItem)
    details = models.TextField(blank=True)
    is_draft = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='static/files/checkouts/', blank=True)
    def __str__(self):
        return self.reference
        
    def save(self, *args, **kwargs):
            if Checkout.objects.filter(pk = self.pk).exists():
                c = Checkout.objects.filter(reference = self.reference)
                if c.count() > 1:
                        raise ValidationError('Checkout with this code exists already', code='invalid')
                super().save(*args, **kwargs)
            else:
                super().save(*args, **kwargs)

    def update(self, *args, **kwargs):               
        #self.item.save(file_name, self.image, save = False)   
        # if Checkout.objects.filter(reference = self.reference).exists():
        #         raise ValidationError('Checkout with this reference exists already', code='invalid')            
        super().save(*args, **kwargs) 
        return self.id     

Adjustment_Type = [
    ('Damage','Damage'),
    ('Addition','Addition'),
    ('Subtraction','Subtraction'),
]

class Type(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Adjustment(models.Model):
    date = models.DateField(default=datetime.now)
    #type = models.CharField(choices=Adjustment_Type, max_length=30, default='Damage')
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    reference = models.CharField(max_length=30)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    items = models.ManyToManyField(MovingItem)
    attachment = models.FileField(upload_to='static/files/adjustments/', blank=True)
    details = models.TextField(blank=True)
    is_draft = models.BooleanField(default=False)
    
    def __str__(self):
        return self.reference
    
    def save(self, *args, **kwargs):
            if Adjustment.objects.filter(pk = self.pk).exists():
                c = Adjustment.objects.filter(reference = self.reference)
                if c.count() > 1:
                        raise ValidationError('Adjustment with this code exists already', code='invalid')
                super().save(*args, **kwargs)
            else:
                super().save(*args, **kwargs)

    def update(self, *args, **kwargs):               
        #self.item.save(file_name, self.image, save = False)   
        
        super().save(*args, **kwargs) 
        return self.id      





    
