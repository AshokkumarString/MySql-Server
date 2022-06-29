from pickle import TRUE
from pyexpat import model
from turtle import isvisible
from django.db import models
from django.db.backends.utils import truncate_name
from django.db.models.deletion import PROTECT, ProtectedError


class TblClientGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbl_clientgroup'


class TblClient(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    # Field name made lowercase.
    engineer_name = models.CharField( max_length=255, blank=True, null=True)
    emailid = models.CharField(max_length=255, blank=True, null=True)
    # Field name made lowercase.
    phoneno = models.CharField(unique=True, max_length=255, blank=True, null=True)
    clientid = models.CharField(
        unique=True, max_length=255, blank=True, null=True)
    isdeleted = models.CharField(max_length=255, blank=True, null=True)
    clientgroup = models.ForeignKey(
        TblClientGroup, related_name="clientgroup", on_delete=models.PROTECT, blank=True,
        null=True)
    gstnumber = models.CharField(max_length=255, blank=True, null=True)
    pannumber = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbl_client'


class TblCompany(models.Model):
    id = models.AutoField(primary_key=True)
    companyname = models.CharField(max_length=255, blank=True, null=True)
    isactive = models.BooleanField(default=True)
    isvisible = models.BooleanField(default=True)
    isdeleted = models.BooleanField(default=False)
    isgst = models.BooleanField(default=True)
    companycode = models.IntegerField(default=0, null=False)

    class Meta:
        managed = True
        db_table = 'tbl_company'
        
class TblProjects(models.Model):
    id=models.AutoField(primary_key=True)
    clientid=models.CharField(max_length=255,blank=True,null=True)
    clientname=models.CharField(max_length=255,blank=True,null=True)
    subclient=models.CharField(max_length=255,blank=True,null=True)
    phonenumber=models.CharField(max_length=255,blank=True,null=True)
    status=models.CharField(max_length=255,blank=True,null=True)
    company=models.CharField(max_length=255,blank=True,null=True)
    projectname=models.CharField(max_length=255,blank=True,null=True)
    totalamount=models.CharField(max_length=255,blank=True,null=True)
    invoiceid=models.CharField(max_length=255,blank=True,null=True)
    class Meta:
        managed=True,
        db_table="tbl_projects"


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    mailid = models.CharField(unique=True, max_length=255)
    # Field name made lowercase.
    isadmin = models.CharField( max_length=255, blank=True, null=True)
    # Field name made lowercase.
    isapproved = models.CharField(
        max_length=255, blank=True, null=True)
    # Field name made lowercase.
    default_rate = models.CharField(
         max_length=255, blank=True, null=True)
    # Field name made lowercase.
    superuser = models.CharField(
         max_length=255, blank=True, null=True)
    userprofile = models.CharField(max_length=255, blank=True, null=True)
    task=models.CharField(max_length=255, blank=True, null=True)
    admin=models.CharField(max_length=255, blank=True, null=True)
    report=models.CharField(max_length=255, blank=True, null=True)
    invoice=models.CharField(max_length=255, blank=True, null=True)
    inventory=models.CharField(max_length=255, blank=True, null=True)
    sales=models.CharField(max_length=255, blank=True, null=True)
    voucher=models.CharField(max_length=255, blank=True, null=True)
    purchase=models.CharField(max_length=255, blank=True, null=True)
    reload=models.BooleanField(default=False)
    initial=models.CharField(max_length=255,blank=True,null=True)
    colour=models.CharField(max_length=255,blank=True,null=True)
    class Meta:
        managed = True
        db_table = 'users'


class Userdetail(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    fristname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    postalcode = models.CharField(max_length=255, blank=True, null=True)
    aboutme = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'userdetail'


class Plantype(models.Model):
    id = models.AutoField(primary_key=True)
    planname = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'plantype'

class TblWorkTimeTable(models.Model):
    subtaskId = models.IntegerField(primary_key=True)
    date = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    clientName = models.CharField(
         max_length=100, blank=True, null=True)
    maintaskname = models.CharField(
         max_length=100, blank=True, null=True)
    subtaskname = models.CharField(
         max_length=100, blank=True, null=True)
    start_time = models.CharField(max_length=100, blank=True, null=True)
    endtime = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)


class TblStockGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbl_stockgroup'


class TblUnitType(models.Model):
    id = models.AutoField(primary_key=True)
    unitname = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbl_unittype'


class TblStock(models.Model):
    id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    stockname = models.CharField(
         max_length=100, blank=True, null=True)
    productcode = models.CharField(
         max_length=100, blank=True, null=True)
    hsncode = models.CharField(max_length=255, blank=True, null=True)
    length = models.CharField(max_length=100, blank=True, null=True, default=0)
    liquid = models.CharField(max_length=100, blank=True, null=True, default=0)
    # Field name made lowercase.
    defaultrate = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    subunit = models.CharField(max_length=255, blank=True, null=True)
    cgstpercentage = models.CharField(
        max_length=255, blank=True, null=True, default=0)
    sgstpercentage = models.CharField(
        max_length=255, blank=True, null=True, default=0)
    stockgroup = models.ForeignKey(
        TblStockGroup, related_name="stockgroup", on_delete=models.PROTECT, blank=True,
        null=True)

    class Meta:
        managed = True
        db_table = 'tbl_stock'


class TblTaskinvoice(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=100, blank=True, null=True)
    unit = models.CharField(max_length=100, blank=True, null=True)
    rate = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    tasklistrowid = models.ForeignKey(
        'TblTasklist', models.DO_NOTHING, db_column='tasklistrowid')

    class Meta:
        managed = True
        db_table = 'tbl_taskinvoice'


class TblStockinvoice(models.Model):
    id = models.AutoField(primary_key=True)
    types = models.CharField(max_length=100, blank=True, null=True)
    unit = models.CharField(max_length=100, blank=True, null=True)
    rate = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    tasklistrow = models.ForeignKey(
        'TblTasklist', models.DO_NOTHING, db_column='tasklistrow')
    quantity = models.IntegerField(default=1)

    class Meta:
        managed = True
        db_table = 'tbl_stockinvoice'


class TblSales(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    supplier = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    roundoff = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    advancereceived = models.CharField(max_length=100, blank=True, default=0)
    advanceused = models.CharField(max_length=255, blank=True, null=True)
    paymentterms = models.CharField(max_length=255, blank=True, null=True)
    dispatchdate = models.DateField(blank=True, null=True)
    deliveryaddress = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True,
        db_table = 'tbl_sales'

class TblTasklist(models.Model):  # to create card table
    id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    date = models.CharField(max_length=100, blank=True, null=True)
    # Field name made lowercase.
    task = models.CharField(max_length=100, blank=True, null=True)
    # Field name made lowercase.
    assignto = models.CharField(max_length=100, blank=True, null=True)
    # Field name made lowercase.
    priority = models.CharField(max_length=100, blank=True, null=True)
    # Field name made lowercase.
    startdate = models.CharField(max_length=100, blank=True, null=True)
    # Field name made lowercase.
    enddate = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    isdeleted = models.CharField(max_length=255, blank=True, null=True)
    plantype = models.CharField(max_length=255, blank=True, null=True)
    client = models.ForeignKey(
        TblClient, related_name="client_id", on_delete=models.PROTECT)
    subclient = models.CharField(max_length=255, blank=True, null=True)
    task_starttime = models.CharField(max_length=255, blank=True, null=True)
    clientname = models.CharField(max_length=255, blank=True, null=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)
    completed_date = models.CharField(max_length=255, blank=True, null=True)
    advanceamount = models.CharField(max_length=255, blank=True, null=True)
    phonenumber = models.CharField(max_length=255, blank=True, null=True)
    # Field name made lowercase.
    drawingtitle = models.CharField(max_length=255, blank=True, null=True)
    parenttaskid = models.CharField(max_length=255, blank=True, null=True)
    parenttaskbalance = models.IntegerField(default=0)
    projectname=models.CharField(max_length=255, blank=True, null=True)
    totalamount=models.CharField(max_length=255, blank=True, null=True)
    taskproject = models.ForeignKey(
         TblProjects, related_name="taskproject", on_delete=PROTECT, blank=True, null=True)
    company = models.ForeignKey(
        TblCompany, related_name="company", on_delete=models.PROTECT)
    companyname = models.CharField(max_length=255, blank=True, null=True)
    invoiceidno=models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return "TblTasklist : {}".format(self.id)

    class Meta:
        managed = True
        db_table = 'tbl_tasklist'

class TblSubtask(models.Model):
    id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    date = models.CharField(max_length=100, blank=True, null=True)
    # Field name made lowercase.
    subtask = models.CharField( max_length=100, blank=True, null=True)
    # Field name made lowercase.
    assignto = models.CharField(max_length=100, blank=True, null=True)
    # Field name made lowercase.
    priority = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    isdeleted = models.CharField(max_length=255, blank=True, null=True)
    completed_date = models.CharField(max_length=255, blank=True, null=True)
    task_starttime = models.CharField(max_length=255, blank=True, null=True)
    tasklist = models.ForeignKey(
        TblTasklist, related_name="subtask", on_delete=models.PROTECT)

    def __str__(self):
        return "TblSubtask : {}".format(self.id)

    class Meta:
        managed = True
        db_table = 'tbl_subtask'

class TblSubtasktime(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    endtime = models.CharField(max_length=255, blank=True, null=True)
    subtask = models.ForeignKey(
        TblSubtask, related_name="subtaskTime", on_delete=models.PROTECT)
    start_time = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):

        return "TblSubtasktime : {}".format(self.id)

    class Meta:
        managed = True
        db_table = 'tbl_subtasktime'

class TblInvoicesummary(models.Model):
    id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    date = models.CharField(max_length=100, blank=True, null=True)
    # Field name made lowercase.
    # client = models.CharField(max_length=100, blank=True, null=True)
    invoicesummaryclient = models.ForeignKey(
        TblClient, related_name="invoicesummaryclient", blank=True, null=True, on_delete=models.PROTECT)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    invoice_amount = models.CharField(max_length=255, blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    amount_received = models.CharField( max_length=255, blank=True, null=True)
    # Field name made lowercase.
    invoicestatus = models.CharField(max_length=255, blank=True, null=True)
    discount = models.CharField(max_length=255, blank=True, null=True)
    subtotal = models.CharField(max_length=255, blank=True, null=True)
    balancedue = models.CharField(max_length=255, blank=True, null=True)
    duedate = models.CharField(max_length=255, blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    originaldeliverynoteid = models.IntegerField(default=0, null=False)
    originalcompanyid = models.IntegerField(default=0, null=False)
    ismoved = models.BooleanField(default=False)
    deliverynoteid = models.IntegerField(blank=True, null=True)
    vehiclenumber = models.CharField(max_length=255, blank=True, null=True)
    invoicetype = models.CharField(max_length=255, blank=True, null=True)
    salesorder = models.ForeignKey(
        TblSales, related_name="salesorder", blank=True, null=True, on_delete=PROTECT)
    # companyid = models.CharField(
    #     max_length=255, blank=True, null=True, default="1")
    tbltasklist = models.ForeignKey(
        TblTasklist, related_name="tbltasklist",blank=True, null=True, on_delete=models.PROTECT)
    companyinvoiceid = models.IntegerField(null=True,)
    clientgroupid = models.ForeignKey(
        TblClientGroup, related_name="clientgroupid", on_delete=PROTECT, blank=True, null=True)
    project = models.ForeignKey(
        TblProjects, related_name="project",blank=True, null=True, on_delete=models.PROTECT)
    invoice_company=models.ForeignKey(
        TblCompany, related_name="invoice_company",blank=True, null=True, on_delete=models.PROTECT)
    class Meta:
        managed = True  
        db_table = 'tbl_invoicesummary'


class TblVouchermanagement(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    username = models.CharField(max_length=250, blank=True, null=True)
    clientname = models.CharField(max_length=250, blank=True, null=True)
    client = models.ForeignKey(
        TblClient, related_name="client", blank=True, null=True, on_delete=models.PROTECT)
    vouchertype = models.CharField(max_length=255, blank=True, null=True)
    vouchersubtype = models.CharField(max_length=255, blank=True, null=True)
    vouchersubreferencetype = models.CharField(
        max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    paymentmode = models.CharField(max_length=250, blank=True, null=True)
    companyname = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True,
        db_table = 'tbl_vouchermanagement'


class TblTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    transactiontask = models.ForeignKey(
        TblTasklist, related_name="transactiontask",blank=True, null=True, on_delete=models.PROTECT)
    date = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    # taskid=models.CharField(max_length=100, blank=True, null=True)
    # clientid = models.ForeignKey(
    #     TblClient, models.DO_NOTHING, db_column='clientid')
    transaction_client = models.ForeignKey(
        TblClient, related_name="transaction_client",blank=True, null=True, on_delete=models.PROTECT)
    # transactionclient = models.ForeignKey(
    #     TblClient, related_name="transactionclient",blank=True, null=True, on_delete=models.PROTECT)
    userid = models.ForeignKey(Users, related_name="userid",on_delete=models.CASCADE)
    deliverynoteid = models.CharField(max_length=100, blank=True, null=True)
    # Field name made lowercase.
    originaldeliverynoteid = models.IntegerField(default=0, null=False)
    originalcompanyid = models.IntegerField(default=0, null=False)
    pmtmode = models.CharField(max_length=250, blank=True, null=True)
    pmtreference = models.CharField(max_length=250, blank=True, null=True)
    salesorderid = models.CharField(max_length=255, blank=True, null=True)
    # companyidnum = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(
         max_length=255, blank=True, null=True)
    transactiontype = models.CharField(max_length=250, blank=True, null=True)
    voucher = models.ForeignKey(
        TblVouchermanagement, related_name='voucher', blank=True, null=True,on_delete=models.CASCADE)
    vouchertype = models.CharField(max_length=255, blank=True, null=True)
    voucherreferencetype = models.CharField(
        max_length=255, blank=True, null=True)
    client_groupid = models.ForeignKey( 
        TblClientGroup, related_name="client_groupid", on_delete=PROTECT, blank=True, null=True)
    company_id=models.ForeignKey(
        TblCompany, related_name="company_id", on_delete=PROTECT, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbl_transaction'


class TblSubclient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        db_column='name', max_length=100, blank=True, null=True)
    phoneno = models.CharField( max_length=100, blank=True, null=True)
    clients = models.ForeignKey(
        TblClient, related_name="clients", on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'tbl_subclient'


class TblTaxyear(models.Model):
    id = models.AutoField(primary_key=True)
    taxyear = models.CharField(max_length=100, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbl_taxyear'

class TblBank(models.Model):
    id = models.AutoField(primary_key=True)
    bankname = models.CharField(max_length=100, blank=True, null=True)
    accountno = models.CharField(max_length=100, blank=True, null=True)
    upi = models.CharField(max_length=100, blank=True, null=True)
    comments = models.CharField(max_length=100, blank=True, null=True)
    ifsc = models.CharField(max_length=100, blank=True, null=True)
    companydetails = models.ForeignKey(
        TblCompany, related_name="companydetails_id", on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'tbl_bank'


# Inventory Tables

class TblPurchaseorder(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    companyid = models.CharField(max_length=100, blank=True, null=True)
    total = models.CharField(max_length=100, blank=True, null=True)
    supplier = models.CharField(max_length=100, blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    payment = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    roundoff = models.CharField(max_length=100, blank=True, null=True)
    isdeleted = models.BooleanField(default=False)
    advancepaid = models.CharField(max_length=100, blank=True, default=0)
    advanceused = models.CharField(max_length=255, blank=True, null=True)
    deliverydate = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbl_purchaseorder'


class TblPurchasestocks(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    productcode = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    rate = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    cgstdiscount = models.CharField(max_length=100, blank=True, null=True)
    sgstdiscount = models.CharField(max_length=100, blank=True, null=True)
    cgstdiscountpercentage = models.CharField(
        max_length=100, blank=True, null=True)
    sgstdiscountpercentage = models.CharField(
        max_length=100, blank=True, null=True)
    gsttype = models.CharField(max_length=250, blank=True, null=True)
    total = models.CharField(max_length=100, blank=True, null=True)
    isdeleted = models.BooleanField(default=False)
    status = models.CharField(max_length=100, blank=True, null=True)
    received = models.CharField(
        max_length=100, blank=True, null=True, default=0)
    remaining = models.CharField(max_length=100, blank=True, null=True)
    invoiceno = models.CharField(max_length=100, blank=True, null=True)
    hsncode = models.CharField(max_length=100, blank=True, null=True)
    purchasesorderid = models.ForeignKey(
        TblPurchaseorder, related_name="purchasestock", on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'tbl_purchasestocks'


class TblPurchaseUserrequest(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    stockname = models.CharField(max_length=100, blank=True, null=True)
    productcode = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    purchaseorderid = models.CharField(max_length=100, blank=True, null=True)
    isdeleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'tbl_purchase_userrequest'


class TblPurchasebillinvoice(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    purchaseinvoiceno = models.CharField(max_length=255, blank=True, null=True)
    supplier = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    roundoff = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    amountreceived = models.CharField(max_length=255, blank=True, null=True)
    invoicedate = models.DateField(blank=True, null=True)

    class Meta:
        managed = True,
        db_table = 'tbl_purchasebillinvoice'


class TblPurchasebillstocks(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    stockname = models.CharField(max_length=100, blank=True, null=True)
    productcode = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    received = models.CharField(max_length=100, blank=True, null=False)
    status = models.CharField(max_length=100, blank=True, null=True)
    purchaseorderid = models.CharField(max_length=255, blank=True, null=True)
    # length = models.CharField(max_length=255, blank=True, null=True, default=0)
    rate = models.IntegerField(blank=True, default=0)
    amount = models.IntegerField(blank=True, default=0)
    cgstpercentage = models.CharField(max_length=100, blank=True, default=0)
    sgstpercentage = models.CharField(max_length=100, blank=True, default=0)
    total = models.IntegerField(blank=True, default=0)
    # batch = models.IntegerField(blank=True, default=0)
    isdeleted = models.BooleanField(default=False)
    invoiceno = models.CharField(max_length=255, blank=True, default=0)
    # location = models.CharField(
    # max_length=255, blank=True, null=True, default=0)
    bill = models.ForeignKey(
        TblPurchasebillinvoice, related_name="bill", on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'tbl_purchasebillstocks'


class TblInventorytransaction(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    stockname = models.CharField(max_length=100, blank=True, null=True)
    productcode = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    invoiceno = models.CharField(max_length=100, blank=True, null=True)
    purchaseorderid = models.CharField(max_length=100, blank=True, null=True)
    length = models.CharField(max_length=255, blank=True, null=True, default=0)
    rate = models.FloatField(blank=True, default=0)
    amount = models.FloatField(blank=True, default=0)
    cgstpercentage = models.CharField(max_length=100, blank=True, default=0)
    sgstpercentage = models.CharField(max_length=100, blank=True, default=0)
    total = models.FloatField(blank=True, default=0)
    batch = models.CharField(max_length=255, blank=True, default=0)
    comments = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(
        max_length=255, blank=True, null=True, default=0)
    salesid = models.CharField(max_length=255, blank=True, null=True)
    hsncode = models.CharField(max_length=100, blank=True, null=True)
    purchaseinvoice = models.ForeignKey(
        TblPurchasebillinvoice, related_name="purchaseinvoice", blank=True, null=True, on_delete=models.PROTECT)
    companyid = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True,
        db_table = 'tbl_inventorytransaction'


class TblBatch(models.Model):
    id = models.AutoField(primary_key=True)
    batchno = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True,
        db_table = 'tbl_batch'


class TblLocation(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    shortlocation = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    godown = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True,
        db_table = 'tbl_location'


class TblSalestransaction(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    stockname = models.CharField(max_length=100, blank=True, null=True)
    productcode = models.CharField(max_length=100, blank=True, null=True) 
    quantity = models.CharField(max_length=100, blank=True, null=True)
    usedqty = models.CharField(max_length=255, blank=True, default=0)
    status = models.CharField(max_length=100, blank=True, null=True)
    rate = models.IntegerField(blank=True, default=0)
    amount = models.IntegerField(blank=True, default=0)
    cgstpercentage = models.CharField(max_length=100, blank=True, default=0)
    sgstpercentage = models.CharField(max_length=100, blank=True, default=0)
    total = models.IntegerField(blank=True, default=0)
    isdeleted = models.BooleanField(default=False)
    hsncode = models.CharField(max_length=100, blank=True, null=True)
    sales = models.ForeignKey(
        TblSales, related_name="sales", blank=True, null=True, on_delete=models.PROTECT)
    task_invoiceno = models.ForeignKey(
        TblInvoicesummary, related_name="task_invoiceno", blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        managed = True,
        db_table = 'tbl_salestransaction'


class TblExpenses(models.Model):
    id = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=255, blank=True, null=True)
    purchasefrom = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    paid = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    purchaseexpense = models.ForeignKey(
        TblPurchasebillinvoice, related_name="purchaseexpense", blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        managed = True,
        db_table = 'tbl_expenses'


class TblSalesrequest(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    stockname = models.CharField(max_length=100, blank=True, null=True)
    productcode = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    salesid = models.CharField(max_length=100, blank=True, null=True)
    isdeleted = models.BooleanField(default=False)
    companyid = models.CharField(max_length=255, blank=True, null=True)
    clientid = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True,
        db_table = 'tbl_salesrequest'


class TblVoucherdetails(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    vouchermanagement = models.ForeignKey(
        TblVouchermanagement, related_name="vouchermanagement", blank=True, null=True, on_delete=PROTECT)
    vouchertype = models.CharField(max_length=255, blank=True, null=True)
    voucherreferencetype = models.CharField(
        max_length=255, blank=True, null=True)

    class Meta:
        managed = True,
        db_table = 'tbl_voucherdetails'


class TblLedgergroups(models.Model):
    id = models.AutoField(primary_key=True)
    ledgergroupname = models.CharField(max_length=255, blank=True, null=True)
    isvisible = models.BooleanField(default=False)
    isdeleted = models.BooleanField(default=False)

    class Meta:
        managed = True,
        db_table = 'tbl_ledgergroup'


class TblLedgertypes(models.Model):
    id = models.AutoField(primary_key=True)
    ledgertypename = models.CharField(max_length=255, blank=True, null=True)
    ledgertypegroup = models.ForeignKey(
        TblLedgergroups, related_name="ledgertypegroup", on_delete=PROTECT, blank=True, null=True)
    isvisible = models.BooleanField(default=False)

    class Meta:
        managed = True,
        db_table = 'tbl_ledgertype'


class TblQuotationrequest(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    supplier = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    roundoff = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    advancereceived = models.CharField(max_length=100, blank=True, default=0)
    advanceused = models.CharField(max_length=255, blank=True, null=True)
    paymentterms = models.CharField(max_length=255, blank=True, null=True)
    dispatchdate = models.DateField(blank=True, null=True)
    salesorderid = models.CharField(max_length=255, blank=True, null=True)
    users = models.CharField(max_length=255, blank=True, null=True)
    phoneno = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True,
        db_table = 'tbl_quotationrequest'


class TblQuotationtransaction(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    stockname = models.CharField(max_length=100, blank=True, null=True)
    productcode = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    usedqty = models.CharField(max_length=255, blank=True, default=0)
    status = models.CharField(max_length=100, blank=True, null=True)
    rate = models.IntegerField(blank=True, default=0)
    amount = models.IntegerField(blank=True, default=0)
    cgstpercentage = models.CharField(max_length=100, blank=True, default=0)
    sgstpercentage = models.CharField(max_length=100, blank=True, default=0)
    total = models.IntegerField(blank=True, default=0)
    isdeleted = models.BooleanField(default=False)
    hsncode = models.CharField(max_length=100, blank=True, null=True)
    salesquotation = models.ForeignKey(
        TblQuotationrequest, related_name="salesquotation", blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        managed = True,
        db_table = 'tbl_quotationtransaction'



        



