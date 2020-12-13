CREATE TABLE "PAYMENT"(
    "PaymentCode" varchar(10) NOT NULL,
    "PaymenttName" varchar(20) NOT NULL,
    PRIMARY KEY ("PaymentCode")
    
);

CREATE TABLE "SHOP"(
    "ShopID" varchar(10) NOT NULL,
    "Location" varchar(100) NOT NULL,
    PRIMARY KEY ("ShopID")
    
);

CREATE TABLE "SALES_PERSON"(
    "UserID" varchar(10) NOT NULL,
    "SaleName" varchar(20) NOT NULL,
    PRIMARY KEY ("UserID")
    
);

CREATE TABLE "WORKS_ON"(
    "ShID" varchar(10) NOT NULL,
    "UID" varchar(10) NOT NULL,
    PRIMARY KEY ("UID","ShID"),
    FOREIGN KEY ("ShID") REFERENCES "SHOP"("ShopID"),
    FOREIGN KEY ("UID") REFERENCES "SALES_PERSON"("UserID")

);

CREATE TABLE "PRODUCT"(
    "ProductID" varchar(10) NOT NULL,
    "ProductName" varchar(30) NOT NULL,
    "Prices" numeric(18,2),
    PRIMARY KEY ("ProductID")
    
);

CREATE TABLE "MEMBER"(
    "ClubID" varchar(10) NOT NULL,
    "Name" varchar(20) NOT NULL,
    "Lastname" varchar(20) NOT NULL,
    "PhoneNO" char(10) NOT NULL,
    "Email" varchar(50) NOT NULL,
    PRIMARY KEY ("ClubID")
);

CREATE TABLE "MEMBER_CARD"(
    "ClubID_card" varchar(10) NOT NULL,
    "CStart" date,
    "CDue" date,
    PRIMARY KEY ("ClubID_card"),
    FOREIGN KEY ("ClubID_card") REFERENCES "MEMBER" ("ClubID")
);

CREATE TABLE "MEMBER_POINT"(
    "ClubID_point" varchar(10) NOT NULL,
    "TotalPoint" int NOT NULL,
    PRIMARY KEY ("ClubID_point"),
    FOREIGN KEY ("ClubID_point") REFERENCES "MEMBER"("ClubID")
);

CREATE TABLE "RECEIPT"(
    "ReceiptNo" varchar(10) NOT NULL,
    "CRID" varchar(10) NOT NULL,
    "CustomerName" varchar(20) NOT NULL,
	"Date" date,
	"TotalPrice" numeric (18,2) NOT NULL,
	"ClubID" numeric (18,2) NOT NULL,
	"PointEarned" int NOT NULL,
	"PName" varchar(20) NOT NULL,
	"SName" varchar(20) NOT NULL,
	"ShRID" varchar(10) NOT NULL,
    PRIMARY KEY ("ReceiptNo"),
    FOREIGN KEY ("CRID") REFERENCES "MEMBER"("ClubID"),
    FOREIGN KEY ("ShRID") REFERENCES "SHOP"("ShopID")
);

CREATE TABLE "RECEIPT_LINE_ITEM"(
    "RNo" varchar(10) NOT NULL,
    "OrderNo" int NOT NULL,
    "PID" varchar(10) NOT NULL,
	"UnitPrice" numeric(18,2) NOT NULL,
	"Quantity" int NOT NULL,
	PRIMARY KEY ("RNo","OrderNo"),
    FOREIGN KEY ("RNo") REFERENCES "RECEIPT"("ReceiptNo"),
    FOREIGN KEY ("PID") REFERENCES "PRODUCT"("ProductID")
);

CREATE TABLE "POINTS"(
    "ReceiptNum" varchar(10) NOT NULL,
    "CPID " varchar(10) NOT NULL,
    "Point" int NOT NULL,
	"PStart" date,
	"PDue" date,
    PRIMARY KEY ("ReceiptNum"),
    FOREIGN KEY ("CPID ") REFERENCES "MEMBER"("ClubID"),
    FOREIGN KEY ("ReceiptNum") REFERENCES "RECEIPT"("ReceiptNo")
);







