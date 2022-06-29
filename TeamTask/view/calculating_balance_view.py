from rest_framework.views import APIView
from django.db.models import Sum,Max,Q
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from TeamTask.models import TblInvoicesummary, TblTransaction
from TeamTask.serialization import SerializationTransaction, seralizationTblInvoicesummary,seralizationTblTaskinvoicedetails


class SpCalculateClosingBalance(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if int(request.data['company_id']) == 0:
            queryset = TblTransaction.objects.filter(date__gte=request.data['startdate'],
                                                     date__lte=request.data['enddate'],
                                                     transaction_client=request.data['client_id'],
                                                     transactiontype__in=['Invoice', 'InvoiceBalanceLastYear',
                                                                          'AdjustmentInvoice']
                                                     ).values()
            
            total_invoiced = 0
            for data in queryset:
                if (len(data['deliverynoteid'])) > 0:
                    invoice = TblInvoicesummary.objects.filter(deliverynoteid=data['deliverynoteid'],
                                                                invoice_company=data['company_id_id']).values()
                    
                    if len(invoice)>0:
                        if invoice[0]['invoicestatus'] != "Cancelled":
                            total_invoiced = int(data['amount']) + total_invoiced
                elif (len(data['deliverynoteid']) == 0) and (data['transactiontype']!='Invoice'):
                        total_invoiced = int(data['amount']) + total_invoiced
            queryset = TblTransaction.objects.filter(transaction_client=request.data['client_id'],
                                                     transactiontype__in=['Received', 'ClientBalanceLastYear',
                                                                          'AdjustmentReceived'],
                                                     date__gte=request.data['startdate'],
                                                     date__lte=request.data['enddate']).aggregate(Sum('amount'))
            total_received = queryset['amount__sum']
            if total_received == None:
                total_received = 0
            balance = total_invoiced - total_received
        else:
            queryset = TblTransaction.objects.filter(date__gte=request.data['startdate'],
                                                     date__lte=request.data['enddate'],
                                                     transaction_client=request.data['client_id'],
                                                     company_id=request.data['company_id'],
                                                     transactiontype__in=['Invoice', 'InvoiceBalanceLastYear',
                                                                          'AdjustmentInvoice']
                                                     ).values()
            
            total_invoiced = 0
            for data in queryset:
                if (len(data['deliverynoteid']) > 0 ):
                    invoice = TblInvoicesummary.objects.filter(deliverynoteid=data['deliverynoteid'],
                                                                invoice_company=data['company_id_id']).values()
                    
                   
                    if len(invoice)>0:
                        if invoice[0]['invoicestatus'] != "Cancelled":
                            total_invoiced = int(data['amount']) + total_invoiced
                elif (len(data['deliverynoteid']) == 0 ) and (data['transactiontype']!='Invoice'):
                    total_invoiced = int(data['amount']) + total_invoiced
            queryset = TblTransaction.objects.filter(transaction_client=request.data['client_id'],
                                                     transactiontype__in=['Received', 'ClientBalanceLastYear',
                                                                          'AdjustmentReceived'],
                                                     date__gte=request.data['startdate'],
                                                     date__lte=request.data['enddate'],
                                                     company_id=request.data['company_id']).aggregate(Sum('amount'))
            total_received = queryset['amount__sum']
            if total_received is None:
                total_received = 0
            balance = total_invoiced - total_received
        return Response({"balance": balance, "total_received": total_received, "total_invoiced": total_invoiced})


class SpReceivedAmountAdjustment(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            currentdate = datetime.today().strftime('%Y-%m-%d')
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            count=0
            transaction_data={
                    "transactiontaskid":"",
                    "date": currentdate,
                    "time": current_time,
                    "amount": request.data['adjustmentamount'],
                    "deliverynoteid": "",
                    "originaldeliverynoteid": 0,
                    "originalcompanyid": 0,
                    "salesorderid": None,
                    "transactiontype": "invoice",
                    "companyid": request.data['companyid'],
                    "transaction_clientid":request.data['clientid'],
                    "userid_id":request.data['userid'],
                    "voucherid":""
            }
            serializer=SerializationTransaction(data=transaction_data)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError("transaction data serilaizer failed",serializer.errors)
            if int(request.data['closingbalanceamount'])<0:
               actualbalance=int(request.data['adjustmentamount'])-int(request.data['closingbalanceamount'])
            queryset=TblTransaction.objects.filter(company_id=request.data['companyid'],
                                                                  transaction_client=request.data['clientid'],
                                                                  transactiontype="Spend").aggregate(Max('id'))
            max_spend_transaction_id=queryset['id__max']
            while int(actualbalance)<0:
                previous_max_transaction=max_spend_transaction_id
                if count>0:
                    print(previous_max_transaction,"previous_max_transaction in if")
                    queryset=TblTransaction.objects.filter(company_id=request.data['companyid'],
                                                                  transaction_client=request.data['clientid'],
                                                                  transactiontype="Spend",
                                                                  id__lt=previous_max_transaction).aggregate(Max('id'))
                    max_spend_transaction_id=queryset['id__max']
                queryset=TblTransaction.objects.filter(id=max_spend_transaction_id).values()
                taskid=queryset[0]['transactiontask_id']
                amount=queryset[0]['amount']
                invoiceid=queryset[0]['deliverynoteid']
                queryset=TblInvoicesummary.objects.filter(deliverynoteid=invoiceid,
                                                          invoice_company=request.data['companyid'],
                                                          invoicesummaryclient=request.data['clientid']).values()
                invoicestatus=queryset[0]['invoicestatus']
                invoice_received_amount=queryset[0]['amount_received']
                invoice_amount=queryset[0]['invoice_amount']
                if int(amount)<abs(int(actualbalance)):
                    # transaction_amount=amount
                    transaction_data_spend={
                            "transactiontaskid":taskid,
                            "date": currentdate,
                            "time": current_time,
                            "amount": (int(amount)* (-1)), 
                            "deliverynoteid": invoiceid,
                            "originaldeliverynoteid": 0,
                            "originalcompanyid": 0,
                            "salesorderid": None,
                            "transactiontype": "Spend",
                            "companyid": request.data['companyid'],
                            "transaction_clientid":request.data['clientid'],
                            "userid_id":request.data['userid'],
                            "voucherid":""
                    }
                    serializer=SerializationTransaction(data=transaction_data_spend)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValueError("transaction data serilaizer failed when count greater than zero",serializer.errors)
                    actualbalance=int(actualbalance)+int(amount)
                    balance_received=int(invoice_received_amount)-int(amount)
                    print(balance_received,"balance_received")
                    if balance_received==0:
                        snippet=TblInvoicesummary.objects.filter(deliverynoteid=invoiceid,
                                                                invoice_company_id=request.data['companyid'],
                                                                invoicesummaryclient=request.data['clientid']).values()
                        for id in snippet:
                            snippet=TblInvoicesummary.objects.get(pk=id['id'])
                            update_data={
                                "amount_received":0,
                                "invoicestatus":"Unpaid",
                                "balancedue":invoice_amount,
                                "tbltasklistid":taskid,
                                "projectid":id['project_id'],
                                "invoicesummaryclientid":id['invoicesummaryclient_id'],
                                "invoice_companyid":id['invoice_company_id']

                            }
                            serializer=seralizationTblInvoicesummary(snippet,data=update_data)
                            if serializer.is_valid():
                                serializer.save
                            else:
                                raise ValueError("transaction data serilaizer failed while updating as unpaid",serializer.errors)
                    else:
                        due_balance=int(invoice_amount)-balance_received
                        snippet=TblInvoicesummary.objects.filter(deliverynoteid=invoiceid,
                                                                invoice_company_id=request.data['companyid'],
                                                                invoicesummaryclient=request.data['clientid']).values()
                        print(snippet,"snippet")
                        for id in snippet:
                            snippet=TblInvoicesummary.objects.get(pk=id['id'])
                            update_data={
                                "amount_received":balance_received,
                                "invoicestatus":"Partially Paid",
                                "balancedue":due_balance,
                                "tbltasklistid":taskid,
                                "projectid":id['project_id'],
                                "invoicesummaryclientid":id['invoicesummaryclient_id'],
                                "invoice_companyid":id['invoice_company_id']
                            }
                            serializer=seralizationTblInvoicesummary(snippet,data=update_data)
                            if serializer.is_valid():
                                serializer.save
                            else:
                                raise ValueError("transaction data serilaizer failed while updating as Partially Paid",serializer.errors)
                else:
                    transaction_data_spend={
                           "transactiontaskid":taskid,
                            "date": currentdate,
                            "time": current_time,
                            "amount": actualbalance, 
                            "deliverynoteid": invoiceid, 
                            "originaldeliverynoteid": 0,
                            "originalcompanyid": 0,
                            "salesorderid": None,
                            "transactiontype": "Spend",
                            "companyid": request.data['companyid'],
                            "transaction_clientid":request.data['clientid'],
                            "userid_id":request.data['userid'],
                            "voucherid":""
                    }
                    serializer=SerializationTransaction(data=transaction_data_spend)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValueError("transaction spend data serializer failed ",serializer.error)

                    balance_received=int(invoice_received_amount)-abs(actualbalance)
                    print(balance_received,"balance_received in else")
                    if balance_received==0:
                        snippet=TblInvoicesummary.objects.filter(deliverynoteid=invoiceid,
                                                                invoice_company_id=request.data['companyid'],
                                                                invoicesummaryclient=request.data['clientid']).values()
                        for id in snippet:
                            snippet=TblInvoicesummary.objects.get(pk=id['id'])
                            update_data={
                                "amount_received":0,
                                "invoicestatus":"Unpaid",
                                "balancedue":invoice_amount,
                                "tbltasklistid":taskid,
                                "projectid":id['project_id'],
                                "invoicesummaryclientid":id['invoicesummaryclient_id'],
                                "invoice_companyid":id['invoice_company_id']
                            }
                            serializer=seralizationTblInvoicesummary(snippet,data=update_data)
                            if serializer.is_valid():
                                serializer.save
                            else:
                                raise ValueError("transaction spend data serializer failed while updating as Unpaid",serializer.errors)
                    else:
                        due_balance=int(invoice_amount)-balance_received
                        snippet=TblInvoicesummary.objects.filter(deliverynoteid=invoiceid,
                                                                invoice_company_id=request.data['companyid'],
                                                                invoicesummaryclient=request.data['clientid']).values()
                        for id in snippet:
                            snippet=TblInvoicesummary.objects.get(pk=id['id'])
                            update_data={
                                "amount_received ":balance_received,
                                "invoicestatus":"Partially Paid",
                                "balancedue":due_balance,
                                "tbltasklistid":taskid,
                                "projectid":id['project_id'],
                                "invoicesummaryclientid":id['invoicesummaryclient_id'],
                                "invoice_companyid":id['invoice_company_id']
                            }
                            serializer=seralizationTblInvoicesummary(snippet,data=update_data)
                            if serializer.is_valid():
                                serializer.save 
                            else:
                                raise ValueError("transaction spend data serializer failed  while updating as Partially Paid",serializer.errors)
                    actualbalance=0 
                count=count+1
            return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response("Seems like actual balance isn't less than Zero")
        except Exception as ex:
            return Response(str(ex),status=status.HTTP_400_BAD_REQUEST)

class SpCalculateOpeningBalance(APIView):
    def post(self,request):
        if int(request.data['company_id'])==0:
            end_date=request.data['taxyear_start_date'] if (request.data['start_date']<=request.data['taxyear_start_date']) else request.data['start_date']
            date_month=end_date[6]+end_date[9]
            print(date_month,end_date[6],end_date[9])
            if date_month!=41:
                queryset=TblTransaction.objects.filter(Q(transactiontype="InvoiceBalanceLastYear")|
                                                      (Q(transactiontype="Invoice"))|
                                                      (Q(transactiontype="AdjustmentInvoice")),
                                                      date__gte=request.data['taxyear_start_date'],
                                                      date__lt=end_date,
                                                      transaction_client=request.data['client_id']).values()
                total_invoiced = 0
                for data in queryset:
                    if (len(data['deliverynoteid']) > 0 ):
                        invoice = TblInvoicesummary.objects.filter(deliverynoteid=data['deliverynoteid'],
                                                                     invoice_company=data['company_id_id']).values()

                        if len(invoice)>0:
                            if invoice[0]['invoicestatus'] != "Cancelled":
                                total_invoiced = int(data['amount']) + total_invoiced
                    elif (len(data['deliverynoteid']) == 0 ) and (data['transactiontype']!='Invoice'):
                        total_invoiced = int(data['amount']) + total_invoiced

            queryset = TblTransaction.objects.filter(transaction_client=request.data['client_id'],
                                                     transactiontype__in=['Received', 'ClientBalanceLastYear',
                                                                          'AdjustmentReceived'],
                                                     date__gte=request.data['taxyear_start_date'],
                                                     date__lt=end_date).aggregate(Sum('amount'))
            total_received = queryset['amount__sum']

            if total_received is None:
                total_received = 0
            balance = total_invoiced - total_received
        else:
            end_date=request.data['taxyear_start_date'] if (request.data['start_date']<request.data['taxyear_start_date']) else request.data['start_date']
            date_month=end_date[6]+end_date[9]
            #if date_month!=41:
            queryset=TblTransaction.objects.filter(transactiontype__in=['InvoiceBalanceLastYear','Invoice','AdjustmentInvoice'],
                                                  date__gte=request.data['taxyear_start_date'],
                                                  date__lt=end_date,
                                                  company_id=request.data['company_id'],
                                                  transaction_client=request.data['client_id']).values()
            total_invoiced = 0
            for data in queryset:
                if (len(data['deliverynoteid']) > 0 ):
                     
                    invoice = TblInvoicesummary.objects.filter(deliverynoteid=data['deliverynoteid'],
                                                                 invoice_company=data['company_id_id']).values()
                    if len(invoice)>0:
                        if invoice[0]['invoicestatus'] != "Cancelled":
                            total_invoiced = int(data['amount']) + total_invoiced
                elif (len(data['deliverynoteid']) == 0 ) and (data['transactiontype']!='Invoice'):
                    total_invoiced = int(data['amount']) + total_invoiced
            if date_month!=41:
                queryset = TblTransaction.objects.filter(Q(transactiontype="ClientBalanceLastYear")|
                                                         Q(transactiontype="Received")|
                                                         Q(transactiontype="AdjustmentReceived"),
                                                         Q(transaction_client=request.data['client_id']),
                                                         Q(company_id=request.data['company_id']),
                                                         Q(date__gte=request.data['taxyear_start_date']),
                                                         Q(date__lt=end_date)).aggregate(Sum('amount'))
                total_received = queryset['amount__sum']

                if total_received is None:
                    total_received = 0
            balance = total_invoiced - total_received
        return Response({"balance": balance, "total_received": total_received, "total_invoiced": total_invoiced})
            
 
            
