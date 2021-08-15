from django.shortcuts import render
from warehouse.models import *
from accounts.models import *
from .forms import *
from django.db.models import Func
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
# Create your views here.

class Month(Func):
    function = 'EXTRACT'
    template = '% (function)s(MONTH from %(expressions)%) %'

@login_required
def Home(request):
    #checkins = Checkin.objects.annotate(month=Month('date')).values('')
    #context = {'checkins'}
    months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September'
    , 'October', 'November', 'December')
    context = {'months': months}    
    return render(request, 'frontend/Home.html')

@login_required
def Checkins(request):
    fm = CheckinForm()
    checkins = Checkin.objects.order_by('-pk')[0:8].filter()
    context = {'type':'Checkins','data': checkins}
    return render(request, 'frontend/Checkins.html', context)

@login_required
def CheckinDetails(request, pk):
    details = Checkin.objects.filter(pk = pk)
    contacts = Contact.objects.all()
    warehouse = Warehouse.objects.all()
    units = Unit.objects.all()
    unitsString = ''
    for unit in units:
        unitsString += str(unit) + ':' + str(unit.pk) + ','
    context = {}
    if details:
        context = {'details': details[0], 'contacts':contacts, 'warehouses':warehouse,'units':unitsString}
    return render(request, 'frontend/CreateCheckin.html', context)

@login_required
def EditCategory(request, pk):
    details = Category.objects.filter(pk = pk)
    fm = ''
    context = {}
    if details:
        image_name = details[0].image.name.split("/")
        fm = CategoryForm(initial={'name':details[0].name,'code': details[0].code})
        context = {'details': details[0], 'form':fm, 'image_name':image_name[3]}
    return render(request, 'frontend/CreateCategory.html', context)

@login_required
def EditContact(request, pk):
    details = Contact.objects.filter(pk = pk)
    fm = ''
    context = {}
    if details:
        image_name = details[0].image.name.split("/")
        fm = ContactForm(initial={'name':details[0].name,'email': details[0].email,
        'details':details[0].details})
        context = {'details': details[0], 'form':fm, 'image_name':image_name[3]}
    return render(request, 'frontend/CreateCategory.html', context)

@login_required
def EditItem(request, pk):
    barcode_symbology = Symbology
    categories = Category.objects.all()
    units = Unit.objects.all()
    details = Item.objects.filter(pk = pk)
    tags = Tag.objects.all()
    fm = ''
    context = {}
    image_name = ''
    if details:
       
        fm = ItemForm(initial={'name':details[0].name,'code': details[0].code,
        'rack_location':details[0].rack_location,'SKU':details[0].SKU,
        'details':details[0].details,'low_stock_alert_quantity':details[0].low_stock_alert_quantity})
    context = {'details': details[0], 'form':fm, 'categories': categories,
    'units': units,'barcode_symbology':Symbology, 'tags': tags}
    return render(request, 'frontend/CreateItem.html', context)

@login_required
def EditTransfer(request, pk):
    barcode_symbology = Symbology
    categories = Category.objects.all()
    units = Unit.objects.all()
    details = Transfer.objects.filter(pk = pk)
    warehouses = Warehouse.objects.all()
    fm = ''
    context = {}
    
    if details:
        date = str(details[0].date.month) + '-' + str(details[0].date.day) + '-' + str(details[0].date.year)
       
        
    context = {'details': details[0],'categories': categories,
    'units': units,'barcode_symbology':Symbology,'date':date,'warehouses':warehouses}
    return render(request, 'frontend/CreateTransfer.html', context)

@login_required
def EditAdjustment(request, pk):
    barcode_symbology = Symbology
    categories = Category.objects.all()
    units = Unit.objects.all()
    details = Adjustment.objects.filter(pk = pk)
    types = Type.objects.all()
    warehouses = Warehouse.objects.all()
    fm = ''
    context = {}
    image_name = ''
    if details:        
        # fm = ItemForm(initial={'name':details[0].name,'code': details[0].code,
        # 'rack_location':details[0].rack_location,'SKU':details[0].SKU,
        # 'details':details[0].details,'low_stock_alert_quantity':details[0].low_stock_alert_quantity})
        #date = details[0].date
        date = str(details[0].date.month) + '-' + str(details[0].date.day) + '-' + str(details[0].date.year)
        context = {'details': details[0], 'categories': categories,
        'units': units,'barcode_symbology':Symbology,'types':types, 'date': date, 'warehouses': warehouses}
        return render(request, 'frontend/CreateAdjustment.html', context)

@login_required
def EditCheckin(request, pk):
    barcode_symbology = Symbology
    categories = Category.objects.all()
    units = Unit.objects.all()
    details = Checkin.objects.filter(pk = pk)
    contact = Contact.objects.all()
    warehouses = Warehouse.objects.all()
    fm = ''
    context = {}
    image_name = ''
    if details:       
        date = str(details[0].date.month) + '-' + str(details[0].date.day) + '-' + str(details[0].date.year)
        context = {'details': details[0],'categories': categories,
        'units': units,'barcode_symbology':Symbology, 'contacts':contact, 'warehouses':warehouses, 'date':date}
        return render(request, 'frontend/CreateCheckin.html', context)

