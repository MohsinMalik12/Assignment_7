import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# ------------------------------------------------------------------

@csrf_exempt
def split_evenly(request) :
    if request.method == "POST" :
        data = json.loads(request.body)
        user_ids = data.get('user_ids')
        total_bill = data.get('total_bill')
        user_length = len(user_ids)
        result = total_bill / user_length
        return JsonResponse({"Bill_Of_Per_Person" : int(result)})
    else:
        return JsonResponse({"Error !" : "POST Method Allowed Only"})

# input must follow given pattern :    
# {
#   "user_ids" : [100, 200, 300, 400],
#   "total_bill" : 400
# }

# ------------------------------------------------------------------

@csrf_exempt
def split_unevenly(request) :
    if request.method == "POST" :
        data = json.loads(request.body)
        contibutions = data.get('contributions')
        total_bill = data.get('total_bill')
        user_length = len(contibutions)
        per_person_bill = int(total_bill / user_length)
        lst = []
        for user_detail in contibutions :
            user_id = user_detail["user_id"]
            user_contribution = user_detail["contribution"]
            user_amount = user_contribution - per_person_bill
            to_pay = 0
            to_receive = 0
            if user_amount == 0 :
                to_receive = 0
                to_pay = 0
            if user_amount > 0 :
                to_receive = int(user_amount)
            else :
                to_pay = int(user_amount)
            result = {
                "user_id" : user_id,
                "total_bill_to_pay" : per_person_bill,
                "user_pay_bill" : user_contribution,
                "receive_from_other" : to_receive,
                "pay_to_other" : to_pay
            }
            lst.append(result)
        return JsonResponse({"Bill_Of_Per_Person_To_Pay_Eachother" : lst})
    else:
        return JsonResponse({"Error !" : "POST Method Allowed Only"})

# input must follow given pattern :
# {
#   "contributions" : [
#     {"user_id" : 100, "contribution": 100},
#     {"user_id" : 200, "contribution": 150},
#     {"user_id" : 300, "contribution": 75},
#     {"user_id" : 400, "contribution": 75}
#   ],
#   "total_bill" : 400
# }

# ------------------------------------------------------------------

@csrf_exempt
def split_evenly_include_tip_tax(request) :
    if request.method == "POST" :
        data = json.loads(request.body)
        user_ids = data.get('user_ids')
        total_bill = data.get('total_bill')
        user_length = len(user_ids)
        tip_percentage = data.get('tip_percentage')
        tax_percentage = data.get('tax_percentage')
        total_tip = total_bill * tip_percentage / 100
        total_tax = total_bill * tax_percentage / 100
        users_total_bill = total_bill + total_tax + total_tip
        per_user_total_bill = users_total_bill / user_length
        return JsonResponse({"Bill_Of_Per_Person_With_Tip_Tax" : int(per_user_total_bill)})
    else:
        return JsonResponse({"Error !" : "POST Method Allowed"})

# input must follow given pattern :    
# {
#   "user_ids" : [100, 200, 300, 400],
#   "total_bill" : 400,
#   "tip_percentage" : 10,
#   "tax_percentage" : 10
# }   

# ------------------------------------------------------------------

@csrf_exempt
def split_evenly_include_discount(request) :
    if request.method == "POST" :
        data = json.loads(request.body)
        user_ids = data.get('user_ids')
        total_bill = data.get('total_bill')
        user_length = len(user_ids)
        discount_percentage = data.get('discount_percentage')
        total_discount = total_bill * discount_percentage / 100
        users_total_bill = total_bill - total_discount
        per_user_total_bill = users_total_bill / user_length
        return JsonResponse({"Bill_Of_Per_Person_With_Discount" : int(per_user_total_bill)})
    else:
        return JsonResponse({"Error !" : "POST Method Allowed"})

# input must follow given pattern :    
# {
#   "user_ids" : [100, 200, 300, 400],
#   "total_bill" : 400,
#   "discount_percentage" : 15
# }

# ------------------------------------------------------------------  
    
@csrf_exempt
def split_include_shared_items(request) :
    if request.method == "POST" :
        data = json.loads(request.body)
        user_ids = data.get('user_ids')
        items_detail = data.get('items_detail')
        lst = []
        for details in items_detail :
            item_name = details["item_name"]
            item_price = details["item_price"]
            share_with = details["share_with"]
            user_length = len(share_with)
            per_person_ammount = item_price / user_length
            for ids in share_with :
                lst_data = {
                    "user_id" : ids,
                    "per_person_ammount" : per_person_ammount
                }
                lst.append(lst_data)
        return JsonResponse({"Amount_due_of_each_user": lst})
    else:
        return JsonResponse({'error':'only POST method is allowed'})    
    
# input must follow given pattern
#   {
#   "user_ids" : [100, 200, 300, 400],
#   "items_detail" : [
#     {"item_name" : "Pizza", "item_price" : 200, "share_with" : [100, 300]},
#     {"item_name" : "Fish", "item_price" : 400, "share_with" : [200, 400]},
#     {"item_name" : "Burger", "item_price" : 500, "share_with" : [100, 200]}
#   ]
# }