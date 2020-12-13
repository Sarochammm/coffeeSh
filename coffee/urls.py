from django.contrib import admin
from django.urls import path

from report import views as report_views
from invoice import views as invoice_views
from receipt import views as receipt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', invoice_views.index, name='index'),

    path('report', report_views.index, name='index'),
    path('report/ReportListAllInvoices', report_views.ReportListAllInvoices),
    path('report/ReportProductsSold', report_views.ReportProductsSold),
    path('report/ReportListAllProducts', report_views.ReportListAllProducts),
    path('report/ReportListAllReceipts', report_views.ReportListAllReceipts),
    path('report/ReportUnpaidInvoices', report_views.ReportUnpaidInvoices),

    path('invoice', invoice_views.index, name='index'),
    path('product/list', invoice_views.ProductList.as_view(), name='product_list'),
    path('customer/list', invoice_views.CustomerList.as_view(), name='customer_list'),
    path('customer/detail/<pk>', invoice_views.CustomerDetail.as_view(), name='customer_detail'),
    path('invoice/list', invoice_views.InvoiceList.as_view(), name='invoice_list'),
    path('invoice/detail/<str:pk>/<str:pk2>', invoice_views.InvoiceDetail.as_view(), name='invoice_detail'),
    path('invoice/create', invoice_views.InvoiceCreate.as_view(), name='invoice_create'),
    path('invoice/update/<str:pk>/<str:pk2>', invoice_views.InvoiceUpdate.as_view(), name='invoice_update'),
    path('invoice/delete/<str:pk>/<str:pk2>', invoice_views.InvoiceDelete.as_view(), name='invoice_delete'),
    path('invoice/pdf/<str:pk>/<str:pk2>', invoice_views.InvoicePDF.as_view(), name='invoice_pdf'),
    path('invoice/report', invoice_views.InvoiceReport.as_view(), name='invoice_report'),

    path('receipt', receipt_views.index, name='index'),
    path('receipt/payment/list', receipt_views.PaymenMethodtList.as_view(), name='receipt_payment_list'),
    path('receipt/payment/detail/<pk>', receipt_views.PaymentMethodDetail.as_view(), name='receipt_payment_detail'),
    path('receipt/list', receipt_views.ReceiptList.as_view(), name='receipt_list'),
    path('receipt/detail/<str:pk>/<str:pk2>', receipt_views.ReceiptDetail.as_view(), name='receipt_detail'),
    path('receipt/create', receipt_views.ReceiptCreate.as_view(), name='receipte_create'),
    path('receipt/update/<str:pk>/<str:pk2>', receipt_views.ReceiptUpdate.as_view(), name='receipt_update'),
    path('receipt/delete/<str:pk>/<str:pk2>', receipt_views.ReceiptDelete.as_view(), name='receipt_delete'),
    path('receipt/pdf/<str:pk>/<str:pk2>', receipt_views.ReceiptPDF.as_view(), name='receipt_pdf'),
    path('receipt/report', receipt_views.ReceiptReport.as_view(), name='receipt_report'),



]
