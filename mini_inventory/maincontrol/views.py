from django.shortcuts import render, redirect
from .models import Inventories, Transactions
from .forms import CreateInventoryForm, RecieveInventoryForm, SendOutInventoryForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
# Create your views here.

def index(request):
    return render(request, 'maincontrol/prime.html')




def create_inventory(request):
    if request.method == 'POST':
        form = CreateInventoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Inventory Successfully created')
            return redirect('create_inventory')

    form = CreateInventoryForm(request.POST or None)
    return render(request, 'maincontrol/create_inventory.html', {'form': form})






def recieve_inventory(request):
    try:
        currently_managing = Inventories.objects.get(currently_managed=True)
    except:
        messages.add_message(request, messages.ERROR, 'You have not set an inventory workspace')
        return redirect('currently_managing_a')

    if request.method == 'POST':
        form = RecieveInventoryForm(request.POST)

        if form.is_valid():
            price = form.cleaned_data.get('price')
            quantity_recieved = form.cleaned_data.get('quantity_recieved')


            #go through transactions to se if its the first or reoccuring transaction
            check_first = Transactions.objects.filter(inventory=currently_managing)
            if check_first.exists():
                #get the last transaction on that inventory
                last_transaction = Transactions.objects.filter(inventory=currently_managing).last()
                #claculate the total
                total = float(price) * int(quantity_recieved)

                #calculated the updated bal qty and value
                updated_bal_qty = int(last_transaction.balance_quantity) + int(quantity_recieved)
                updated_bal_value = float(last_transaction.balance_value) + float(total)

                #create the transaction object
                create_trans = Transactions.objects.create(action='reciept', inventory=currently_managing, quantity_recieved=quantity_recieved, price_recieved=price, total_cost=total, balance_quantity=updated_bal_qty, balance_value=updated_bal_value, quantity_remaining=quantity_recieved)

                messages.add_message(request, messages.INFO, 'Stocks have been added')
                return redirect('recieve_inventory')

            else:
                #make process for first transaction in the inventory
                total = float(price) * int(quantity_recieved)
                #create transaction
                create_trans = Transactions.objects.create(action='reciept', inventory=currently_managing, quantity_recieved=quantity_recieved, price_recieved=price, total_cost=total, balance_quantity=quantity_recieved, balance_value=total, quantity_remaining=quantity_recieved)

                messages.add_message(request, messages.INFO, 'Stocks have been added')
                return redirect('recieve_inventory')

    form = RecieveInventoryForm(request.POST or None)
    return render(request, 'maincontrol/recieve_inventory.html', {'form': form, 'current':currently_managing})







