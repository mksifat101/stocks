from os import name
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.serializers import Serializer
from .serializers import *
from rest_framework import views, viewsets
from rest_framework import permissions
from rest_framework.response import Response
from warehouse.models import *
from django.contrib import messages
from rest_framework import  status
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from django.http import Http404
import json
from rest_framework.authentication import SessionAuthentication

class TransferViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = Transfer.objects.all()
        serializer = TransferSerializer(queryset, many=True)
        return Response(serializer.data)
    # def retrieve(self, request, pk=None):
    #     queryset = Transfer.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = TransferSerializer(user)
    #     return Response(serializer.data)
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
    permission_classes = [permissions.AllowAny]
    # def retrieve(self, request,pk = None):
    #     queryset = Variant.objects.all()
    #     variant = get_object_or_404(queryset, pk=pk)
    #     serializer = VariantSerializer(variant)
    #     return Response(serializer.data)

class CheckinViewSet(viewsets.ModelViewSet):
    queryset = Checkin.objects.all()
    serializer_class = CheckinItemSerializer
    permission_classes = [permissions.AllowAny]

class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutItemSerializer
    permission_classes = [permissions.AllowAny]

class AdjustmentViewSet(viewsets.ModelViewSet):
    queryset = Adjustment.objects.all()
    serializer_class = AdjustmentSerializer
    permission_classes = [permissions.AllowAny]
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@api_view(['POST'])
def CreateTransfer(request):
    permission_classes = (permissions.AllowAny,)
    items = request.data.get('items','')
    updated_request = request.POST.copy()
    reference = request.data.get('reference','')
    if Checkin.objects.filter(reference = reference).exists():
        return Response({
            'status':False,
            'detail':'Checkin with this Reference already exists'
        }, status.status.HTTP_400_BAD_REQUEST)
    #date = request.data
    #transfer = Transfer.objects.create()
    items = json.loads(items)
    serializer = TransferSerializer(data = request.data)
    if serializer.is_valid():
        transfer = serializer.save()
        for i in items:
            if i is not None:
                item_Obj = Item.objects.filter(pk = i['item'])
                weight = 0
                if item_Obj:
                    item_Obj = item_Obj[0]
                    unit = i['unit']
                    if item_Obj.track_weight:
                            weight = i['weight']
                    quantity = i['quantity']
                    unit_Obj = Unit.objects.get(pk = unit)
                    moving_Obj = MovingItem.objects.create(item = item_Obj,
                    unit = unit_Obj, quantity = int(quantity), weight = weight)
                    moving_Obj.save()

            transfer.item.add(moving_Obj.pk)
            
            messages.add_message(request, messages.SUCCESS, 'Transfer Created Successfully')
            return Response({
                'status':True,
                'detail':'Transfer Created Successfully'
            }) 

    return Response({
       'status':False,
       'detail':'Transfer could not be saved'
    }, status.HTTP_400_BAD_REQUEST)    
    #updated_request.update({'item': item})

    
    
        
    return Response(serializer.data)


@api_view(['POST'])
def CreateCategory(request):
    permission_classes = (permissions.AllowAny,)        
    
    serializer = CategorySerializer(data = request.data)
    if serializer.is_valid():
        category = serializer.save()
       
        messages.add_message(request, messages.SUCCESS, 'Category Created Successfully')
        return Response({
            'status':True,
            'detail':'Category Created Successfully'
        })
        #return redirect('/categories')
    else:
        return Response({
            'status':False,
            'detail':'Invalid request. Please try again'
        })

@api_view(['POST'])
def CreateContact(request):
    permission_classes = (permissions.AllowAny,)        
    
    serializer = ContactSerializer(data = request.data)
    if serializer.is_valid():
        category = serializer.save()
       
        messages.add_message(request, messages.SUCCESS, 'Contact Created Successfully')
        return Response({
            'status':True,
            'detail':'Contact Created Successfully'
        })
        #return redirect('/categories')
    else:
        return Response({
            'status':False,
            'detail':'Invalid request. Please try again'
        })
    pass

