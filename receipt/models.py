from django.db import models

# Create your models here.
class Member(models.Model):
    ClubID = models.CharField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=20, null=True)
    Lastname = models.CharField(max_length=20, null=True)
    PhoneNO = models.CharField(max_length=10, null=True)
    Email = models.CharField(max_length=50, null=True)
    
    class Meta:
        db_table = "MEMBER"
        managed = False
    def __str__(self):
        return self.ClubID

class Shop(models.Model):
    ShopID = models.CharField(max_length=10, primary_key=True)
    Location = models.CharField(max_length=100, null=True,blank=True)

    class Meta:
        db_table = "SHOP"
        managed = False
    def __str__(self):
        return self.ShopID

class Payment(models.Model):
    PaymentCode = models.CharField(max_length=10, primary_key=True)
    PaymentName = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "PAYMENT"
        managed = False
    def __str__(self):
        return self.PaymentCode

class Product(models.Model):
    ProductID = models.CharField(max_length=10, primary_key=True)
    ProductName = models.CharField(max_length=30, null=True)
    Prices = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "PRODUCT"
        managed = False
    def __str__(self):
        return self.ProductID



class Receipt(models.Model):
    ReceiptNo = models.CharField(max_length=10, primary_key=True)
    CRID = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='ClubID')
    Date = models.DateField(null=True, blank=True)
    TotalPrice = models.FloatField(null=True, blank=True)
    PointEarned = models.FloatField(null=True, blank=True)
    PName = models.CharField(max_length=20, null=True)
    SName = models.CharField(max_length=20, null=True)
    ShRID = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column='ShopID')

    class Meta:
        db_table = "RECRIPT"
        managed = False


class ReceiptLineItem(models.Model):
    OrderNo = models.IntegerField()
    RNo = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name = 'invoiceNo', db_column='ReceiptNo')
    PID = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='ProductID')
    Quantity = models.FloatField(null=True)
    ExtendedPrice = models.FloatField(null=True)

    class Meta:
        db_table = "RECEIPT_LINE_ITEM"
        unique_together = (("RNo", "OrderNo"),)
        managed = False