def send_out_inventory(request):
    try:
        currently_managing = Inventories.objects.get(currently_managed=True)
    except:
        messages.add_message(request, messages.ERROR, 'You have not set an inventory workspace')
        return redirect('currently_managing_a')

    if request.method == 'POST':
        form = SendOutInventoryForm(request.POST)
        if form.is_valid():

            #get the qty required
            quantity_required = form.cleaned_data.get('quantity_sent_out')
            qty_req = int(quantity_required)

            #first thing is to check wether qty required is available
            get_bal_qty = Transactions.objects.filter(inventory=currently_managing).last()
            #check if there are any reciepts
            if get_bal_qty is None:
                messages.add_message(request, messages.INFO, 'No recorded reciepts')
                return redirect('send_out_inventory')

            qty_available = get_bal_qty.balance_quantity

            #this list will be to hold all value of requisition
            value_list = []

            #check for availability
            if quantity_required <= qty_available:

                #check the stock method so u know how to calculate
                if currently_managing.method_of_management == 'FIFO':
                    #look up all available stock reciepts
                    lookup = Transactions.objects.filter(inventory=currently_managing).filter(action='reciept').exclude(quantity_remaining=0)

                    for instance in lookup:

                        if instance.quantity_remaining > qty_req:
                            remaining_qty = instance.quantity_remaining - qty_req
                            instance.quantity_remaining = remaining_qty
                            instance.save(update_fields=['quantity_remaining'])

                            #create bal quantities and values 
                            value_list.append(qty_req*instance.price_recieved)
                            print(value_list)

                            #update qty rec
                            qty_req = 0
                    
                        #check for possible bug
                        elif instance.quantity_remaining < qty_req:
                            print('okay')
                            qty_req = qty_req - instance.quantity_remaining

                            value_list.append(instance.price_recieved*instance.quantity_remaining)
                            print(value_list)

                            instance.quantity_remaining = 0
                            instance.save(update_fields=['quantity_remaining'])

                            #create balances
                            

                        else:
                            print('eq')
                            qty_req = qty_req - instance.quantity_remaining     
                            instance.quantity_remaining = 0
                            instance.save(update_fields=['quantity_remaining'])
                            #create balances

                            #bug at eq calculation
                            value_list.append(instance.price_recieved*quantity_required)
                            print(value_list)
                            #update qty rec
                            qty_req = 0

                        if qty_req == 0:

                            last_bal_qty = get_bal_qty.balance_quantity
                            last_bal_value = get_bal_qty.balance_value
                            
                            #create requisition
                            record_requisition = Transactions.objects.create(action='requisition', inventory=currently_managing, quantity_sent_out=quantity_required, total=sum(value_list), balance_quantity=last_bal_qty-quantity_required, balance_value=last_bal_value-sum(value_list))
                            print('here')

                            #final
                            break

                    #after a successfull withdrawal
                    messages.add_message(request, messages.INFO, 'Inventory requisited')
                    return redirect('send_out_inventory')



                elif currently_managing.method_of_management == 'LIFO':
                    #look up all available stock reciepts
                    lookup = Transactions.objects.filter(inventory=currently_managing).filter(action='reciept').exclude(quantity_remaining=0).reverse()

                    for instance in lookup:

                        if instance.quantity_remaining > qty_req:
                            remaining_qty = instance.quantity_remaining - qty_req
                            instance.quantity_remaining = remaining_qty
                            instance.save(update_fields=['quantity_remaining'])

                            #create bal quantities and values 
                            value_list.append(qty_req*instance.price_recieved)
                            print(value_list)

                            #update qty rec
                            qty_req = 0
                    
                        #check for possible bug
                        elif instance.quantity_remaining < qty_req:
                            print('okay')
                            qty_req = qty_req - instance.quantity_remaining

                            value_list.append(instance.price_recieved*instance.quantity_remaining)
                            print(value_list)

                            instance.quantity_remaining = 0
                            instance.save(update_fields=['quantity_remaining'])

                            #create balances
                            

                        else:
                            print('eq')
                            qty_req = qty_req - instance.quantity_remaining     
                            instance.quantity_remaining = 0
                            instance.save(update_fields=['quantity_remaining'])
                            #create balances

                            #bug at eq calculation
                            value_list.append(instance.price_recieved*quantity_required)
                            print(value_list)
                            #update qty rec
                            qty_req = 0

                        if qty_req == 0:

                            last_bal_qty = get_bal_qty.balance_quantity
                            last_bal_value = get_bal_qty.balance_value
                            
                            #create requisition
                            record_requisition = Transactions.objects.create(action='requisition', inventory=currently_managing, quantity_sent_out=quantity_required, total=sum(value_list), balance_quantity=last_bal_qty-quantity_required, balance_value=last_bal_value-sum(value_list))
                            print('here')

                            #final
                            break

                    #after a successfull withdrawal
                    messages.add_message(request, messages.INFO, 'Inventory requisited')
                    return redirect('send_out_inventory')



                else:
                    print('currently not available for avp')
                    #get the prices and calculate their average

            else:
                messages.add_message(request, messages.INFO, 'The quantity you need is not in stock')
                return redirect('send_out_inventory')


    form = SendOutInventoryForm(request.POST or None)
    return render(request, 'maincontrol/send_out_inventory.html', {'form': form})





# viewing all inventories
def currently_managing_a(request):
    get_all = Inventories.objects.all()
    return render(request, 'maincontrol/set_currently_managing.html', {'inventories': get_all})




# this is used to view all transactions relating to the current inventory workspace
def view_all(request):
    try:
        active_inventory = Inventories.objects.get(currently_managed=True)
    except:
        messages.add_message(request, messages.ERROR, 'You need to set a current stock workspace')
        return redirect('currently_managing_a')

    get_all = Transactions.objects.filter(inventory=active_inventory)
    return render(request, 'maincontrol/view_inventory.html', {'transactions': get_all})


# set currently managing stock
def currently_managing_b(request, pk):
    get_all = Inventories.objects.all()

    for inventory in get_all:
        if inventory.id == pk:
            inventory.currently_managed = True
            inventory.save(update_fields=['currently_managed'])

        else:
            inventory.currently_managed = False
            inventory.save(update_fields=['currently_managed'])

    messages.add_message(request, messages.INFO, 'Stock has been set to currently managing')
    return redirect('currently_managing_a')