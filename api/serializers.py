from django.db.models import fields
from rest_framework import serializers
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from warehouse.models import *
from django.core.files.base import ContentFile
import base64
# import six
import uuid


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class VariantSerializer(serializers.ModelSerializer):
    option = OptionSerializer(many = True)
    class Meta:
        model = Variant
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):     
    parser_classes = [MultiPartParser, FormParser, JSONParser]  
    variant = VariantSerializer(many = True)
    class Meta:
        model = Item
        fields = '__all__'

class ItemSerializerWithoutVariant(serializers.ModelSerializer):     
    parser_classes = [MultiPartParser, FormParser, JSONParser]  
    #variant = VariantSerializer(many = True)
    class Meta:
        model = Item
        fields = ['name','category', 'code','unit','barcode_symbology','rack_location','SKU',
        'image','details','track_quantity','track_weight','track_variant','low_stock_alert_quantity','tag']

class TransferItemSerializer(serializers.ModelSerializer):      
    item = ItemSerializer(many = True) 
    class Meta:
        model = Transfer
        fields = '__all__'

class CheckinItemSerializer(serializers.ModelSerializer):      
    items = ItemSerializer(many = True) 
    class Meta:
        model = Checkin
        fields = '__all__'

class CheckoutItemSerializer(serializers.ModelSerializer):      
    items = ItemSerializer(many = True) 
    class Meta:
        model = Checkout
        fields = '__all__'

class TransferSerializer(serializers.ModelSerializer):      
    #item = ItemSerializer(many = True) 
    class Meta:
        model = Transfer
        fields = ['date','from_warehouse','to_warehouse','reference','details','attachment','is_draft']

class CheckinSerializer(serializers.ModelSerializer):      
    #item = ItemSerializer(many = True) 
    class Meta:
        model = Checkin
        fields = ['date','contact','warehouse','reference','details','attachment','is_draft']

class CheckoutSerializer(serializers.ModelSerializer):      
    #item = ItemSerializer(many = True) 
    class Meta:
        model = Checkout
        fields = ['date','contact','warehouse','reference','details','attachment','is_draft']

class AdjustmentSerializer(serializers.ModelSerializer):      
    #item = ItemSerializer(many = True) 
    class Meta:
        model = Adjustment
        fields = ['date','type','warehouse','reference','details','attachment','is_draft']


class CategorySerializer(serializers.ModelSerializer):      
    #item = ItemSerializer(many = True) 
    class Meta:
        model = Category
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):      
    #item = ItemSerializer(many = True) 
    class Meta:
        model = Contact
        fields = '__all__'
        


# class OptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Option
#         fields = '__all__'










# class Base64ImageField(serializers.ImageField):
#     """
#     A Django REST framework field for handling image-uploads through raw post data.
#     It uses base64 for encoding and decoding the contents of the file.

#     Heavily based on
#     https://github.com/tomchristie/django-rest-framework/pull/1268

#     Updated for Django REST framework 3.
#     """
#     def get_file_extension(self, file_name, decoded_file):
#         import imghdr

#         extension = imghdr.what(file_name, decoded_file)
#         extension = "jpg" if extension == "jpeg" else extension

#         return extension

#     def to_internal_value(self, data):       
#         # Check if this is a base64 string
#         if isinstance(data, six.string_types):
#             # Check if the base64 string is in the "data:" format
#             if 'data:' in data and ';base64,' in data:
#                 # Break out the header from the base64 content
#                 header, data = data.split(';base64,')

#             # Try to decode the file. Return validation error if it fails.
#             try:
#                 decoded_file = base64.b64decode(data)
#             except TypeError:
#                 self.fail('invalid_image')

#             # Generate file name:
#             file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
#             # Get the file name extension:
#             file_extension = self.get_file_extension(file_name, decoded_file)

#             complete_file_name = "%s.%s" % (file_name, file_extension, )

#             data = ContentFile(decoded_file, name=complete_file_name)

#         return super(Base64ImageField, self).to_internal_value(data)



class WarehouseSerializer(serializers.ModelSerializer):  
    # image = Base64ImageField(
    #     max_length=None, use_url=True,
    # )     
    class Meta:
        model = Warehouse
        fields = '__all__'
