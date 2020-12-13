from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.db.models import Max
from django.db import connection
from receipt.models import *
import json
# Create your views here.
def index(request):
    data = {}
    return render(request, 'receipt/receipt.html', data)
#------------------------------------------------------------------------
#------------------------------------------------------------------------
class PaymenMethodtList(View):
    def get(self, request):
        payments = list(Payment.objects.all().values())
        data = dict()
        data['payments'] = payments
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class PaymentMethodDetail(View):
    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        data = dict()
        data['payments'] = model_to_dict(payment)
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

#--------------------------------------------------------------------------

class ProductList(View):
    def get(self,request):
        products = list(Product.Objects.all().value())
        data = dict()
        data['products'] = products
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response
    
class ProductDetail(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        data = dict()
        data['products'] = model_to_dict(product)
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

#--------------------------------------------------------------------------

class MemberList(View):
    def get(self, request):
        members = list(Member.objects.all().values())
        data = dict()
        data['members'] = members
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class MemberDetail(View):
    def get(self, request, pk):
        member = get_object_or_404(Member, pk=pk)
        data = dict()
        data['members'] = model_to_dict(member)
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

#------------------------------------------------------------------------

class ShopList(View):
    def get(self, request):
        shops = list(Shop.objects.all().values())
        data = dict()
        data['shops'] = shops
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class ShopDetail(View):
    def get(self, request, pk):
        shop = get_object_or_404(Shop, pk=pk)
        data = dict()
        data['shops'] = model_to_dict(shop)
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

#------------------------------------------------------------------------
# class InvoiceList(View):
#     def get(self, request):
#         invoices = list(Invoice.objects.order_by('invoice_no').all().values())
#         data = dict()
#         data['invoices'] = invoices
#         response = JsonResponse(data)
#         response["Access-Control-Allow-Origin"] = "*"
#         return response

# class InvoiceDetail(View):
#     def get(self, request, pk, pk2):
#         invoice_no = pk + "/" + pk2

#         invoice = list(Invoice.objects.select_related("custome").filter(invoice_no=invoice_no).values('invoice_no', 'date', 'customer_code', 'customer_code__name','due_date','total','vat','amount_due'))
#         invoicelineitem = list(InvoiceLineItem.objects.select_related('product_code').filter(invoice_no=invoice_no).order_by('lineitem').values("lineitem","invoice_no","product_code","product_code__name","product_code__units","unit_price","quantity","extended_price"))

#         data = dict()
#         data['invoice'] = invoice[0]
#         data['invoicelineitem'] = invoicelineitem

#         response = JsonResponse(data)
#         response["Access-Control-Allow-Origin"] = "*"
#         return response

# class InvoiceForm(forms.ModelForm):
#     class Meta:
#         model = Invoice
#         fields = '__all__'

# class InvoiceLineItemForm(forms.ModelForm):
#     class Meta:
#         model = InvoiceLineItem
#         fields = '__all__'

#------------------------------------------------------------------------

class ReceiptList(View):
    def get(self, request):
        receipts = list(Receipt.objects.order_by('ReceiptNo').all().values())
        data = dict()
        data['receipts'] = receipts
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class ReceiptDetail(View):
    def get(self, request, pk, pk2):
        ReceiptNo = pk + "/" + pk2

        receipt = list(Receipt.objects.select_related("CRID").filter(ReceiptNo=ReceiptNo).values('ReceiptNo', 'Date', 'CRID', 'CRID_Name','TotalPrice','PointEarned','PName','SName','ShRID'))
        receiptlineitem = list(ReceiptLineItem.objects.select_related('RNo').filter(RNo=ReceiptNo).order_by('OrderNo').values("OrderNo","RNo","PID__ProductName","PID__Prices","Quantity","ExtendedPrice"))

        data = dict()
        data['receipt'] = receipt[0]
        data['receiptlineitem'] = receiptlineitem

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'

class ReceiptLineItemForm(forms.ModelForm):
    class Meta:
        model = ReceiptLineItem
        fields = '__all__'
#----------------------------------------------------------------------------------------------
@method_decorator(csrf_exempt, name='dispatch')
class ReceiptCreate(View):
    def post(self, request):
        data = dict()
        request.POST = request.POST.copy()
        if Receipt.objects.count() != 0:
            ReceiptNo_max = Receipt.objects.aggregate(Max('ReceiptNo'))['ReceiptNo__max']
            next_ReceiptNo = ReceiptNo_max[0:3] + str(int(ReceiptNo_max[3:7])+1) + "/" + ReceiptNo_max[8:10]
        else:
            next_ReceiptNo = "RCT1000/20"
        request.POST['ReceiptNo'] = next_ReceiptNo
        request.POST['Date'] = reFormatDateMMDDYYYY(request.POST['Date'])
        request.POST['TotalPrice'] = reFormatNumber(request.POST['TotalPrice'])

        form = ReceiptForm(request.POST)
        if form.is_valid():
            receipt = form.save()

            dict_OrderNo = json.loads(request.POST['OrderNo'])
            for OrderNo in dict_OrderNo['OrderNo']:
                OrderNo['RNo'] = next_ReceiptNo
                OrderNo['PID'] = OrderNo['ProductID']
                OrderNo['Quantity'] = OrderNo['Quantity']
                OrderNo['UnitPrice'] = OrderNo['ProductID__Prices']
                OrderNo['ExtendedPrice'] = reFormatNumber(OrderNo['ExtendedPrice'])

                formlineitem = ReceiptLineItemForm(OrderNo)
                formlineitem.save()

            data['receipt'] = model_to_dict(receipt)
        else:
            data['error'] = 'form not valid!'

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

@method_decorator(csrf_exempt, name='dispatch')
class ReceiptUpdate(View):
    def post(self, request, pk, pk2):
        ReceiptNo = pk + "/" + pk2
        data = dict()
        receipt = Receipt.objects.get(pk=ReceiptNo)
        request.POST = request.POST.copy()
        request.POST['ReceiptNo'] = ReceiptNo
        request.POST['Date'] = reFormatDateMMDDYYYY(request.POST['Date'])
        request.POST['TotalPrice'] = reFormatNumber(request.POST['TotalPrice'])

        form = ReceiptForm(instance=receipt, data=request.POST)
        if form.is_valid():
            receipt = form.save()

            ReceiptLineItem.objects.filter(ReceiptNo=ReceiptNo).delete()

            dict_lineitem = json.loads(request.POST['lineitem'])
            for lineitem in dict_lineitem['lineitem']:
                lineitem['RNo'] = ReceiptNo
                lineitem['PID'] = lineitem['ProductID']
                lineitem['Quantity'] = lineitem['Quantity']
                lineitem['UnitPrice'] = lineitem['UnitPrice']
                lineitem['ExtendPrice'] = reFormatNumber(lineitem['ExtendPrice'])
    
                formlineitem = ReceiptLineItemForm(lineitem)
                formlineitem.save()

            data['receipt'] = model_to_dict(receipt)
        else:
            data['error'] = 'form not valid!'

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

@method_decorator(csrf_exempt, name='dispatch')
class ReceiptDelete(View):
    def post(self, request, pk, pk2):
        ReceiptNo = pk + "/" + pk2
        data = dict()
        receipt = Receipt.objects.get(pk=ReceiptNo)
        if receipt:
            receipt.delete()
            data['message'] = "Receipt Deleted!"
        else:
            data['message'] = "Error!"
        return JsonResponse(data)
    
class ReceiptPDF(View):
    def get(self, request, pk, pk2):
        ReceiptNo = pk + "/" + pk2

        receipt = list(Receipt.objects.select_related("ClubID").filter(RNo=ReceiptNo).values('RNo', 'receipt_date', 'customer_code', 'customer_code__name','payment_method','payment_reference','remarks','total'))
        receiptlineitem = list(ReceiptLineItem.objects.select_related('invoice_no').filter(ReceiptNo=ReceiptNo).order_by('lineitem').values("lineitem","ReceiptNo","invoice_no","invoice_no__date","invoice_no__amount_due","amount_paid_here"))
        #invoicelineitem = InvoiceLineItem.objects.raw(
        #    "SELECT * "
        #    "FROM invoice_line_item LIT "
        #    "  JOIN product P ON LIT.product_code = P.code "
        #    "WHERE LIT.invoice_no = '{}'" .format(invoice_no)
        #)

        #list_lineitem = [] 
        #for lineitem in invoicelineitem:
        #    dict_lineitem = json.loads(str(lineitem))
        #    dict_lineitem['product_name'] = lineitem.product_code.name
        #    dict_lineitem['units'] = lineitem.product_code.units
        #    list_lineitem.append(dict_lineitem)

        data = dict()
        data['receipt'] = receipt[0]
        data['receiptlineitem'] = receiptlineitem
        
        #return JsonResponse(data)
        return render(request, 'receipt/pdf.html', data)
    
class ReceiptReport(View):
    def get(self, request):

        with connection.cursor() as cursor:
            cursor.execute('SELECT r.ReceiptNo as "Receipt No", r.receipt_date as "Receipt Date" '
                           ' , r.customer_code as "Customer Code", c.name as "Customer Name" '
                           ' , r.payment_method as "Payment Method" '
                           ' , r.payment_reference as "Payment Reference", r.remarks as "Remarks" '
                           ' , r.total as "Total Received" '
                           ' FROM receipt r LEFT JOIN customer c '
                           ' ON r.customer_code = c.customer_code '
                           ' ORDER BY r.ReceiptNo ')
           
            row = dictfetchall(cursor)
            column_name = [col[0] for col in cursor.description]
        data = dict()
        data['column_name'] = column_name
        data['data'] = row
        
        
        #return JsonResponse(data)
        return render(request, 'receipt/report.html', data)

#-------------------------------------------------------------------------
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [name[0].replace(" ", "_").lower() for name in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def reFormatDateMMDDYYYY(ddmmyyyy):
        if (ddmmyyyy == ''):
            return ''
        return ddmmyyyy[3:5] + "/" + ddmmyyyy[:2] + "/" + ddmmyyyy[6:]

def reFormatNumber(str):
        if (str == ''):
            return ''
        return str.replace(",", "")