@api_view(['POST'])
def CreateCheckin(request):
    permission_classes = (permissions.AllowAny,)
    items = request.data.get('items','')
    reference = request.data.get('reference','')
    if Checkin.objects.filter(reference = reference).exists():
        return Response({
            'status':False,
            'detail':'Checkin with this Reference already exists'
        }, status.HTTP_400_BAD_REQUEST)
    updated_request = request.POST.copy()    
    #date = request.data
    #transfer = Transfer.objects.create()
    #result = [x.strip() for x in items.split(',')]
    items = json.loads(items)
    serializer = CheckinSerializer(data = request.data)
    if serializer.is_valid():
        checkin = serializer.save()
        for i in items:
            print(i)
            #item = Item.objects.filter(pk = int(i))
            if i is not None:
                item_Obj = Item.objects.filter(pk = i['item'])
                weight = 0
                if item_Obj:
                    item_Obj = item_Obj[0]
                    unit = i['unit']
                    if item_Obj.track_weight:
                            weight = i['weight']
                    quantity = int(i['quantity'])
                    unit_Obj = Unit.objects.get(pk = unit)
                    mi = MovingItem.objects.filter(item = i['item'])
                    quant = 0
                    if mi.exists():
                        quant = mi[0].quantity 
                        quantity = quantity + quant
                        #mi[0].quantity = quantity
                        #mi[0].save()
                        new_mi = MovingItem.objects.filter(pk = mi[0].pk).update(quantity = quantity)
                        checkin.items.add(mi[0].pk)
                        # moving_Obj = MovingItem.objects.update(item = item_Obj,
                        # unit = unit_Obj, quantity = int(quantity), weight = weight)
                    else:
                        moving_Obj = MovingItem.objects.create(item = item_Obj,
                        unit = unit_Obj, quantity = int(quantity), weight = weight)
                        checkin.items.add(moving_Obj.pk)
                    # inventory = Inventory.objects.create(
                    #     item = moving_Obj.item,
                    #     warehouse = checkin.warehouse,
                    #     quantity = quantity
                    # )
                    # moving_Obj.save()

           
            checkin.save()
            messages.add_message(request, messages.SUCCESS, 'Checkin Created Successfully')
            return Response({
                'status':True,
                'detail':'Checkin Created Successfully'
            })       
        
    return Response({
       'status':False,
       'detail':'Checkin could not be saved'
    }, status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def CreateCheckout(request):
    permission_classes = (permissions.AllowAny,)
    items = request.data.get('items','')
    updated_request = request.POST.copy()  
    reference = request.data.get('reference','')
    if Checkout.objects.filter(reference = reference).exists():
        return Response({
            'status':False,
            'detail':'Checkout with this Reference already exists'
        }, status.status.HTTP_400_BAD_REQUEST)  
    
    items = json.loads(items)
    serializer = CheckoutSerializer(data = request.data)
    if serializer.is_valid():
        checkout = serializer.save()
        for i in items:
            print(i)
            #item = Item.objects.filter(pk = int(i))
            if i is not None:
                quantity = 0
                item_Obj = Item.objects.filter(pk = i['item'])
                alert_quantity = item_Obj[0].low_stock_alert_quantity
                weight = 0
                if item_Obj:
                    item_Obj = item_Obj[0]
                    unit = i['unit']
                    if item_Obj.track_weight:
                            weight = i['weight']
                    quantity = i['quantity']
                    unit_Obj = Unit.objects.get(pk = unit)
                    moving_Obj = MovingItem.objects.create(item = item_Obj,
                    unit = unit_Obj, quantity = int(quantity), weight = weight)
                    moving_Obj.save()
            #quantity_left = 
            checkout.items.add(moving_Obj.pk)
           
            messages.add_message(request, messages.SUCCESS, 'Checkin Created Successfully')
            return Response({
                'status':True,
                'detail':'Checkout Created Successfully'
            })       
        
    return Response({
       'status':False,
       'detail':'Checkout could not be saved'
    }, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def CreateAdjustment(request):
    permission_classes = (permissions.AllowAny,)
    items = request.data.get('items','')
    
    updated_request = request.POST.copy()  
    reference = request.data.get('reference','')
    if Adjustment.objects.filter(reference = reference).exists():
        return Response({
            'status':False,
            'detail':'Adjustment with this Reference already exists'
        }, status.status.HTTP_400_BAD_REQUEST)  
    
    items = json.loads(items)  
    #date = request.data
    #transfer = Transfer.objects.create()
    
    serializer = AdjustmentSerializer(data = request.data)
    if serializer.is_valid():
        adjustment = serializer.save()
        for i in items:
            print(i)
            #item = Item.objects.filter(pk = int(i))
            if i is not None:
                quantity = 0
                alert_quantity = 0
                item_Obj = Item.objects.filter(pk = i['item'])
                item_track_quantity = item_Obj[0].track_quantity
                if item_track_quantity:
                    alert_quantity = item_Obj[0].low_stock_alert_quantity
                weight = 0
                if item_Obj:
                    item_Obj = item_Obj[0]
                    unit = i['unit']
                    if item_Obj.track_weight:
                            weight = i['weight']
                    quantity = i['quantity']
                    unit_Obj = Unit.objects.get(pk = unit)
                    moving_Obj = MovingItem.objects.create(item = item_Obj,
                    unit = unit_Obj, quantity = int(quantity), weight = weight)
                    moving_Obj.save()
        adjustment.items.add(moving_Obj.pk)
            
        messages.add_message(request, messages.SUCCESS, 'Adjustment Created Successfully')
        return Response({
            'status':True,
            'detail':'Adjustment Created Successfully'
        })       
        
    return Response({
       'status':False,
       'detail':'Checkout could not be saved'
    }, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def CreateWarehouse(request):
    permission_classes = (permissions.AllowAny,)
    serializer = WarehouseSerializer(data = request.data)
    image = request.data.get('image','')
    if serializer.is_valid():
       wh = serializer.save()
       messages.add_message(request, messages.SUCCESS, 'Warehouse Created Successfully')
       return Response({
           'status':True,
           'details':'Warehouse Saved Successfully'
       }, status.HTTP_200_OK)
       #return redirect('/warehouses')
    #wh.image = image
    return Response({
       'status':False,
       'detail':'Warehouse could not be saved'
    }, status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def CreateItem(request):
    authentication_classes = [SessionAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    variants = request.data.get('variant', '')
    variant_Obj = ''
    
            
            # if Option.objects.filter(name = option).exists():
            #     pass
            # else:
            #     variantObject = Variant.objects.create(
            #             name = variant)
            # for option in variants["options"]:
            #     optionData = {}
            #     optionData['name'] = option
            #     #serializer = OptionSerializer(data = optionData)
            #     #if serializer
            #     if Option.objects.filter(name = option).exists():
            #         pass
            #     else:
            #         Option.objects.create(name = option)
                # variantSerializer = VariantSerializer(data = variant)
            
    serializer = ItemSerializerWithoutVariant(data = request.data)
    print(request.data)
    if serializer.is_valid():
        item_Obj = serializer.save()
        if variants:
            variants = json.loads(variants)
        option_obj = ''
        for variant in variants:        
            #temp_data = {'name': variants[variant]}
            variant_name = variant['name']
            options = variant['option']
            variant_Obj = Variant.objects.create(name=variant_name)
            for option in options:                
                option_obj = Option.objects.create(name = option)
                variant_Obj.option.add(option_obj)

            variant_Obj.save()
            if variant_Obj is not None:
                item_Obj.variant.add(variant_Obj)

        messages.add_message(request, messages.SUCCESS, 'Item Created Successfully')
        return Response({
           'status':True,
           'details':'Item Saved Successfully'
       }, status.HTTP_200_OK)
    return Response(serializer.data)
    
@api_view(['GET'])
def SearchItem(request):
    item = request.GET.get('item','')
    i = Item.objects.filter(name__icontains = item)
    # i_dict = model_to_dict(i)
    # oi_serialized = json.dumps(i_dict)
    serializer = ItemSerializer(i, many = True)
    return Response(serializer.data)
    pass

class CategoryDetail(APIView):
    """
    Retrieve, update or delete a category instance.
    """
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.add_message(request, messages.SUCCESS, 'Category Edited Successfully')
            return Response({
                'status':True,
                'detail':'Category Edited Successfully'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        messages.add_message(request, messages.SUCCESS, 'Category Deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)

class ContactDetail(APIView):
    def get_object(self, pk):
        try:
            return Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            raise Http404
   

    def put(self, request, pk, format=None):
        contact = self.get_object(pk)
        serializer = CategorySerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.add_message(request, messages.SUCCESS, 'Contact Edited Successfully')
            return Response({
                'status':True,
                'detail':'Contact Edited Successfully'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        contact = self.get_object(pk)
        contact.delete()
        messages.add_message(request, messages.SUCCESS, 'Contact Deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdjustmentDetail(APIView):
    def get_object(self, pk):
        try:
            return Adjustment.objects.get(pk=pk)
        except Adjustment.DoesNotExist:
            raise Http404
   

    def put(self, request, pk, format=None):
        contact = self.get_object(pk)
        serializer = AdjustmentSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.add_message(request, messages.SUCCESS, 'Adjustment Edited Successfully')
            return Response({
                'status':True,
                'detail':'Adjustment Edited Successfully'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        contact = self.get_object(pk)
        contact.delete()
        messages.add_message(request, messages.SUCCESS, 'Adjustment Deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)

class TransferDetail(APIView):
    def get_object(self, pk):
        try:
            return Transfer.objects.get(pk=pk)
        except Transfer.DoesNotExist:
            raise Http404
   

    def put(self, request, pk, format=None):
        transfer = self.get_object(pk)
        serializer = TransferSerializer(transfer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.add_message(request, messages.SUCCESS, 'Transfer Edited Successfully')
            return Response({
                'status':True,
                'detail':'Transfer Edited Successfully'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            transfer = self.get_object(pk)
            transfer.delete()
            messages.add_message(request, messages.SUCCESS, 'Transfer Deleted')
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            if not e.args[0].find("because they are referenced through protected foreign keys") == -1:
                            messages.add_message(request, messages.ERROR, 'This Warehouse cannot be deleted as it has other references')
                            return Response({
                                'status':False,
                                'detail':"This Transfer cannot be deleted as it has other references"
                            })
            return Response({
                'status': False,
                'detail': "Transfer could not be deleted due to some error."
            },status.HTTP_500_INTERNAL_SERVER_ERROR)

class CheckinDetail(APIView):
    def get_object(self, pk):
        try:
            return Checkin.objects.get(pk=pk)
        except Checkin.DoesNotExist:
            raise Http404
   

    def put(self, request, pk, format=None):
        checkin = self.get_object(pk)
        serializer = CheckinSerializer(checkin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.add_message(request, messages.SUCCESS, 'Checkin Edited Successfully')
            return Response({
                'status':True,
                'detail':'Checkin Edited Successfully'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        contact = self.get_object(pk)
        contact.delete()
        messages.add_message(request, messages.SUCCESS, 'Checkin Deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)

class CheckoutDetail(APIView):
    def get_object(self, pk):
        try:
            return Checkout.objects.get(pk=pk)
        except Checkout.DoesNotExist:
            raise Http404
   

    def put(self, request, pk, format=None):
        checkout = self.get_object(pk)
        serializer = CheckinSerializer(checkout, data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.add_message(request, messages.SUCCESS, 'Checkout Edited Successfully')
            return Response({
                'status':True,
                'detail':'Checkout Edited Successfully'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        contact = self.get_object(pk)
        contact.delete()
        messages.add_message(request, messages.SUCCESS, 'Checkout Deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemDetail(APIView):
    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404
   

    def put(self, request, pk, format=None):
        variants = request.data.get('variant', '')
        item = self.get_object(pk)
        serializer = ItemSerializerWithoutVariant(item, data=request.data)
        if serializer.is_valid():
            item_Obj = serializer.save()
            if variants:
                variants = json.loads(variants)
                option_obj = ''
            for variant in variants:        
                #temp_data = {'name': variants[variant]}
                variant_name = variant['name']
                options = variant['option']
                variant_Obj = Variant.objects.create(name=variant_name)
                for option in options:                
                    option_obj = Option.objects.create(name = option)
                    variant_Obj.option.add(option_obj)

                variant_Obj.save()
                if variant_Obj is not None:
                    item_Obj.variant.add(variant_Obj)
            messages.add_message(request, messages.SUCCESS, 'Item Edited Successfully')
            return Response({
                'status':True,
                'detail':'Item Edited Successfully'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        messages.add_message(request, messages.SUCCESS, 'Item Deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)


class WarehouseDetail(APIView):
    def get_object(self, pk):
        try:
            return Warehouse.objects.get(pk=pk)
        except Warehouse.DoesNotExist:
            raise Http404
   

    def put(self, request, pk, format=None):
        transfer = self.get_object(pk)
        serializer = WarehouseSerializer(transfer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.add_message(request, messages.SUCCESS, 'Warehouse Edited Successfully')
            return Response({
                'status':False,
                'detail':'Warehouse Edited Successfully'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            item = self.get_object(pk)
            item.delete()
            messages.add_message(request, messages.SUCCESS, 'Warehouse Deleted')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            if not e.args[0].find("because they are referenced through protected foreign keys") == -1:
                            messages.add_message(request, messages.ERROR, 'This Warehouse cannot be deleted as it has other references')
                            return Response({
                                'status':False,
                                'detail':"This Warehouse cannot be deleted as it has other references"
                            })
            return Response({
                'status': False,
                'detail': "Warehouse could not be deleted due to some error."
            },status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def CreateUnit(request):
    data = request.data 
    serializer = UnitSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        messages.add_message(request, messages.SUCCESS, 'Checkout Deleted')
        return redirect('/units')
        return Response({
            'status':True,
            'detail':'Unit Created'
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def SaveOptions(variantObj):
    pass