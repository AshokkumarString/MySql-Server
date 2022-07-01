from pyexpat import model
from traceback import print_tb
from rest_framework import status
from django.db.models import Max, Min, Sum, Q
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from TeamTask import models
from TeamTask import serialization
from datetime import date
from django.db.models import Count
from django.http import JsonResponse
from rest_framework.decorators import api_view
# from dateutil.relativedelta import relativedelta
from TeamTask.models import TblInvoicesummary, TblTasklist
from rest_framework import serializers
from django.core.serializers import serialize
#from dateutil.relativedelta import relativedelta
from TeamTask.models import TblInvoicesummary, TblTransaction
from rest_framework import status


class sp_makeInvoice(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = serialization.seralizationTblInvoicesummary

    def post(self, request):
        try:
            res = TblInvoicesummary.objects.filter(invoice_company=request.data['companyid']).aggregate(
                max_id=Max('companyinvoiceid'))
            invoiceid = TblInvoicesummary.objects.filter(
                deliverynoteid=request.data['deliverynoteid'],invoice_company=request.data['companyid']).values() 
            maxid = res['max_id']
            updateinvoicesummary = {
                "companyinvoiceid": maxid + 1,
                "tbltasklistid": invoiceid[0]['tbltasklist_id'],
                "projectid": invoiceid[0]['project_id'],
                "invoicesummaryclientid":invoiceid[0]['invoicesummaryclient_id'],
                "invoice_companyid":invoiceid[0]['invoice_company_id']
            }
            serializer = serialization.seralizationTblInvoicesummary(
                models.TblInvoicesummary.objects.get(pk=invoiceid[0]['id']), updateinvoicesummary)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.errors)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)