@login_required
def EditCheckout(request, pk):
    barcode_symbology = Symbology
    categories = Category.objects.all()
    units = Unit.objects.all()
    details = Checkout.objects.filter(pk = pk)
    fm = ''
    context = {}
    image_name = ''
    if details:
        # if details[0].image is not None:
        #     image_name = details[0].image.name.split("/")
        # fm = ItemForm(initial={'name':details[0].name,'code': details[0].code,
        # 'rack_location':details[0].rack_location,'SKU':details[0].SKU,
        # 'details':details[0].details,'low_stock_alert_quantity':details[0].low_stock_alert_quantity})
        date = str(details[0].date.month) + '-' + str(details[0].date.day) + '-' + str(details[0].date.year)
        context = {'details': details[0], 'categories': categories,
        'units': units,'barcode_symbology':Symbology, 'date':date}
        return render(request, 'frontend/CreateCheckout.html', context)

@login_required
def EditWarehouse(request, pk):
    barcode_symbology = Symbology
    categories = Category.objects.all()
    units = Unit.objects.all()
    details = Warehouse.objects.filter(pk = pk)
    fm = ''
    context = {}
    image_name = ''
    if details:          
             
        context = {'details': details[0],'categories': categories,
        'units': units,'barcode_symbology':Symbology}
        return render(request, 'frontend/CreateWarehouse.html', context)

@login_required
def Checkouts(request):
    checkouts = Checkout.objects.order_by('-pk')[0:8].filter()
    context = {'type':'Checkouts','data': checkouts}
    return render(request, 'frontend/Checkouts.html', context)

@login_required
def Adjustments(request):
    adjustments = Adjustment.objects.order_by('-pk')[0:8].filter()
    context = {'adjustments': adjustments}
    return render(request, 'frontend/Adjustments.html', context)

@login_required
def Transfers(request):
    transfers = Transfer.objects.order_by('-pk')[0:8].filter()
    context = {'transfers': transfers}
    return render(request, 'frontend/Transfers.html', context)

@login_required
def Contacts(request):
    contacts = Contact.objects.all()
    context = {'contacts': contacts}
    return render(request, 'frontend/Contacts.html', context)

@login_required
def Categories(request):
    categories = Category.objects.all()
    parentCategories = ParentCategory.objects.all()
    context = {'categories': categories,'parentCategories':parentCategories}
    return render(request, 'frontend/Categories.html', context)

@login_required
def Items(request):
    items = Item.objects.all().order_by('-pk')[0:10].filter()
    #items_rev = items.reverse()
    item_array = []
    item_dict = {}
    warehouse_wise_list = []
    warehouse_dict = {}
    
    qty = 0
    for i in items:
        total = 0
        warehouses = Warehouse.objects.all()
        mi = MovingItem.objects.filter(item = i)
        warehouse_wise_list = []
        for w in warehouses:
            inventory = Inventory.objects.filter(warehouse = w)
            
            if inventory.exists():
                for inv_item in inventory[0].items.all():
                    qty = 0
                    if mi.exists():
                        if mi[0].pk == inv_item.pk:
                            qty = mi[0].quantity
                            total = total + qty
            warehouse_dict = {}
            warehouse_dict['name'] = w.name
            warehouse_dict['qty'] = qty
            total = total + qty
            warehouse_dict['total'] = str(total)
            warehouse_wise_list.append(warehouse_dict)

        i.warehouses = warehouse_wise_list
        # mi = MovingItem.objects.filter(item = i.pk)
        # for inv in Inventory.objects.all():
        #     for inv_item in inv.items.all():
        #         for m in mi.all():
        #             if m.pk == inv_item.pk:
        #                 qty = mi[0].quantity
        #                 warehouse_dict = {}
        #                 warehouse_dict['name'] = inv.warehouse.name
        #                 warehouse_dict['quantity'] = qty
        #                 total = total + qty
                        
        #             else:
        #                 warehouse_dict['name'] = inv.warehouse.name
        #                 warehouse_dict['quantity'] = 0
        #             warehouse_wise_list.append(warehouse_dict)
        # item_dict['item'] = i.pk
        # item_dict['warehouses'] = warehouse_wise_list
        # item_array.append(item_dict)
        
        print(item_array)

        
       # items_rev[0].warehouses = ['1','2','3']



    
    # inventory = Inventory.objects.all()
    # for item in inventory.items.all():
    #     if item.
    context = {'items': items}
    return render(request, 'frontend/Items.html', context)

@login_required
def Units(request):
    units = Unit.objects.all()
    context = {'units': units}
    return render(request, 'frontend/Units.html', context)

@login_required
def Users(request):
    user = User.objects.all()
    context = {'users': user}
    return render(request, 'frontend/Users.html', context)

@login_required
def Warehouses(request):
    warehouses = Warehouse.objects.all().order_by('-pk')[0:10].filter()
    context = {'warehouses': warehouses}
    return render(request, 'frontend/Warehouses.html', context)

@login_required
def CreateCheckin(request):    
    contacts = Contact.objects.all()
    warehouse = Warehouse.objects.all()
    units = Unit.objects.all()
    unitsString = ''
    for unit in units:
        unitsString += str(unit) + ':' + str(unit.pk) + ','
    context = {'contacts': contacts, 'warehouses':warehouse, 'units':unitsString}
    return render(request, 'frontend/CreateCheckin.html', context)

@login_required
def CreateCheckout(request):    
    contacts = Contact.objects.all()
    warehouse = Warehouse.objects.all()
    units = Unit.objects.all()
    unitsString = ''
    for unit in units:
        unitsString += str(unit) + ':' + str(unit.pk) + ','
    context = {'contacts': contacts, 'warehouses':warehouse, 'units':unitsString}
    return render(request, 'frontend/CreateCheckout.html', context)

@login_required
def CreateTransfers(request):    
    fm = TransferForm()
    warehouses = Warehouse.objects.all()
    units = Unit.objects.all()
    unitsString = ''
    for unit in units:
        unitsString += str(unit) + ':' + str(unit.pk) + ','
        pass
    return render(request, 'frontend/CreateTransfer.html',{'form': fm,'warehouses':warehouses,'units':unitsString})

Symbology = [
        ('CODE128'),
        ('CODE39'),
        ('EAN-5'),
        ('EAN-8'),
        ('EAN-13'),
        ('UPC-A'),
    ]

@login_required
def CreateItem(request):   
    units = Unit.objects.all() 
    categories = Category.objects.all()
    barcode_symbology = Symbology
    tags = Tag.objects.all()
    fm = ItemForm()
    return render(request, 'frontend/CreateItem.html',{'form': fm,
    'units': units,'barcode_symbology':barcode_symbology,'categories':categories, 'tags':tags })

@login_required
def CreateAdjustment(request):
    types = Type.objects.all()
    warehouse = Warehouse.objects.all()
    units = Unit.objects.all()
    unitsString = ''
    for unit in units:
        unitsString += str(unit) + ':' + str(unit.pk) + ','
    context = {'types': types, 'warehouses':warehouse, 'units':unitsString}
    return render(request, 'frontend/CreateAdjustment.html', context)

@login_required
def CreateContact(request): 
    fm = ContactForm()  
    return render(request, 'frontend/CreateContact.html',{'form':fm})

@login_required
def CreateCategory(request):   
    fm = CategoryForm()
    parent_categories = ParentCategory.objects.all()
    return render(request, 'frontend/CreateCategory.html',{'form':fm,'parent_categories':parent_categories})

@login_required
def CreateWarehouse(request):   
    fm = WarehouseForm()
    context = {'form': fm}
    return render(request, 'frontend/CreateWarehouse.html', context)

@login_required
def CreateUnit(request):   
    base_unit = BaseUnit.objects.all()
    return render(request, 'frontend/CreateUnit.html',{'base_unit': base_unit})
    
@login_required
def CreateUser(request):   
    return render(request, 'frontend/CreateUser.html')

@login_required
def ImportContacts(request):   
    return render(request, 'frontend/ImportContact.html')

@login_required
def SettingsView(request):
    return render(request, 'frontend/EditSettings.html')


@login_required
def ViewCategory(request,pk):
    return render(request, 'frontend/ViewCategory.html')

@login_required
def ViewItem(request,pk):
    try:
        details = Item.objects.get(pk = pk)

        return render(request, 'frontend/ViewItem.html',{'details': details})
    
    except Exception as e:
        return Http404("Item does not exists or has been deleted")

@login_required
def ViewTransfer(request,pk):
     try:
        details = Transfer.objects.get(pk = pk)
        
        return render(request, 'frontend/ViewTransfer.html',{'details':details})
     except Exception as e:
        return Http404("Item does not exists or has been deleted")


@login_required
def ViewAdjustment(request,pk):
     try:
        details = Adjustment.objects.get(pk = pk)
        
        return render(request, 'frontend/ViewAdjustment.html',{'details':details})
     except Exception as e:
        return Http404("Item does not exists or has been deleted")


@login_required
def ViewCheckin(request,pk):    
     try:
        details = Checkin.objects.get(pk = pk)
        
        return render(request, 'frontend/ViewCheckin.html',{'details':details})
     except Exception as e:
        return Http404("Item does not exists or has been deleted")

@login_required
def ViewCheckout(request,pk):
     try:
        details = Checkout.objects.get(pk = pk)
        
        return render(request, 'frontend/ViewCheckout.html',{'details':details})
     except Exception as e:
        return Http404("Item does not exists or has been deleted")

@login_required
def ViewWarehouse(request,pk):
    try:
        warehouse = Warehouse.objects.get(pk = pk)
        items = []
        inv = Inventory.objects.filter(warehouse = pk)
        for wh in inv.all():
            for inv_item in wh.items.all():
                items.append(inv_item)

            
        return render(request, 'frontend/ViewWarehouse.html',{'warehouse':warehouse,'items':items})
    except Exception as e:
        return Http404("Item does not exists or has been deleted")