class sp_createinvocieandtransaction(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = serialization.seralizationTblInvoicesummary

    def post(self, request):
        try:
            returndata = [
                {
                    "alearyinvoice": "No",
                    "invoiceid": "No"
                }
            ]
            clientgroupid = models.TblClient.objects.filter(
                id=request.data['client']).values('clientgroup')
            alreadyinvoicecreated = models.TblInvoicesummary.objects.filter(tbltasklist=request.data['taskid'],
                                                                            invoicestatus__in=[
                                                                                'Unpaid', 'Partially Paid', 'Paid'],
                                                                            invoicesummaryclient=request.data['client'], invoice_company=request.data['companyid']).values('id')
            if len(alreadyinvoicecreated) > 0:
                returndata[0]['alearyinvoice'] = "Already Invoice created for this Task"
                return Response(returndata)
            else:
                if request.data['client'] == 110 or request.data['client'] == 182:
                    advanceamount = models.TblTasklist.objects.filter(
                        id=request.data['taskid']).values('advanceamount')
                    receivedamountTotal = int(
                        advanceamount[0]['advanceamount']) + int(request.data['amount_received'])
                else:
                    receivedamountTotal = int(request.data['amount_received'])
                if receivedamountTotal > 0:
                    self.create_transactionforreceivedamount(
                        request.data, receivedamountTotal) 

                if int(request.data['invoice_amount']) > 0:
                    currentdate = datetime.today().strftime('%Y-%m-%d')
                    three_months = date.today()
                    res = TblInvoicesummary.objects.filter(invoice_company=request.data['companyid']).aggregate(
                        max_id=Max('deliverynoteid'))
                    maxid=0
                    print(res['max_id'])
                    if res['max_id'] == None:
                        maxid = 9999
                    else:
                        maxid = res['max_id']
                    returndata[0]['invoiceid'] = maxid+1
                    print( maxid+1)
                    invoice_dict = {
                        "tbltasklistid": request.data['taskid'],
                        "projectid": None,
                        "task_invoiceno": "",
                        "date": currentdate,
                        "invoicesummaryclientid": request.data['client'],
                        "invoice_amount": request.data['invoice_amount'],
                        "amount_received": 0,
                        "invoicestatus": "Unpaid",
                        "discount": request.data['discount'],
                        "subtotal": request.data['subtotal'],
                        "balancedue": request.data['invoice_amount'],
                        "duedate": str(three_months),
                        "comments": "",
                        "originaldeliverynoteid": 0,
                        "originalcompanyid": 0,
                        "deliverynoteid": maxid+1,
                        "invoice_companyid": request.data['companyid'],
                        "salesorder": "",
                        "tbltasklist": "",
                        "clientgroupid": clientgroupid,
                        "project": None
                    }
                    serializerinvoicesummary = serialization.seralizationTblInvoicesummary(
                        data=invoice_dict)
                    if serializerinvoicesummary.is_valid():
                        serializerinvoicesummary.save()
                    else:
                        raise ValueError(serializerinvoicesummary.errors,"0st Exception")
                    self.create_transaction(request.data,maxid)
                    my_dict = {
                        'status': 'Completed',
                        'client': request.data['client'],
                        'taskproject': "",
                        'company': request.data['companyid'],
                        'invoiceidno': ""
                    }
                    responsedetails = serialization.SerializationTaskList(
                        models.TblTasklist.objects.get(pk=request.data['taskid']), data=my_dict)
                    if responsedetails.is_valid():
                        responsedetails.save()
                        
            return Response(returndata)
        except Exception as ex:
            return Response(str(ex))

    def create_transaction(self, data,deliverynoteid):
        currentdate = datetime.today().strftime('%Y-%m-%d')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        transaction_dict = {
            "transactiontaskid": data['taskid'],
            "date": currentdate,
            "time": current_time,
            "amount": data['invoice_amount'],
            "deliverynoteid": deliverynoteid+1,
            "originaldeliverynoteid": 0,
            "originalcompanyid": 0,
            "salesorderid": None,
            "transactiontype": "invoice",
            "companyid": data['companyid'],
            "transaction_clientid": data['client'],
            "userid_id": data['userid'],
            "voucherid":""
        }
        serializer = serialization.SerializationTransaction(
            data=transaction_dict)
        if serializer.is_valid():
            serializer.save()
        else:
           raise ValueError(serializer.errors,"1st Exception")

    def create_transactionforreceivedamount(self, data, receivedamountTotal):
        currentdate = datetime.today().strftime('%Y-%m-%d')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if receivedamountTotal > 0:
            transaction_dict = {
                "transactiontaskid": data['taskid'],
                "date": currentdate,
                "time": current_time,
                "amount": receivedamountTotal,
                "deliverynoteid": "",
                "originaldeliverynoteid": 0,
                "originalcompanyid": 0,
                "salesorderid": None,
                "transactiontype": "Received",
                "companyid": data['companyid'],
                "transaction_clientid": data['client'],
                "userid_id": data['userid'],
                 "voucherid":""
            }
            serializer = serialization.SerializationTransaction(
                data=transaction_dict)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError(serializer.errors,"2nd Exception")


class sp_getcompanygreaterinvoice(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = serialization.seralizationTblInvoicesummary

    def post(self, request):
        res = TblInvoicesummary.objects.filter(
            invoice_company=request.data['companyid']).aggregate(max_id=Max('deliverynoteid'))
        return Response(res['max_id'])


class sp_cancelinvoice(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = serialization.seralizationTblInvoicesummary

    def put(self, request):
        try:
            queryset = models.TblInvoicesummary.objects.filter(
                deliverynoteid=request.data['deliverynoteid'], invoice_company=request.data['companyid']).values()
            print(queryset[0])
            updateinvoicesummary = {
                "invoicesummaryclientid":queryset[0]['invoicesummaryclient_id'],
                "invoice_companyid":queryset[0]['invoice_company_id'],
                "companyinvoiceid": queryset[0]['companyinvoiceid'],
                "invoicestatus": "Cancelled",
                "tbltasklistid": queryset[0]['tbltasklist_id'],
                "projectid": queryset[0]['project_id']
            }
            serializer = serialization.seralizationTblInvoicesummary(
                models.TblInvoicesummary.objects.get(pk=queryset[0]['id']), updateinvoicesummary)
            if serializer.is_valid():
                serializer.save()
                if queryset[0]['tbltasklist_id'] != None:
                    self.update_tasklist(queryset[0])
            else:
                raise ValueError("invociesummary failed",serializer.errors)
            self.update_inventorytransaction(
                request.data['deliverynoteid'], request.data['usercomments'])
            return Response(request.data)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    def update_inventorytransaction(self, deliverynoteid, usercomments):
        inventorydata = models.TblInventorytransaction.objects.filter(
            invoiceno=deliverynoteid).values()
        for data in inventorydata:
            inventoryupdate_dict = {
                "quantity": "0",
                "rate": "0",
                "amount": "0",
                "total": "0",
                "comments": usercomments
            }
            serializationinventory = serialization.SerializationInventorytransaction(
                models.TblInventorytransaction.objects.get(pk=data['id']), inventoryupdate_dict)
            if serializationinventory.is_valid():
                serializationinventory.save()
            else:
                raise ValueError("responsetransaction failed",
                                     serializationinventory.errors)

    def update_tasklist(self, data):
        maintaskdetails = models.TblTasklist.objects.filter(
            id=data['tbltasklist_id']).values()
        updatemaintask_dict = {
            "status": "ReadyToBill",
            "client": maintaskdetails[0]['client_id'],
            "taskproject": maintaskdetails[0]['taskproject_id'],
            "company": maintaskdetails[0]['company_id']
        }
        serializer = serialization.SerializationTaskList(
            models.TblTasklist.objects.get(pk=data['tbltasklist_id']), updatemaintask_dict)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError("responsetransaction failed",
                                     serializer.errors)


class sp_payforcurrentinvoicetask(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = serialization.seralizationTblInvoicesummary

    def post(self, request):
        invoicedetails = models.TblInvoicesummary.objects.filter(
            tbltasklist_id=request.data['tbltasklist_id'], invoice_company=request.data['companyid']).values()
        balancedueamount = int(
            invoicedetails[0]['balancedue'])-int(request.data['amount'])
        if int(request.data['amount']) >= int(invoicedetails[0]['balancedue']) and int(invoicedetails[0]['balancedue']) > 0:
            updateinvoicesummary = {
                "tbltasklistid": invoicedetails[0]['tbltasklist_id'],
                "projectid": invoicedetails[0]['project_id'],
                "invoicestatus": "Paid",
                "amount_received": int(request.data['amount']),
                "balancedue": balancedueamount,
                "invoicesummaryclientid":invoicedetails[0]['invoicesummaryclient_id'],
                "invoice_companyid":invoicedetails[0]['invoice_company_id']
            }
            update_invoicesummary = serialization.seralizationTblInvoicesummary(
                models.TblInvoicesummary.objects.get(pk=invoicedetails[0]["id"]), updateinvoicesummary)
            if update_invoicesummary.is_valid():
                update_invoicesummary.save()
                self.write_transactionfor_received_amount(
                    request.data, invoicedetails[0])
                Response(update_invoicesummary.data)
        else:
            updateinvoicesummary = {
                "tbltasklistid": invoicedetails[0]['tbltasklist_id'],
                "projectid": invoicedetails[0]['project_id'],
                "invoicestatus": "Partially Paid",
                "amount_received": int(request.data['amount']),
                "balancedue": balancedueamount,
                "invoicesummaryclientid":invoicedetails[0]['invoicesummaryclient_id'],
                "invoice_companyid":invoicedetails[0]['invoice_company_id']
            }
            update_invoicesummary = serialization.seralizationTblInvoicesummary(
                models.TblInvoicesummary.objects.get(pk=invoicedetails[0]["id"]), updateinvoicesummary)
            if update_invoicesummary.is_valid():
                update_invoicesummary.save()
                self.write_transactionfor_received_amount(
                    request.data, invoicedetails[0])
        return Response(request.data)

    def write_transactionfor_received_amount(self, userinput, Invoicedata):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        currentdate = datetime.today().strftime('%Y-%m-%d')
        transaction_dict = {
            "transactiontaskid": Invoicedata['tbltasklist_id'],
            "date": currentdate,
            "time": current_time,
            "amount": userinput['amount'],
            "deliverynoteid": Invoicedata['deliverynoteid'],
            "originaldeliverynoteid": 0,
            "originalcompanyid": 0,
            "salesorderid": Invoicedata['salesorder_id'],
            "transactiontype": "Spend",
            "companyid": Invoicedata['invoice_company_id'],
            "transaction_clientid": Invoicedata['invoicesummaryclient_id'],
            "userid_id": userinput['userid'],
             "voucherid":""
        }
        create_transaction = serialization.SerializationTransaction(
            data=transaction_dict)
        if create_transaction.is_valid():
            create_transaction.save()
        return Response(create_transaction.errors)


class sp_updatecurrentinvoice(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = serialization.seralizationTblInvoicesummary

    def put(self, request):
        try:
            invoicesummaryquaryset = models.TblInvoicesummary.objects.filter(
                id=request.data['invoiceidno']).values()
            print(invoicesummaryquaryset)
            updateinvoicesummary = {
                "invoicesummaryclientid":invoicesummaryquaryset[0]['invoicesummaryclient_id'],
                "tbltasklistid": invoicesummaryquaryset[0]['tbltasklist_id'],
                "projectid": invoicesummaryquaryset[0]['project_id'],
                "invoicestatus": request.data['invoicestatus'],
                "amount_received": request.data['amount_received'],
                "balancedue": request.data['balancedue'],
                "invoice_companyid":invoicesummaryquaryset[0]['invoice_company_id']
            }
            response = serialization.seralizationTblInvoicesummary(models.TblInvoicesummary.objects.get(
                pk=invoicesummaryquaryset[0]['id']), data=updateinvoicesummary)
            if response.is_valid():
                response.save()
            return Response(response.errors)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT'])
def getinvoicewithfilterdata(request):
    status = request.GET['status'].split(",")
    startdate = request.GET['startdate']
    enddate = request.GET['enddate']
    companydetailsid = request.GET['company_id'].split(",")
    clientgroupdetails = request.GET['groupid'].split(",")
    clientid = request.GET['clientid']
    today = date.today()
    clientgroup = 'NoClientGroupid'
    print(enddate)
    enddatedetails = today if enddate == '2019-01-01' else enddate
    Totaldata=[]
    Return_data=[]
    if clientid == "allclient":
        if clientgroupdetails[0] == clientgroup:
            print("data 1",enddatedetails)
            Totaldata =TblInvoicesummary.objects.filter(invoicestatus__in=status,date__gte=startdate,date__lte=enddatedetails,invoice_company__in=companydetailsid).select_related('invoicesummaryclient','tbltasklist','invoice_company').all()
             
        else:
            print("data 2")
            Totaldata = TblInvoicesummary.objects.filter(invoicestatus__in=status, date__gte=startdate, date__lte=enddatedetails,
                                                        invoice_company__in=companydetailsid, clientgroupid_id__in=clientgroupdetails).select_related('invoicesummaryclient','tbltasklist','invoice_company').all()
    else:
        if clientgroupdetails[0] == clientgroup:
            print("data 3")
            Totaldata = TblInvoicesummary.objects.filter(
                invoicestatus__in=status, date__gte=startdate, date__lte=enddatedetails, invoice_company__in=companydetailsid, invoicesummaryclient=clientid).select_related('invoicesummaryclient','tbltasklist','invoice_company').select_related('invoicesummaryclient','tbltasklist','invoice_company').all()
           

        else:
            print("data 4")
            Totaldata = TblInvoicesummary.objects.filter(invoicestatus__in=status, date__gte=startdate, date__lte=enddatedetails,
                                                         invoice_company__in=companydetailsid, clientgroupid_id__in=clientgroupdetails, invoicesummaryclient=clientid).select_related('invoicesummaryclient','tbltasklist','invoice_company').all()
    for invoice in Totaldata:
        # print("loop")
        data={
                "id":invoice.id,
                "client":invoice.invoicesummaryclient.id,
                "invoice_amount":invoice.invoice_amount,
                "amount_received":invoice.amount_received,
                "invoicestatus":invoice.invoicestatus,
                "discount":invoice.discount,
                "subtotal":invoice.subtotal,
                "balancedue":invoice.balancedue,
                "duedate":invoice.duedate,
                "comments":invoice.comments,
                "tbltasklist_id":invoice.tbltasklist_id,
                "date":invoice.date,
                "deliverynoteid":invoice.deliverynoteid,
                "ismoved":invoice.ismoved,
                "companyid":invoice.invoice_company.id,
                "originalcompanyid":invoice.originalcompanyid,
                "originaldeliverynoteid":invoice.id,
                "companyinvoiceid":invoice.companyinvoiceid,
                "salesorder_id":invoice.salesorder_id,
                "vehiclenumber":invoice.vehiclenumber,
                "invoicetype":invoice.invoicetype,
                "clientgroupid_id":invoice.clientgroupid_id,
                "project_id":invoice.project_id,
                "invoicesummaryclient_id":invoice.invoicesummaryclient_id,
                "invoice_company_id":invoice.invoice_company.id,
                "receivedamount":invoice.amount_received,
                "invoiceamount":invoice.invoice_amount,
                "companyname":invoice.invoice_company.companyname,
                "companycode":invoice.invoice_company.companycode,
                "taskid":"" if invoice.tbltasklist is None else invoice.tbltasklist.id,
                "task":"" if invoice.tbltasklist is None else invoice.tbltasklist.task,
                "company_name":invoice.invoicesummaryclient.company_name,
                "engineer_name":invoice.invoicesummaryclient.engineer_name,
                "subclient":"" if invoice.tbltasklist is None else invoice.tbltasklist.subclient
            }
        # print(data)
        Return_data.append(data)
    return Response(Return_data)
           
class sp_moveselectedinvoice(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serialization.seralizationTblInvoicesummary

    def post(self, request):
        try:
            for selectedinvoice in request.data['invoicedetails']:
                print(selectedinvoice)
                queryset = TblInvoicesummary.objects.filter(
                    deliverynoteid=selectedinvoice['deliverynoteid'], invoice_company=selectedinvoice['companyid']).values()
                res = TblInvoicesummary.objects.filter(
                    invoice_company=request.data['companyid']).aggregate(max_id=Max('deliverynoteid'))
                max_devliverynoteid = 0
                if res['max_id'] == None:
                    max_devliverynoteid = 9999
                else:
                    max_devliverynoteid = res['max_id']
                if len(queryset) > 0:
                    updateinvoicesummary = {
                        "tbltasklistid": queryset[0]['tbltasklist_id'],
                        "projectid": queryset[0]['project_id'],
                        "originalcompanyid": queryset[0]['invoice_company_id'],
                        "originaldeliverynoteid": selectedinvoice['deliverynoteid'],                                         
                        "deliverynoteid": max_devliverynoteid+1,
                        "invoice_company": request.data['companyid'],
                        "invoicesummaryclientid":queryset[0]['invoicesummaryclient_id'],
                        "invoice_companyid":request.data['companyid'],
                    }
                    response = serialization.seralizationTblInvoicesummary(
                        models.TblInvoicesummary.objects.get(pk=queryset[0]['id']), data=updateinvoicesummary)
                    if response.is_valid():
                        response.save()
                    else:
                        raise ValueError("responsetransaction failed",
                                     response.errors)
                self.update_transaction(selectedinvoice['deliverynoteid'], int(
                    max_devliverynoteid)+1, selectedinvoice['companyid'], request.data['companyid'],)
                if len(queryset) > 0:
                    self.update_tasklist(
                        request.data['companyid'], queryset[0]['tbltasklist_id'], queryset[0]['invoicesummaryclient_id'])
                # return Response(response.errors)
            return Response(request.data)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    def update_transaction(self, oldDeliverynoteid, newDeliverynoteid, oldComanyid, newCompanyid):
        queryset = models.TblTransaction.objects.filter(
            deliverynoteid=oldDeliverynoteid, company_id=oldComanyid).values()
        if len(queryset) > 0:
            for transaction in queryset:
                print(transaction)
                update_transaction = {
                    "transaction_clientid": transaction['transaction_client_id'],
                    "userid_id": transaction['userid_id'],
                    "originalcompanyid": transaction['company_id_id'],
                    "originaldeliverynoteid": transaction['deliverynoteid'],
                    "deliverynoteid": newDeliverynoteid,
                    "companyid": newCompanyid,
                    "transactiontaskid": transaction['transactiontask_id'],
                    "voucherid": transaction['voucher_id']
                }
                responsetransaction = serialization.SerializationTransaction(
                    models.TblTransaction.objects.get(pk=transaction['id']), data=update_transaction)
                if responsetransaction.is_valid():
                    responsetransaction.save()
                else:
                    print(responsetransaction.errors)
                    raise ValueError("responsetransaction failed",
                                     responsetransaction.errors)

    def update_tasklist(self, companyid, tasklistid, client):
        tasklist_dict = {
            "company": companyid,
            "client": client
        }
        serializationtasklist = serialization.SerializationTaskList(
            models.TblTasklist.objects.get(pk=tasklistid), data=tasklist_dict)
        if serializationtasklist.is_valid():
            serializationtasklist.save()
        else:
            raise ValueError("serializationtasklist failed",
                             serializationtasklist.errors)


class sp_payforunpaidinvoice(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            queryset = TblTransaction.objects.filter(transaction_client=request.data['client_id'],
                                                     transactiontype="InvoiceBalanceLastYear",
                                                     date__gte=request.data['startdate'],
                                                     company_id=request.data['company_id_value'],
                                                     date__lte=request.data['enddate']
                                                     ).aggregate(Sum('amount'))
            previousyearinvoicebalance = queryset['amount__sum']
            if previousyearinvoicebalance == None:
                previousyearinvoicebalance = 0
            queryset = TblTransaction.objects.filter(transaction_client=request.data['client_id'],
                                                     transactiontype="ClientBalanceLastYear",
                                                     date__gte=request.data['startdate'],
                                                     company_id=request.data['company_id_value'],
                                                     date__lte=request.data['enddate']
                                                     ).aggregate(Sum('amount'))
            previousyearclientbalance = queryset['amount__sum']
            if previousyearclientbalance == None:
                previousyearclientbalance = 0

            balance = previousyearclientbalance-previousyearinvoicebalance
            queryset = TblTransaction.objects.filter(transaction_client=request.data['client_id'],
                                                     transactiontype__in=[
                                                         "Received", "AdjustmentReceived"],
                                                     date__gte=request.data['startdate'],
                                                     company_id=request.data['company_id_value'],
                                                     date__lte=request.data['enddate']
                                                     ).aggregate(Sum('amount'))
            SumofAllReceived = queryset['amount__sum']
            if SumofAllReceived == None:
                SumofAllReceived = 0

            queryset = TblTransaction.objects.filter(date__gte=request.data['startdate'],
                                                     date__lte=request.data['enddate'],
                                                     transaction_client=request.data['client_id'],
                                                     company_id=request.data['company_id_value'],
                                                     transactiontype__in=[
                                                         'AdjustmentSpend', 'Spend']
                                                     ).values()
            amount = 0
            for data in queryset:
                if len(data['deliverynoteid']) > 0:
                    invoice = TblInvoicesummary.objects.filter(
                        deliverynoteid=data['deliverynoteid'], invoice_company=request.data['company_id_value']).values()
                    if len(invoice) > 0:
                        if invoice[0]['invoicestatus'] != "Cancelled":
                            amount = int(data['amount'])+amount
                elif (len(data['deliverynoteid']) == 0) and (data['transactiontype'] != 'Invoice'):
                    amount = int(data['amount']) + amount
           
            if balance > 0:
                balancemoney = (balance+SumofAllReceived)-amount
            else:
                balancemoney = SumofAllReceived-amount
            print(balancemoney)
            while int(balancemoney) > 0:
                queryset = TblInvoicesummary.objects.filter(Q(invoice_company=request.data['company_id_value']),
                                                            Q(invoicesummaryclient_id=request.data['client_id']),
                                                            (Q(invoicestatus="Unpaid") | Q(
                                                                invoicestatus="Partially Paid"))
                                                            ).aggregate(Min('deliverynoteid'))
                print(queryset)
                unpaidinvoiceid = queryset['deliverynoteid__min']
                print(unpaidinvoiceid,"unpaidinvoiceid")
                if (len(queryset)>0 and (unpaidinvoiceid !=None)):
                    queryset = TblInvoicesummary.objects.filter(
                        invoice_company=request.data['company_id_value'], invoicesummaryclient=request.data['client_id'], deliverynoteid=unpaidinvoiceid).values()
                    taskid = queryset[0]['tbltasklist_id']
                    Balancedue = queryset[0]['balancedue']
                    if Balancedue is None:
                        Balancedue = 0
                    invoicereceived = queryset[0]['amount_received']
                    if invoicereceived is None:
                        invoicereceived = 0
                    if int(balancemoney) >= int(Balancedue):
                        Totalreceived = int(Balancedue)+int(invoicereceived)
                        balancemoney = int(balancemoney)-int(Balancedue)
                        snippet = TblInvoicesummary.objects.get(
                            invoice_company=request.data['company_id_value'], invoicesummaryclient=request.data['client_id'], deliverynoteid=unpaidinvoiceid)
                        update_dict = {
                            "invoicesummaryclientid":request.data['client_id'],
                            "invoice_companyid":request.data['company_id_value'],
                            "invoicestatus": "Paid",
                            "amount_received": Totalreceived,
                            "balancedue": "0",
                            "tbltasklistid": taskid,
                            "projectid": queryset[0]['project_id']
                        }
                        serializer = serialization.seralizationTblInvoicesummary(
                            snippet, data=update_dict)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            raise ValueError(
                                "serialization invoice summary failed", serializer.errors)
                        now = datetime.now()
                        currentdate = datetime.today().strftime('%Y-%m-%d')
                        current_time = now.strftime("%H:%M:%S")
                        transaction_data = {
                            "transactiontaskid": taskid,
                            "transaction_clientid": request.data['client_id'],
                            "userid_id": request.data['userid'],
                            "amount": Balancedue,
                            "deliverynoteid": unpaidinvoiceid,
                            "description": "",
                            "date": currentdate,
                            "time": current_time,
                            "transactiontype": "Spend",
                            "companyid": request.data['company_id_value'],
                            "originalcompanyid": "0",
                            "originaldeliverynoteid": "0",
                            "pmtmode": "",
                            "pmtreference": "",
                             "voucherid":""
                        }

                        serializer_transaction = serialization.SerializationTransaction(
                            data=transaction_data)
                        if serializer_transaction.is_valid():
                            serializer_transaction.save()
                        else:
                            raise ValueError(
                                "serializer_transaction failed", serializer_transaction.errors)

                    else:
                        receivedtotalAmount = int(
                            invoicereceived)+int(balancemoney)
                        duebalance = int(Balancedue)-int(balancemoney)
                        snippet = TblInvoicesummary.objects.get(
                            invoice_company=request.data['company_id_value'], invoicesummaryclient=request.data['client_id'], deliverynoteid=unpaidinvoiceid)
                        update_dict = {
                            "invoicesummaryclientid":request.data['client_id'],
                            "invoice_companyid":request.data['company_id_value'],
                            "invoicestatus": "Partially Paid",
                            "amount_received": receivedtotalAmount,
                            "balancedue": duebalance,
                            "tbltasklistid": taskid,
                            "projectid": queryset[0]['project_id']
                        }
                        serializer = serialization.seralizationTblInvoicesummary(
                            snippet, data=update_dict)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            raise ValueError(
                                "serialization invoice summary failed", serializer.errors)
                        now = datetime.now()
                        currentdate = datetime.today().strftime('%Y-%m-%d')
                        current_time = now.strftime("%H:%M:%S")
                        transaction_data = {
                            "transactiontaskid": taskid,
                            "transaction_clientid": request.data['client_id'],
                            "userid_id": request.data['userid'],
                            "amount": int(balancemoney),
                            "deliverynoteid": unpaidinvoiceid,
                            "description": "",
                            "date": currentdate,
                            "time": current_time,
                            "transactiontype": "Spend",
                            "companyid": request.data['company_id_value'],
                            "originalcompanyid": "0",
                            "originaldeliverynoteid": "0",
                            "pmtmode": "",
                            "pmtreference": "",
                             "voucherid":""
                        }
                        serializer_transaction = serialization.SerializationTransaction(
                            data=transaction_data)
                        if serializer_transaction.is_valid():
                            serializer_transaction.save()
                            balancemoney = 0
                        else:
                            raise ValueError(
                                "serializer_transaction failed", serializer_transaction.errors)
                else:
                    balancemoney = 0

            return Response(({"sum of all paid": amount}, {"balancemoney": balancemoney},
                             {"balance": balance}, {
                                 "SumofAllReceived": SumofAllReceived},
                             {"previousyearinvoicebalance": previousyearinvoicebalance}, {"previousyearclientbalance": previousyearclientbalance}))
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)


class sp_taskinvoiceinventorytransaction(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = serialization.seralizationTblInvoicesummary

    def post(self, request):
        currentdate = datetime.today().strftime('%Y-%m-%d')
        # print(request.data['stock'])
        try:
            for individualstock in request.data['stock']:
                result = (models.TblInventorytransaction.objects.filter(stockname=individualstock['types']).values('stockname', 'batch')
                         .annotate(dcount=Sum('quantity'))
                          )
                numberofdata = len(result)
                loopcount = 0
                quantity = int(individualstock['quantity'])
                while quantity > 0:
                    if numberofdata > loopcount:
                        filterdata = result[loopcount]
                        if int(result[loopcount]['dcount']) > 0:
                            if quantity <= int(result[loopcount]['dcount']):
                                loopcount = loopcount+1
                                inventory_dict = {
                                    'date':  date.today(),
                                    'username': request.data['userid'],
                                    'stockname': individualstock['types'],
                                    'productcode': individualstock['productcode'],
                                    'quantity': -quantity,
                                    'status': 'Invoice Stock',
                                    'invoiceno': request.data['deliverynoteid'],
                                    'rate': individualstock['rate'],
                                    'amount': int(individualstock['rate'])*int(quantity),
                                    'cgstpercentage': '',
                                    'sgstpercentage': '',
                                    'total': -int(individualstock['rate'])*int(quantity),
                                    'batch': filterdata['batch'],
                                    'location': '0',
                                    'companyid': request.data['companyid']
                                }
                                queryInventorytansaction = serialization.SerializationInventorytransaction(
                                    data=inventory_dict)
                                if queryInventorytansaction.is_valid():
                                    queryInventorytansaction.save()
                                    quantity = 0
                                else:
                                    raise Response(
                                        queryInventorytansaction.errors)
                            else:                          
                                inventory_dict = {
                                    'date': date.today(),
                                    'username': request.data['userid'],
                                    'stockname': individualstock['types'],
                                    'productcode': individualstock['productcode'],
                                    'quantity': -int(result[loopcount]['dcount']),
                                    'status': 'Invoice Stock',
                                    'invoiceno': request.data['deliverynoteid'],
                                    'rate': individualstock['rate'],
                                    'amount': int(individualstock['rate'])*int(quantity),
                                    'cgstpercentage': '',
                                    'sgstpercentage': '',
                                    'total': -int(individualstock['rate'])*int(quantity),
                                    'batch': filterdata['batch'],
                                    'location': '0',
                                    'companyid': request.data['companyid']
                                }
                                queryInventorytansaction = serialization.SerializationInventorytransaction(
                                    data=inventory_dict)
                                if queryInventorytansaction.is_valid():
                                    queryInventorytansaction.save()
                                    quantity = quantity - int(result[loopcount]['dcount'])
                                    loopcount = loopcount+1
                                else:
                                    print( queryInventorytansaction.errors,"line807")
                                    raise Response(
                                        queryInventorytansaction.errors)
                                # print(quantity,"line 579")
                                # # quantity=0;
                        else:
                            loopcount = loopcount+1
                    else:
                        print("line")
                        inventory_dict = {
                            'date': date.today(),
                            'username': request.data['userid'],
                            'stockname': individualstock['types'],
                            'productcode': individualstock['productcode'],
                            'quantity': -quantity,
                            'status': 'Invoice Stock',
                            'invoiceno': request.data['deliverynoteid'],
                            'rate': individualstock['rate'],
                            'amount': int(individualstock['rate'])*int(quantity),
                            'cgstpercentage': '',
                            'sgstpercentage': '',
                            'total': -int(individualstock['rate'])*int(quantity),
                            'batch': filterdata['batch'],
                            'location': '0',
                            'companyid': request.data['companyid']
                        }
                        queryInventorytansaction = serialization.SerializationInventorytransaction(data=inventory_dict)
                        if queryInventorytansaction.is_valid():
                            queryInventorytansaction.save()
                            self.create_purchaser_request(
                                request.data, individualstock)
                            quantity = 0
                        else:
                            raise Response(queryInventorytansaction.errors)
            return Response("created successsfully")
        except Exception as ex:
            return Response(ex, status=status.HTTP_400_BAD_REQUEST)

            # return Response(request.data)

    def create_purchaser_request(self, requestdata, individualstock):
        purchase = {
            'date': date.today(),
            'time': datetime.today().strftime('%Y-%m-%d'),
            'username': requestdata['userid'],
            'stockname': individualstock['types'],
            'productcode': individualstock['productcode'],
            'quantity': individualstock['quantity'],
            'status': "Requested",
            'description': "",
            'purchaseorderid': "",
            'isdeleted': 0
        }
        queryInventorytansaction = serialization.SerializarionUserpurchaserequest(
            data=purchase)
        if queryInventorytansaction.is_valid():
            queryInventorytansaction.save()
        else:
            raise Response(queryInventorytansaction.errors)


class SpDaterangeInvoiceReceivedAmount(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # print(request.data)
        if int(request.data['clientid']) > 99:
            if request.data['company_id'] == 0:
                Transactionleftjoindata = []
                Returndata = []
                transactiondata = models.TblTransaction.objects.filter(transactiontype__in=[
                                                                       'Invoice', 'AdjustmentInvoice'], date__gte=request.data['startdate'], date__lte=request.data['enddate'], transaction_client=request.data['clientid']).values()
                for trans in transactiondata:
                    # print(trans)
                    if trans['deliverynoteid'] !='':
                        deliverynoteid = models.TblInvoicesummary.objects.filter(
                            deliverynoteid=trans['deliverynoteid'],invoice_company=trans['company_id_id']).values()
                        if len(deliverynoteid)>0:
                            status = deliverynoteid[0]['invoicestatus']
                        if len(deliverynoteid) > 0 and status != 'Cancelled':
                            Transactionleftjoindata.append(trans)
                totalinvoiced = sum(int(item['amount'])
                                    for item in Transactionleftjoindata)
                totalReceived = models.TblTransaction.objects.filter(transactiontype__in=[
                                                                    'Received', 'AdjustmentReceived'], date__gte=request.data['startdate'], date__lte=request.data['enddate'], transaction_client=request.data['clientid']).aggregate(Sum('amount'))
                Returndata.append(totalinvoiced)
                Returndata.append(totalReceived['amount__sum'])
            else:
                Transactionleftjoindata = []
                Returndata = []
                transactiondata = models.TblTransaction.objects.filter(transactiontype__in=['Invoice', 'AdjustmentInvoice'], date__gte=request.data[
                                                                       'startdate'], date__lte=request.data['enddate'], transaction_client=request.data['clientid'], company_id=request.data['company_id']).values()
                for trans in transactiondata:
                    if trans['deliverynoteid'] != '':
                        deliverynoteid = models.TblInvoicesummary.objects.filter(
                            deliverynoteid=trans['deliverynoteid']).values()
                        if len(deliverynoteid)>0:
                            status = deliverynoteid[0]['invoicestatus']
                        # print(trans)
                        if len(deliverynoteid) > 0 and status != 'Cancelled':
                            Transactionleftjoindata.append(trans)
                totalinvoiced = sum(int(item['amount'])
                                    for item in Transactionleftjoindata)
                totalReceived = models.TblTransaction.objects.filter(transactiontype__in=['Received', 'AdjustmentReceived'], date__gte=request.data[
                                                                     'startdate'], date__lte=request.data['enddate'], transaction_client=request.data['clientid'], company_id=request.data['company_id']).aggregate(Sum('amount'))
                Returndata.append(totalinvoiced)
                Returndata.append(totalReceived['amount__sum'])
                # print("TotalCompany")
            return Response(Returndata)
        else:
            if int(request.data['clientid']) == 98:
                # print("client id is 98")
                if request.data['company_id'] == 0:
                    Transactionleftjoindata = []
                    Returndata = []
                    transactiondata = models.TblTransaction.objects.filter(transactiontype__in=[
                                                                           'Invoice', 'AdjustmentInvoice'], date__gte=request.data['startdate'], date__lte=request.data['enddate'], transaction_client='110').values()
                    for trans in transactiondata:
                        if trans['deliverynoteid'] != '':
                            deliverynoteid = models.TblInvoicesummary.objects.filter(
                                deliverynoteid=trans['deliverynoteid']).values()
                            if len(deliverynoteid)>0:
                                status = deliverynoteid[0]['invoicestatus']
                            # print(trans)
                            if len(deliverynoteid) > 0 and status != 'Cancelled':
                                Transactionleftjoindata.append(trans)
                    totalinvoiced = sum(int(item['amount'])
                                        for item in Transactionleftjoindata)
                    totalReceived = models.TblTransaction.objects.filter(transactiontype__in=[
                                                                         'Received', 'AdjustmentReceived'], date__gte=request.data['startdate'], date__lte=request.data['enddate'], transaction_client='110').aggregate(Sum('amount'))
                    Returndata.append(totalinvoiced)
                    Returndata.append(totalReceived['amount__sum'])
                    # print("AllCompanys")
                else:
                    Transactionleftjoindata = []
                    Returndata = []
                    transactiondata = models.TblTransaction.objects.filter(transactiontype__in=[
                                                                           'Invoice', 'AdjustmentInvoice'], date__gte=request.data['startdate'], date__lte=request.data['enddate'], clientid=110, company_id=request.data['company_id']).values()
                    for trans in transactiondata:
                        if trans['deliverynoteid'] != '':
                            deliverynoteid = models.TblInvoicesummary.objects.filter(
                                deliverynoteid=trans['deliverynoteid']).values()
                            if len(deliverynoteid)>0:
                                status = deliverynoteid[0]['invoicestatus']
                            # print(trans)
                            if len(deliverynoteid) > 0 and status != 'Cancelled':
                                Transactionleftjoindata.append(trans)
                    totalinvoiced = sum(int(item['amount'])
                                        for item in Transactionleftjoindata)
                    totalReceived = models.TblTransaction.objects.filter(transactiontype__in=['Received', 'AdjustmentReceived'], date__gte=request.data[
                                                                         'startdate'], date__lte=request.data['enddate'], transaction_client=110, company_id=request.data['company_id']).aggregate(Sum('amount'))
                    Returndata.append(totalinvoiced)
                    Returndata.append(totalReceived['amount__sum'])
                    # print("TotalCompany")
                return Response(Returndata)
            else:
                print("company99")
                if request.data['company_id'] == 0:
                    Transactionleftjoindata = []
                    Returndata = []
                    transactiondata = models.TblTransaction.objects.filter(transactiontype__in=[
                                                                           'Invoice', 'AdjustmentInvoice'], date__gte=request.data['startdate'], date__lte=request.data['enddate']).aggregate(Sum('amount'))
                    cancelinvoice=models.TblInvoicesummary.objects.filter(invoicestatus='Cancelled').values()
                    cancelinvoicetotal=0
                    for invoice in cancelinvoice:
                        total=models.TblTransaction.objects.filter(transactiontype__in=[
                                                                          'Invoice', 'AdjustmentInvoice'],company_id=invoice['invoice_company_id'],deliverynoteid=invoice['deliverynoteid']).aggregate(Sum('amount'))
                        amount= 0 if total['amount__sum'] is None else total['amount__sum']
                        cancelinvoicetotal=cancelinvoicetotal+amount
                   
                    totalReceived = models.TblTransaction.objects.filter(transactiontype__in=[
                                                                         'Received', 'AdjustmentReceived'], date__gte=request.data['startdate'], date__lte=request.data['enddate']).aggregate(Sum('amount'))
                    totalinvoiced=transactiondata['amount__sum']-cancelinvoicetotal
                    Returndata.append(totalinvoiced)
                    Returndata.append(totalReceived['amount__sum'])
                else:
                    Transactionleftjoindata = []
                    Returndata = []
                    transactiondata = models.TblTransaction.objects.filter(transactiontype__in=[
                                                                           'Invoice', 'AdjustmentInvoice'], date__gte=request.data['startdate'], date__lte=request.data['enddate'], company_id=request.data['company_id']).aggregate(Sum('amount'))
                    cancelinvoice=models.TblInvoicesummary.objects.filter(invoicestatus='Cancelled',invoice_company=request.data['company_id']).values()
                    cancelinvoicetotal=0
                    for invoice in cancelinvoice:
                        total=models.TblTransaction.objects.filter(transactiontype__in=[
                                                                          'Invoice', 'AdjustmentInvoice'],company_id=invoice['invoice_company_id'],deliverynoteid=invoice['deliverynoteid']).aggregate(Sum('amount'))
                        amount= 0 if total['amount__sum'] is None else total['amount__sum']
                        cancelinvoicetotal=cancelinvoicetotal+amount
                   
                    totalReceived = models.TblTransaction.objects.filter(transactiontype__in=[
                                                                         'Received', 'AdjustmentReceived'], date__gte=request.data['startdate'], date__lte=request.data['enddate'], company_id=request.data['company_id']).aggregate(Sum('amount'))
                    totalinvoiced=transactiondata['amount__sum']-cancelinvoicetotal
                    Returndata.append(totalinvoiced)
                    Returndata.append(totalReceived['amount__sum'])
                    # print("TotalCompany")
                return Response(Returndata)

   # for trans in transactiondata:
                    #     # print(trans['deliverynoteid'])
                    #     if trans['deliverynoteid'] != '':
                    #         deliverynoteid = models.TblInvoicesummary.objects.filter(
                    #             deliverynoteid=trans['deliverynoteid']).values()
                    #         if len(deliverynoteid)>0:
                    #             status = deliverynoteid[0]['invoicestatus']
                    #         # print(trans)
                    #         if len(deliverynoteid) > 0 and status != 'Cancelled':
                    #             Transactionleftjoindata.append(trans)
                    # totalinvoiced = sum(int(item['amount'])
                    #                     for item in Transactionleftjoindata)


     # print(cancelinvoicetotal)
                    # for trans in transactiondata:
                    #     if trans['deliverynoteid'] != '':
                    #         deliverynoteid = models.TblInvoicesummary.objects.filter(
                    #             deliverynoteid=trans['deliverynoteid']).values()
                    #         if len(deliverynoteid)>0:
                    #             status = deliverynoteid[0]['invoicestatus']
                    #         # print(trans)
                    #         if len(deliverynoteid) > 0 and status != 'Cancelled':
                    #             Transactionleftjoindata.append(trans)
                    # totalinvoiced = sum(int(item['amount'])
                    #                     for item in Transactionleftjoindata)


class SpJoinTransaction(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requestdata = models.TblTransaction.objects.all().values()
        for data in requestdata:
            data['company_id_id'] = models.TblCompany.objects.filter(
                id=data['companyid']).values()
            data['transaction_client_id'] = models.TblClient.objects.filter(
                id=data['clientid_id']).values()
            data['userid_id'] = models.Users.objects.filter(
                id=data['userid_id']).values()
            taskdetails = []
            if data["transactiontask_id"] != '' and data["transactiontask_id"] != None:
                taskdetails = models.TblTasklist.objects.filter(
                    id=int(data["transactiontask_id"])).values()
            if len(taskdetails) > 0:
                data['transactiontask_id'] = taskdetails[0]
        return Response(requestdata)


class SpGetAvailableQTYTemptable(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        result = (models.TblInventorytransaction.objects.filter().values('stockname', 'batch')
                  .annotate(quantity=Sum('quantity')).filter(quantity__gt=0)
                  )
        print(result)
        purchasestock = self.getpurchasestockdetails()
        salestocks = self.getsalestransaction()
        # print(purchasestock,salestocks)
        # print(salestocks)
        dict_returndata = []
        for inventory in result:
            purchase = 0
            salesqty = 0
            for sales in salestocks:
                if inventory['stockname'] == sales['stockname']:
                    salesqty = sales['quantity']
            for stock in purchasestock:
                if inventory['stockname'] == stock['name']:
                    purchase = stock['quantity']
            dict = {
                "StockName": inventory['stockname'],
                "InventoryQty": inventory['quantity'],
                "SOQty": salesqty,
                "POQty": purchase,
                "TotalQty": int(inventory['quantity'])+int(purchase)-int(salesqty)
            }
            dict_returndata.append(dict)
        return Response(dict_returndata)

    def getpurchasestockdetails(self):
        result = (models.TblPurchasestocks.objects.filter(status__in=['Partially Received', 'Issued']).values('name')
                  .annotate(quantity=Sum('quantity')-Sum('received')).filter(quantity__gt=0)
                  )
        return result

    def getsalestransaction(self):
        result = (models.TblSalestransaction.objects.filter(status__in=['Partially Dispatched', 'Issued']).values('stockname')
                  .annotate(quantity=Sum('quantity')-Sum('usedqty')).filter(quantity__gt=0)
                  )
        return result


class SpSummarizedBalance(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        totaldata = []
        get_distinct = models.TblInvoicesummary.objects.order_by(
            'invoicesummaryclient_id').values('invoicesummaryclient_id').distinct()
        for data in get_distinct:
            clientname=models.TblClient.objects.filter(id=data['invoicesummaryclient_id']).values('company_name')
            invoicesummarydata=models.TblInvoicesummary.objects.filter(invoicesummaryclient_id=data['invoicesummaryclient_id'],invoicestatus__in=['Paid','Partially Paid','Unpaid']).aggregate(Sum('invoice_amount'),Sum('amount_received'),Sum('balancedue'))
            if(invoicesummarydata['invoice_amount__sum']==0.0  and invoicesummarydata['amount_received__sum']==0.0 and invoicesummarydata['balancedue__sum']==0.0):
                pass
            else:
                if invoicesummarydata['invoice_amount__sum'] != invoicesummarydata['amount_received__sum']:
                    dict_summarized={
                        "invoicesummaryclient_id":data['invoicesummaryclient_id'],
                        "clientname":clientname[0]['company_name'],
                        "invoice_amount":invoicesummarydata['invoice_amount__sum'],
                        "amount_received":invoicesummarydata['amount_received__sum'],
                        "balancedue":invoicesummarydata['balancedue__sum'],
                    }
                    totaldata.append(dict_summarized)

        return Response(totaldata)


class JoinInvoiceSummaryRaw(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        clients=models.TblInvoicesummary.objects.order_by(
            'invoicesummaryclient').values('invoicesummaryclient').distinct()
        # print(clients)
        totalcompanys=[]
        for data in clients:
            companyname=models.TblClient.objects.filter(id=data['invoicesummaryclient']).values('company_name')
            data={
                "company_name":companyname[0]['company_name'],
            }
            totalcompanys.append(data)
        return Response(totalcompanys)


class Transactiondetails(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        Transactiondetails=models.TblTransaction.objects.filter(date__gte=request.data['startdate'],date__lte=request.data['enddate']).values()
        Return_data=[]
        print(len(Transactiondetails))
        for transaction in Transactiondetails:
            clientname=models.TblClient.objects.filter(id=transaction['clientid_id']).values('company_name')
            companyname=models.TblCompany.objects.filter(id=transaction['companyid']).values('companyname')
            username=models.Users.objects.filter(id=transaction['userid_id']).values('name')
            print(clientname[0]['company_name'])
            transaction['clientid_id']=clientname[0]['company_name']
            transaction['companyid']=companyname[0]['companyname']
            transaction['userid_id']=username[0]['name']
            if transaction['taskid'] !='' and transaction['taskid']!=None:
               task=models.TblTasklist.objects.filter(id=transaction['taskid']).values('task')
               transaction['taskid']=task[0]['task']
            Return_data.append(transaction)
        return Response(Return_data) 


class SpTransactionOverView(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Transactiondetails=models.TblTransaction.objects.filter(date__gte=request.data['startdate'],date__lte=request.data['enddate']).all()
        print(Transactiondetails)
        serializer = serialization.SerializationTransaction(Transactiondetails, many=True)
        print(serializer.data)
        # for transaction in serializer.data:
        #     transaction['clientid']= transaction['clientid']['company_name']
        #     print(transaction)
        return Response(serializer.data)


class sptransaction2(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Transactiondetails=models.TblTransaction.objects.filter(date__gte=request.data['startdate'],date__lte=request.data['enddate']).select_related('userid','transaction_client','transactiontask','company_id','client_groupid','voucher').all()
        returndata=[]
        # print(Transactiondetails)
        for transaction in Transactiondetails:
            if (transaction.transactiontype != 'ClientBalanceLastYear') and (transaction.transactiontype != 'InvoiceBalanceLastYear'): 
                data={
                    "id": transaction.id,
                    "date": transaction.date,
                    "time": transaction.time,
                    "name": transaction.userid.name,
                    "Invoice": transaction.deliverynoteid,
                    "ClientName": transaction.transaction_client.company_name,
                    "Task": transaction.transactiontask.task if transaction.transactiontask is not None else "",
                    "Credit": transaction.amount if  transaction.transactiontype=='Received' or transaction.transactiontype=='CancelReceived'or transaction.transactiontype=='AdjustmentReceived' else 0,
                    "Debit":transaction.amount if  transaction.transactiontype=='Spend' or transaction.transactiontype=='AdjustmentSpend'else 0,
                    "InvoiceAmount": transaction.amount if  transaction.transactiontype=='Invoice' or transaction.transactiontype=='AdjustmentInvoice' else 0,
                    "companyid": transaction.company_id.companyname,
                    "clientgroupid": transaction.client_groupid.id if transaction.client_groupid is not None else transaction.client_groupid,
                    "transactiontype": transaction.transactiontype,
                    "Amount":transaction.amount,
                    "openingbalance":"",
                    "closingbalance":"",
                    "Paymentmode":transaction.pmtmode,  
                    "ReferenceNo":transaction.pmtreference,
                    "voucher_id": transaction.voucher.id if transaction.voucher is not None else "" ,
                    "voucherreferencetype":transaction.voucherreferencetype,
                    "vouchertype": transaction.vouchertype,
                       }
                returndata.append(data)
        return Response(returndata)





