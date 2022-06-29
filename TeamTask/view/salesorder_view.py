
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from datetime import date, datetime
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Max, Sum, Min, Q
from TeamTask.models import TblClient, TblInventorytransaction, TblInvoicesummary, TblQuotationrequest, TblQuotationtransaction, TblSales, TblSalesrequest, TblSalestransaction, TblStock, TblTransaction
from rest_framework.response import Response
from TeamTask.serialization import SerializarionUserpurchaserequest, SerializationInventorytransaction, SerializationSales, SerializationSalesRequest, SerializationTransaction, Serializationquotationrequest, Serializationquotationtransaction, Serializationsalestransaction, seralizationTblInvoicesummary


class SpSalesTransaction(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data['advancereceived']="0"
        request.data['advanceused']="0"
        serializer = SerializationSales(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                self.create_sales_transaction(
                    request.data['salesdetails'], request.data)
                return Response({"sucessfully created": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    def create_sales_transaction(self, salesdetails, requestdata):
        latestid = TblSales.objects.latest('id').id
        for salesdetails in salesdetails:
            salesdetails['date'] = requestdata['date']
            salesdetails['status'] = requestdata['status']
            salesdetails['isdeleted'] = False
            salesdetails['usedqty'] = "0"
            salesdetails['sales'] = latestid
            serializer = Serializationsalestransaction(data=salesdetails)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError(
                    'Sales transaction serialization failed', serializer.errors)
            queryset = TblSalesrequest.objects.filter(
                stockname=salesdetails['stockname'], id=salesdetails['requestid']).values()
            len_requested_id = len(queryset)
            if len_requested_id > 0:
                snippet = TblSalesrequest.objects.get(id=queryset[0]['id'])
                requested_data = {
                    "status": "AddedDispatch",
                    "Salesid": latestid
                }
                serializer = SerializationSalesRequest(
                    snippet, data=requested_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(
                        'Sales request serialization failed', serializer.errors)


class SpEditSalesTransaction(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        snippet = TblSales.objects.get(id=request.data['sales_id'])
        salesdetails_update = {
            "amount": request.data['amount'],
            "roundoff": request.data['roundoff'],
            "status": request.data['status']
        }
        serializer = SerializationSales(snippet, data=salesdetails_update)
        try:
            if serializer.is_valid():
                serializer.save()
                self.edit_sales_transaction(
                    request.data['salesdetails'], request.data)
                return Response("sucessfully created", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    def edit_sales_transaction(self, salesdetails, requestdata):
        for salesdetails in salesdetails:
            salestrasactionidvalue = TblSalestransaction.objects.filter(id=salesdetails['salestransactionid'],
                                                                        sales=requestdata['sales_id'], stockname=salesdetails['stockname']).values()
            if len(salestrasactionidvalue) <= 0:
                if salesdetails['stockname'] != 'Total':
                    salesdetails['date'] = requestdata['date']
                    salesdetails['status'] = requestdata['status']
                    salesdetails['sales'] = requestdata['sales_id']
                    salesdetails['isdeleted'] = False
                    salesdetails['usedqty'] = "0"
                    serilaizer = Serializationsalestransaction(
                        data=salesdetails)
                    if serilaizer.is_valid():
                        serilaizer.save()
                    else:
                        raise ValueError(
                            'Sales transaction serialization failed', serializer.errors)
            else:
                snippet = TblSalestransaction.objects.get(
                    id=salestrasactionidvalue[0]['id'])
                salesdetails['status'] = requestdata['status']
                serializer = Serializationsalestransaction(
                    snippet, data=salesdetails)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(
                        'Sales transaction serialization failed when sales transaction id present', serializer.errors)


class SpCreateSOwithQuotation(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.data['date'] = date.today()
        request.data['status'] = "Draft"
        request.data['advancereceived'] = "0"
        request.data['advanceused'] = "0"
        serializer = SerializationSales(data=request.data)
        print(request.data)
        try:
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError(serializer.errors,"SerializationSales failed")
            latestid = TblSales.objects.latest('id').id
            self.update_quotation_request(request.data, latestid)
            self.create_sales_order(
                request.data['salesquotationdetails'], request.data, latestid)
            self.update_status(latestid)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    def update_quotation_request(self, requestdata, latestid):
        snippet = TblQuotationrequest.objects.get(
            id=requestdata['salesquotationrequest_id'])
        quotation_data = {
            "salesorderid": latestid,
            "advancereceived": requestdata['roundoff'],
            "amount": requestdata['amount']
        }
        serializer = Serializationquotationrequest(
            snippet, data=quotation_data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError(serializer.errors,"update_quotation_request failed")

    def create_sales_order(self, quotationdetails, requestdata, latestid):
        for quotation in quotationdetails:
            quotationtransaction_id = TblQuotationtransaction.objects.filter(
                id=quotation['id'], stockname=quotation['stockname']).values('id')
            if len(quotationtransaction_id) > 0:
                snippet = TblQuotationtransaction.objects.get(
                    pk=quotationtransaction_id[0]['id'])
                quotation_update = {
                    "stockname": quotation['stockname'],
                    "productcode": quotation['productcode'],
                    "quantity": quotation['quantity'],
                    "amount": quotation['amount'],
                    "rate": quotation['rate'],
                    "cgstpercentage": quotation['cgstpercentage'],
                    "sgstpercentage": quotation['sgstpercentage'],
                    "total": quotation['total'],
                    "status": "AddedSO",
                    "salesquotation": requestdata['salesquotationrequest_id']
                }
                serilaizer = Serializationquotationtransaction(
                    snippet, data=quotation_update)
                if serilaizer.is_valid():
                    serilaizer.save()
                else:
                    raise ValueError(serilaizer.errors,"create_sales_order failed")
            else:
                quotation['date'] = date.today()
                quotation['usedqty'] = "0"
                quotation['status'] = "AddedSO"
                quotation['isdeleted'] = False
                quotation['salesquotation'] = requestdata['salesquotationrequest_id']
                serilaizer = Serializationquotationtransaction(data=quotation)
                if serilaizer.is_valid():
                    serilaizer.save()
                else:
                    raise ValueError(serilaizer.errors,"create_sales_order failed in else part")
            quotation['date'] = date.today()
            quotation['status'] = "Draft"
            quotation['isdeleted'] = False
            quotation['sales'] = latestid
            serilaizer = Serializationsalestransaction(data=quotation)
            if serilaizer.is_valid():
                serilaizer.save()
            else:
                raise ValueError(serilaizer.errors,"Serializationsalestransaction failed")

    def update_status(self, latestid):
        requested_id = TblQuotationrequest.objects.filter(
            salesorderid=latestid).values()
        if len(requested_id) > 0:
            snippet = TblQuotationrequest.objects.get(pk=requested_id[0]['id'])
            request_update = {
                "status": "AddedSO"
            }
            serilaizer = Serializationquotationrequest(
                snippet, data=request_update)
            if serilaizer.is_valid():
                serilaizer.save()
            else:
                raise ValueError(serilaizer.errors,"update_status failed")
            update_transaction = TblQuotationtransaction.objects.filter(
                salesquotation=requested_id[0]['id']).values('id')
            for id in update_transaction:
                snippet = TblQuotationtransaction.objects.get(pk=id['id'])
                transaction_update = {
                    "status": "AddedSO",
                    "sales": latestid
                }
                serilaizer = Serializationquotationtransaction(
                    snippet, data=transaction_update)
                if serilaizer.is_valid():
                    serilaizer.save()
                else:
                    raise ValueError(serilaizer.errors,"Serializationquotationtransaction failed")


class SpSalesQuotation(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = Serializationquotationrequest(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                self.sales_quotation(
                    request.data['salesdetails'], request.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    def sales_quotation(self, salesdetails, requestdata):
        latestid = TblQuotationrequest.objects.latest('id').id
        for salesdetails in salesdetails:
            salesdetails['date'] = date.today()
            salesdetails['isdeleted'] = False
            salesdetails['usedqty'] = "0"
            salesdetails['salesquotation'] = latestid
            salesdetails['status'] = requestdata['status']
            serializer = Serializationquotationtransaction(data=salesdetails)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError(serializer.errors)


class SpDeleteSalesorder(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            snippet = TblSales.objects.get(pk=request.data['sales_id'])
            sales_update = {
                "status": "Cancelled"
            }
            serializer = SerializationSales(snippet, data=sales_update)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError(serializer.errors)

            snippet_transaction = TblSalestransaction.objects.filter(
                sales=request.data['sales_id']).values('id')
            for id in snippet_transaction:
                snippet = TblSalestransaction.objects.get(pk=id['id'])
                transaction_update = {
                    "status": "Cancelled",
                    "isdeleted": True
                }
                serializer = Serializationsalestransaction(
                    snippet, data=transaction_update)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(serializer.errors)

            snippet_request = TblSalesrequest.objects.filter(
                salesid=request.data['sales_id']).values('id')
            for id in snippet_request:
                snippet = TblSalesrequest.objects.get(pk=id['id'])
                request_update = {
                    "status": "Returned",
                    "salesid": ""
                }
                serializer = SerializationSalesRequest(
                    snippet, data=request_update)
                if serializer.is_valid():
                    serializer.save()
            return Response("Deleted Successfully")

        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)


class SpCreateQuoatationwithClientDetails(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        now = datetime.now()
        currentdate = datetime.today().strftime('%Y-%m-%d')
        current_time = now.strftime("%H:%M:%S")
        for quotation in request.data['quotation']:
            sales_requet = {
                "date": currentdate,
                "time": current_time,
                "username": request.data['userid'],
                "stockname": quotation['stockname'],
                "productcode": quotation['productcode'],
                "quantity": quotation['quantity'],
                "status": "Requested",
                "description": "",
                "Salesid": "",
                "isdeleted": False,
                "clientid": request.data['clientid'],
                "companyid": request.data['companyid']

            }
            serializer = SerializationSalesRequest(data=sales_requet)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SpAddSalestockWithSalesRequest(APIView):

    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            queryset = TblSalesrequest.objects.filter(
                id=request.data['salesrequest_id']).values()
            stockname = queryset[0]['stockname']
            productcode = queryset[0]['productcode']
            quantity = queryset[0]['quantity']
            queryset = TblStock.objects.filter(stockname=stockname).values()
            cgstpercentage = queryset[0]['cgstpercentage']
            if cgstpercentage is None:
                cgstpercentage = 0
            sgstpercentage = queryset[0]['sgstpercentage']
            if sgstpercentage is None:
                sgstpercentage = 0
            sales_transaction_id = TblSalestransaction.objects.filter(
                stockname=stockname, sales=request.data['sales_id']).values('id')
            if len(sales_transaction_id) == 0:
                sales_data = {
                    "date": date.today(),
                    "stockname": stockname,
                    "productcode": productcode,
                    "quantity": quantity,
                    "status": "Draft",
                    "rate": "0",
                    "amount": "0",
                    "cgstpercentage": cgstpercentage,
                    "sgstpercentage": sgstpercentage,
                    "total": "0",
                    "sales": request.data['sales_id'],
                    "isdeleted": False,
                    "usedqty": "0"
                }
                serializer = Serializationsalestransaction(data=sales_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(serializer.errors)
            else:
                previous_quantity = TblSalestransaction.objects.filter(
                    id=sales_transaction_id[0]['id']).values('quantity')
                snippet = TblSalestransaction.objects.get(
                    pk=sales_transaction_id[0]['id'])
                update_data = {
                    "quantity": int(quantity)+int(previous_quantity[0]['quantity']),
                    "sales": request.data['sales_id']
                }
                serializer = Serializationsalestransaction(
                    snippet, data=update_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(serializer.errors)

            snippet = TblSalesrequest.objects.get(
                pk=request.data['salesrequest_id'])
            update_data = {
                "status": "AddedSO",
                "Salesid": request.data['sales_id']
            }
            serializer = SerializationSalesRequest(snippet, data=update_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)


class SpDeleteSalesStock(APIView):

    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            sales_delete_id = TblSalestransaction.objects.filter(
                id=request.data['salestransaction_id'], sales=request.data['sales_id']).values('id')
            if len(sales_delete_id) > 0:
                queryset = TblSalestransaction.objects.filter(
                    id=request.data['salestransaction_id']).values()
                stockname = queryset[0]['stockname']
                quantity = queryset[0]['quantity']
                amount = queryset[0]['amount']
                # cgstpercentage=queryset[0]['cgstpercentage']
                # sgstpercentage=queryset[0]['sgstpercentage']
                total = queryset[0]['total']
                queryset = TblSalestransaction.objects.filter(
                    stockname="Total", sales=request.data['sales_id']).values()
                total_id = queryset[0]['id']
                total_quantity = queryset[0]['quantity']
                total_amount = queryset[0]['amount']
                new_total = queryset[0]['total']

                snippet = TblSalestransaction.objects.get(pk=total_id)
                update_data = {
                    "quantity": float(total_quantity)-int(quantity),
                    "amount": int(total_amount)-int(amount),
                    "total": int(new_total)-int(total)
                }
                serializer = Serializationsalestransaction(
                    snippet, data=update_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(serializer.errors)

                snippet = TblSales.objects.get(pk=request.data['sales_id'])
                update_data = {
                    "amount": int(new_total)-int(total)
                }
                serializer = SerializationSales(snippet, data=update_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(serializer.errors)

                snippet = TblSalestransaction.objects.get(
                    id=request.data['salestransaction_id'], sales=request.data['sales_id'])
                update_data = {
                    "isdeleted": True
                }
                serializer = Serializationsalestransaction(
                    snippet, data=update_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(serializer.errors)
                try:
                    request_id = TblSalesrequest.objects.filter(
                        stockname=stockname, Salesid=request.data['sales_id']).values('id')
                    if request_id is not None:
                        snippet = TblSalesrequest.objects.get(
                            pk=request_id[0]['id'])
                        update_data = {
                            "status": "Returned"
                        }
                        serializer = SerializationSalesRequest(
                            snippet, data=update_data)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            raise ValueError(serializer.errors)
                except:
                    pass
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)


class SpMoveToDispatch(APIView):
    def post(self, request):
        queryset = TblInvoicesummary.objects.filter(
            invoice_company=request.data['company_id']).aggregate(Max('deliverynoteid'))
        company_invoice_id = queryset['deliverynoteid__max']
        if company_invoice_id == 0:
            company_invoice_id = 9999
        now = datetime.now()
        currentdate = datetime.today().strftime('%Y-%m-%d')
        current_time = now.strftime("%H:%M:%S")
        due_date = datetime.today().strftime('%Y-%m-%d')
        salesorder_details = request.data['sales_id']
        invoiceno = ""
        client_group = TblClient.objects.filter(
            id=request.data['client_id']).values('clientgroup')
        try:
            if int(request.data['advanceamount']) > 0:
                if request.data['advanceamount'] == request.data['totalamount']:
                    invoice_summary_data = {
                        "date": currentdate,
                        "invoicesummaryclientid": request.data['client_id'],
                        "client": request.data['client_id'],
                        "invoice_amount": request.data['totalamount'],
                        "amount_received": request.data['advanceamount'],
                        "invoicestatus": "Paid",
                        "discount": request.data['roundoffamount'],
                        "subtotal": int(request.data['totalamount'])+float(request.data['roundoffamount']),
                        "balancedue": int(request.data['totalamount'])-int(request.data['advanceamount']),
                        "duedate": currentdate,
                        "comments": "",
                        "originaldeliverynoteid": "0",
                        "originalcompanyid": "0",
                        "isMoved": "0",
                        "deliverynoteid": company_invoice_id+1,
                        "vehiclenumber": "",
                        "invoicetype": "Sales",
                        "salesorder": salesorder_details,
                        "invoice_company": request.data['company_id'],
                        "tbltasklistid": "",
                        "clientgroupid": client_group[0]['clientgroup'],
                        "projectid": ""
                    }
                    serializer = seralizationTblInvoicesummary(
                        data=invoice_summary_data)
                    if serializer.is_valid():
                        serializer.save()
                        self.invoice_transaction_paid(
                            request.data, currentdate, current_time, company_invoice_id, salesorder_details)
                    else:
                        raise ValueError(serializer.errors,"seralizationTblInvoicesummary failed")
                else:
                    invoice_summary_data = {
                        "date": currentdate,
                        "invoicesummaryclientid": request.data['client_id'],
                        "invoice_amount": request.data['totalamount'],
                        "amount_received": request.data['advanceamount'],
                        "invoicestatus": "Partially Paid",
                        "discount": request.data['roundoffamount'],
                        "subtotal": int(float(request.data['totalamount']))+float(request.data['roundoffamount']),
                        "balancedue": int(float(request.data['totalamount']))-int(request.data['advanceamount']),
                        "duedate": currentdate,
                        "comments": "",
                        "originaldeliverynoteid": "0",
                        "originalcompanyid": "0",
                        "isMoved": "0",
                        "deliverynoteid": company_invoice_id+1,
                        "vehiclenumber": "",
                        "invoicetype": "Sales",
                        "salesorder": salesorder_details,
                        "invoice_companyid": request.data['company_id'],
                        "tbltasklistid": "",
                        "clientgroupid": client_group,
                        "projectid": ""
                    }
                    serializer = seralizationTblInvoicesummary(
                        data=invoice_summary_data)
                    if serializer.is_valid():
                        serializer.save()
                        self.invoice_transaction_partially_paid(
                            request.data, currentdate, current_time, company_invoice_id, salesorder_details)
                    else:
                        raise ValueError(
                            serializer.errors, "seralizationTblInvoicesummary invoice_transaction_partially_paid failed")
            else:
                invoice_summary_data = {
                    "date": currentdate,
                    "invoicesummaryclientid": request.data['client_id'],
                    "invoice_amount": request.data['totalamount'],
                    "amount_received": request.data['advanceamount'],
                    "invoicestatus": "Unpaid",
                    "discount": request.data['roundoffamount'],
                    "subtotal": int(request.data['totalamount'])+float(request.data['roundoffamount']),
                    "balancedue": int(request.data['totalamount'])-int(request.data['advanceamount']),
                    "duedate": currentdate,
                    "comments": "",
                    "originaldeliverynoteid": "0",
                    "originalcompanyid": "0",
                    "isMoved": "0",
                    "deliverynoteid": company_invoice_id+1,
                    "vehiclenumber": "",
                    "invoicetype": "Sales",
                    "salesorder": salesorder_details,
                    "invoice_companyid": request.data['company_id'],
                    "tbltasklistid": "",
                    "clientgroupid": client_group,
                    "projectid": ""
                }
                serializer = seralizationTblInvoicesummary(
                    data=invoice_summary_data)
                if serializer.is_valid():
                    serializer.save()
                    self.invoice_transaction_unpaid(
                        request.data, currentdate, current_time, company_invoice_id, salesorder_details)
                else:
                    raise ValueError(serializer.errors,"seralizationTblInvoicesummary failed in else part")
            self.update_sales(request.data)
            self.sales_transaction(
                request.data['salesdata'], request.data, currentdate)
            return Response("Sales Order Has Been Moved to Dispatch ", status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    def invoice_transaction_paid(self, requestdata, currentdate, current_time, company_invoice_id, salesorder_details):
        transaction_data = {
            "transactiontaskid": "",
            "date": currentdate,
            "time": current_time,
            "description": requestdata['reference'],
            "amount": requestdata['totalamount'],
            "deliverynoteid": company_invoice_id+1,
            "originaldeliverynoteid": 0,
            "originalcompanyid": 0,
            "salesorderid": salesorder_details,
            "pmtmode": "Cash",
            "pmtreference": "",
            "transactiontype": "invoice",
            "companyid": requestdata['company_id'],
            "transaction_clientid": requestdata['client_id'],
            "userid_id": requestdata['username'],
            "voucherid":""
        }
        serializer = SerializationTransaction(data=transaction_data)
        if serializer.is_valid():
            serializer.save()
            transaction_id = TblTransaction.objects.filter(
                vouchertype="Receipt", voucherreferencetype=requestdata['sales_id'], transactiontype="ReceiptVoucher").values('id')
            if len(transaction_id) > 0:
                self.update_transaction(
                    transaction_id, requestdata, salesorder_details, company_invoice_id, current_time, currentdate)
            else:
                self.insert_transaction(
                    requestdata, currentdate, current_time, company_invoice_id, salesorder_details)
        else:
            raise ValueError(serializer.errors,
                             "invoice_transaction_paid failed")

    def update_transaction(self, transaction_id, requestdata, salesorder_details, company_invoice_id, current_time, currentdate):
        already_received_amount = TblTransaction.objects.filter(
            id=transaction_id[0]['id']).values('amount')
        balancedue = int(requestdata['advanceamount']) + \
            int(already_received_amount[0]['amount'])

        snippet = TblTransaction.objects.get(pk=transaction_id[0]['id'])
        update_data = {
            "transactiontype": "Spend",
            "salesorderid": salesorder_details,
            "deliverynoteid": company_invoice_id+1
        }
        serializer = SerializationTransaction(snippet, update_data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError(serializer.errors, "update_transaction failed")

        transaction_data_received = {
            "transactiontaskid": "",
            "transaction_clientid": requestdata['client_id'],
            "userid_id": requestdata['username'],
            "amount": balancedue,
            "deliverynoteid": company_invoice_id+1,
            "description": requestdata['reference'],
            "time": current_time,
            "transactiontype": "Received",
            "date": currentdate,
            "companyid": requestdata['company_id'],
            "originaldeliverynoteid": 0,
            "originalcompanyid": 0,
            "pmtmode": "Cash",
            "pmtreference": "",
            "salesorderid": salesorder_details,
            "voucherid":"",
        }
        serializer = SerializationTransaction(data=transaction_data_received)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError(serializer.errors,
                             "transaction data received failed")

        transaction_data_spend = {
            "transactiontaskid": "",
            "transaction_clientid": requestdata['client_id'],
            "userid_id": requestdata['username'],
            "amount": balancedue,
            "deliverynoteid": company_invoice_id+1,
            "description": requestdata['reference'],
            "time": current_time,
            "transactiontype": "Spend",
            "date": currentdate,
            "companyid": requestdata['company_id'],
            "originaldeliverynoteid": 0,
            "originalcompanyid": 0,
            "pmtmode": "Cash",
            "pmtreference": "",
            "salesorderid": salesorder_details,
            "voucherid":"",
        }
        serializer = SerializationTransaction(data=transaction_data_spend)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError(serializer.errors,
                             "transaction data spend failed")

    def insert_transaction(self, requestdata, currentdate, current_time, company_invoice_id, salesorder_details):

        transaction_data_received = {
            "transactiontaskid": "",
            "transaction_clientid": requestdata['client_id'],
            "userid_id": requestdata['username'],
            "amount": requestdata['advanceamount'],
            "deliverynoteid": company_invoice_id+1,
            "description": requestdata['reference'],
            "time": current_time,
            "transactiontype": "Received",
            "date": currentdate,
            "companyid": requestdata['company_id'],
            "originaldeliverynoteid": 0,
            "originalcompanyid": 0,
            "pmtmode": "Cash",
            "pmtreference": "",
            "salesorderid": salesorder_details,
            "voucherid":"",
        }
        serializer = SerializationTransaction(data=transaction_data_received)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError(
                serializer.errors, "insert_transaction transaction data received failed")

        transaction_data_spend = {
            "transactiontaskid": "",
            "transaction_clientid": requestdata['client_id'],
            "clientname": requestdata['client_id'],
            "userid_id": requestdata['username'],
            "amount": requestdata['advanceamount'],
            "deliverynoteid": company_invoice_id+1,
            "description": requestdata['reference'],
            "time": current_time,
            "transactiontype": "Spend",
            "date": currentdate,
            "companyid": requestdata['company_id'],
            "originaldeliverynoteid": 0,
            "originalcompanyid": 0,
            "pmtmode": "Cash",
            "pmtreference": "",
            "salesorderid": salesorder_details,
            "voucherid":"",
        }
        serializer = SerializationTransaction(data=transaction_data_spend)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError(
                serializer.errors, "insert_transaction transaction data spend failed")
        #return Response(serializer.data, status=status.HTTP_201_CREATED)

    def invoice_transaction_partially_paid(self, requestdata, currentdate, current_time, company_invoice_id, salesorder_details):
        transaction_data = {
            "transactiontaskid": "",
            "date": currentdate,
            "time": current_time,
            "description": requestdata['reference'],
            "amount": requestdata['totalamount'],
            "deliverynoteid": company_invoice_id+1,
            "originaldeliverynoteid": 0,
            "originalcompanyid": 0,
            "salesorderid": salesorder_details,
            "pmtmode": "Cash",
            "pmtreference": "",
            "transactiontype": "invoice",
            "companyid": requestdata['company_id'],
            "transaction_clientid": requestdata['client_id'],
            "userid_id": requestdata['username'],
            "voucherid":"",
        }
        serializer = SerializationTransaction(data=transaction_data)
        if serializer.is_valid():
            serializer.save()
            transaction_id = TblTransaction.objects.filter(
                vouchertype="Receipt", voucherreferencetype=requestdata['sales_id'], transactiontype="ReceiptVoucher").values('id')
            if len(transaction_id) > 0:
                self.update_transaction_partially_paid(
                    transaction_id, requestdata, salesorder_details, company_invoice_id, current_time, currentdate)
            else:
                self.insert_transaction_partially_paid(
                    requestdata, currentdate, current_time, company_invoice_id, salesorder_details)
        else:
            raise ValueError(serializer.errors,
                             "invoice_transaction_partially_paid failed")

    def update_transaction_partially_paid(self, transaction_id, requestdata, salesorder_details, company_invoice_id, current_time, currentdate):
        if len(transaction_id) > 0:
            already_received_amount = TblTransaction.objects.filter(
                id=transaction_id[0]['id']).values('amount')
            balancedue = int(requestdata['advanceamount']) + \
                int(already_received_amount[0]['amount'])

            snippet = TblTransaction.objects.get(pk=transaction_id[0]['id'])
            update_data = {
                "transactiontype": "Spend",
                "salesorderid": salesorder_details,
                "deliverynoteid": company_invoice_id+1
            }
            serializer = SerializationTransaction(snippet, update_data)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError(serializer.errors,
                                 "update_transaction_partially_paid failed")

            transaction_data_received = {
                "transactiontaskid": "",
                "transaction_clientid": requestdata['client_id'],
                "userid_id": requestdata['username'],
                "amount": balancedue,
                "deliverynoteid": company_invoice_id+1,
                "description": requestdata['reference'],
                "time": current_time,
                "transactiontype": "Received",
                "date": currentdate,
                "companyid": requestdata['company_id'],
                "originaldeliverynoteid": 0,
                "originalcompanyid": 0,
                "pmtmode": "Cash",
                "pmtreference": "",
                "salesorderid": salesorder_details,
                "voucherid":"",
            }
            serializer = SerializationTransaction(
                data=transaction_data_received)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError(
                    serializer.errors, "update_transaction_partially_paid transaction_data_received failed")
            transaction_data_spend = {
                "transactiontaskid": "",
                "transaction_clientid": requestdata['client_id'],
                "userid_id": requestdata['username'],
                "amount": balancedue,
                "deliverynoteid": company_invoice_id+1,
                "description": requestdata['reference'],
                "time": current_time,
                "transactiontype": "Spend",
                "date": currentdate,
                "companyid": requestdata['company_id'],
                "originaldeliverynoteid": 0,
                "originalcompanyid": 0,
                "pmtmode": "Cash",
                "pmtreference": "",
                "salesorderid": salesorder_details,
            "voucherid":"",
            }
            serializer = SerializationTransaction(data=transaction_data_spend)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError(
                    serializer.errors, "update_transaction_partially_paid transaction_data_spend failed")

    def insert_transaction_partially_paid(self, requestdata, currentdate, current_time, company_invoice_id, salesorder_details):
        transaction_data_received = {
            "transactiontaskid": "",
            "transaction_clientid": requestdata['client_id'],
            "userid_id": requestdata['username'],
            "amount": requestdata['advanceamount'],
            "deliverynoteid": company_invoice_id+1,
            "description": requestdata['reference'],
            "time": current_time,
            "transactiontype": "Received",
            "date": currentdate,
            "companyid": requestdata['company_id'],
            "originaldeliverynoteid": 0,
            "originalcompanyid": 0,
            "pmtmode": "Cash",
            "pmtreference": "",
            "salesorderid": salesorder_details,
            "voucherid":"",
        }
        serializer = SerializationTransaction(data=transaction_data_received)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError(
                serializer.errors, "insert_transaction_partially_paid transaction_data_received failed")

        transaction_data_spend = {
            "transactiontaskid": "",
            "transaction_clientid": requestdata['client_id'],
            "userid_id": requestdata['username'],
            "amount": requestdata['advanceamount'],
            "deliverynoteid": company_invoice_id+1,
            "description": requestdata['reference'],
            "time": current_time,
            "transactiontype": "Spend",
            "date": currentdate,
            "companyid": requestdata['company_id'],
            "originaldeliverynoteid": 0,
            "originalcompanyid": 0,
            "pmtmode": "Cash",
            "pmtreference": "",
            "salesorderid": salesorder_details,
            "voucherid":"",
        }
        serializer = SerializationTransaction(data=transaction_data_spend)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError(
                serializer.errors, "insert_transaction_partially_paid transaction_data_spend failed ")

    def invoice_transaction_unpaid(self, requestdata, currentdate, current_time, company_invoice_id, salesorder_details):
        transaction_data = {
            "transactiontaskid": "",
            "date": currentdate,
            "time": current_time,
            "description": requestdata['reference'],
            "amount": requestdata['totalamount'],
            "deliverynoteid": company_invoice_id+1,
            "originaldeliverynoteid": 0,
            "originalcompanyid": 0,
            "salesorderid": salesorder_details,
            "pmtmode": "Cash",
            "pmtreference": "",
            "transactiontype": "invoice",
            "companyid": requestdata['company_id'],
            "transaction_clientid": requestdata['client_id'],
            "userid_id": requestdata['username'],
            "voucherid":"",
        }
        serializer = SerializationTransaction(data=transaction_data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError(serializer.errors,
                             "invoice_transaction_unpaid failed")

    def update_sales(self, requestdata):
        snippet = TblSales.objects.get(pk=requestdata['sales_id'])
        update_dict = {
            "amount": requestdata['totalamount'],
            "roundoff": requestdata['roundoffamount'],
            "status": requestdata['editstatus']
        }
        serializer = SerializationSales(snippet, data=update_dict)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError(serializer.errors, "update_sales failed")

    def sales_transaction(self, salesdata, requestdata, currentdate):
        invoice_no = TblInvoicesummary.objects.latest('id').id
        sales_details = []
        for salesdetails in salesdata:
            sales_transaction_id = TblSalestransaction.objects.filter(id=salesdetails['salestransaction_id'],
                                                                      sales=requestdata['sales_id'],
                                                                      stockname=salesdetails['stockname']).values('id')
            if len(sales_transaction_id) == 0:
                sales_transaction_data = {
                    "date": currentdate,
                    "stockname": salesdetails['stockname'],
                    "productcode": salesdetails['productcode'],
                    "quantity": salesdetails['quantity'],
                    "status": requestdata['editstatus'],
                    "rate": salesdetails['rate'],
                    "amount": salesdetails['amount'],
                    "cgstpercentage": salesdetails['cgstpercentage'],
                    "sgstpercentage": salesdetails['sgstpercentage'],
                    "total": salesdetails['total'],
                    "sales": requestdata['sales_id'],
                    "isdeleted": False,
                    "usedqty": 0,
                    "task_invoiceno": invoice_no
                }
                serializer = Serializationsalestransaction(
                    data=sales_transaction_data)
                if serializer.is_valid():
                    serializer.save()
                    sales_details.append(salesdetails)
                else:
                    raise ValueError(serializer.errors,
                                     "sales_transaction failed")
            else:
                snippet = TblSalestransaction.objects.get(
                    pk=sales_transaction_id[0]['id'])
                update_data = {
                    "stockname": salesdetails['stockname'],
                    "productcode": salesdetails['productcode'],
                    "quantity": salesdetails['quantity'],
                    "status": requestdata['editstatus'],
                    "rate": salesdetails['rate'],
                    "amount": salesdetails['amount'],
                    "cgstpercentage": salesdetails['cgstpercentage'],
                    "sgstpercentage": salesdetails['sgstpercentage'],
                    "total": salesdetails['total'],
                    "task_invoiceno": invoice_no
                }
                serializer = Serializationsalestransaction(
                    snippet, data=update_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(serializer.errors,
                                     "update sales transaction failed")
        return Response(sales_details, status=status.HTTP_201_CREATED)


class SpDispatchHandling(APIView):
    def post(self, request):
        try:
            for inventory in request.data['inventorydata']:
                temp_stockbatch_details = TblInventorytransaction.objects.values(
                    'stockname', 'batch', 'purchaseinvoice').filter(quantity__gt=0,stockname=inventory['stockname']).annotate(totalquantity=Sum('quantity'))
                #print(temp_stockbatch_details,"temp_stockbatch_details")
                data_count = len(temp_stockbatch_details)
                #print(data_count,"data count")
                if inventory['orderquantity'] == inventory['quantity']:
                    if data_count > 0:
                        already_received_qty = TblSalestransaction.objects.filter(
                            stockname=inventory['stockname'], id=inventory['salesstock_id']).values('usedqty')
                        snippet = TblSalestransaction.objects.get(
                            pk=inventory['salesstock_id'], stockname=inventory['stockname'])
                        update_data = {
                            "status": "Dispatched",
                            "usedqty": int(already_received_qty[0]['usedqty'])+int(inventory['quantity'])
                        }
                        serializer = Serializationsalestransaction(
                            snippet, data=update_data)
                        if serializer.is_valid():
                            # serializer.validated_data
                            serializer.save()
                            # return Response(serializer.data,status=status.HTTP_201_CREATED)
                else:
                    if data_count > 0:
                        already_received_qty = TblSalestransaction.objects.filter(
                            stockname=inventory['stockname'], id=inventory['salesstock_id']).values('usedqty')
                        snippet = TblSalestransaction.objects.get(
                            pk=inventory['salesstock_id'], stockname=inventory['stockname'])
                        update_data = {
                            "status": "Partially Dispatched",
                            "usedqty": int(already_received_qty[0]['usedqty'])+int(inventory['quantity'])
                        }
                        serializer = Serializationsalestransaction(
                            snippet, data=update_data)
                        if serializer.is_valid():
                            # serializer.validated_data
                            serializer.save()
                            # return Response(serializer.data,status=status.HTTP_201_CREATED)
                id = 0
                while int(inventory['quantity']) > 0:
                    if id < data_count:
                        queryset = temp_stockbatch_details.aggregate(
                            Min('purchaseinvoice'))
                        invoice_id = queryset['purchaseinvoice__min']
                        batch = temp_stockbatch_details.filter(
                            purchaseinvoice=invoice_id).values('batch')
                        batch_quantity = temp_stockbatch_details.filter(
                            purchaseinvoice=invoice_id).values('totalquantity')
                        if int(batch_quantity[0]['totalquantity']) >= int(inventory['quantity']):
                            dynamic_total = int(
                                inventory['quantity'])*int(inventory['rate'])
                            cgst = (dynamic_total +
                                    int(inventory['cgstpercentage'])/100)
                            sgst = (dynamic_total +
                                    int(inventory['sgstpercentage'])/100)
                            inventory_transaction_data = {
                                "date": request.data['dispatchdate'],
                                "username": request.data['userid'],
                                "stockname": inventory['stockname'],
                                "productcode": inventory['productcode'],
                                "quantity": (-int(inventory['quantity'])),
                                "rate": inventory['rate'],
                                "amount": int(inventory['quantity'])*int(inventory['rate']),
                                "cgstpercentage": inventory['cgstpercentage'],
                                "sgstpercentage": inventory['sgstpercentage'],
                                "total": round(dynamic_total+cgst+sgst),
                                "batch": batch[0]['batch'],
                                "location": 0,
                                "status": "Sales",
                                "invoiceno": 0,
                                "purchaseorderid": 0,
                                "length": 0,
                                "purchaseinvoice": invoice_id,
                                "salesid": request.data['salesorder_id']
                            }
                            serializer = SerializationInventorytransaction(
                                data=inventory_transaction_data)
                            if serializer.is_valid():
                                # serializer.validated_data
                                serializer.save()
                                inventory['quantity'] = 0
                            else:
                                raise ValueError(
                                    serializer.errors, "inventory_transaction_data failed")
                        else:
                            dynamic_total = int(
                                inventory['quantity'])*int(inventory['rate'])
                            cgst = (dynamic_total +
                                    int(inventory['cgstpercentage'])/100)
                            sgst = (dynamic_total +
                                    int(inventory['sgstpercentage'])/100)
                            inventory_transaction_data = {
                                "date": request.data['dispatchdate'],
                                "username": request.data['userid'],
                                "stockname": inventory['stockname'],
                                "productcode": inventory['productcode'],
                                "quantity": (-int(batch_quantity[0]['totalquantity'])),
                                "rate": inventory['rate'],
                                "amount": int(inventory['quantity'])*int(inventory['rate']),
                                "cgstpercentage": inventory['cgstpercentage'],
                                "sgstpercentage": inventory['sgstpercentage'],
                                "total": round(dynamic_total+cgst+sgst),
                                "batch": batch[0]['batch'],
                                "location": 0,
                                "status": "Sales",
                                "invoiceno": 0,
                                "purchaseorderid": 0,
                                "length": 0,
                                "purchaseinvoice": invoice_id,
                                "salesid": request.data['salesorder_id']
                            }
                            serializer = SerializationInventorytransaction(
                                data=inventory_transaction_data)
                            if serializer.is_valid():
                                # serializer.validated_data
                                serializer.save()
                                inventory['quantity'] = int(
                                    inventory['quantity'])-int(batch_quantity[0]['totalquantity'])
                                # instance=temp_stockbatch_details.filter(purchaseinvoice=invoice_id).delete()
                                # instance.delete()
                            else:
                                raise ValueError(
                                    serializer.errors, "inventory_transaction_data failed in else part")
                        id += 1
                    else:
                        now = datetime.now()
                        currentdate = datetime.today().strftime('%Y-%m-%d')
                        current_time = now.strftime("%H:%M:%S")
                        purchase_user_request = {
                            "date": currentdate,
                            "time": current_time,
                            "username": request.data['userid'],
                            "stockname": inventory['stockname'],
                            "productcode": inventory['productcode'],
                            "quantity": inventory['quantity'],
                            "status": "Requested",
                            "description": "",
                            "purchaseorderid": "",
                            "isdeleted": False
                        }
                        serializer = SerializarionUserpurchaserequest(
                            data=purchase_user_request)
                        if serializer.is_valid():
                            # serializer.validated_data
                            serializer.save()
                            inventory['quantity'] = 0
                        else:
                            raise ValueError(
                                serializer.errors, "inventory_transaction_data failed while quantity less tahn zero")
            queryset = TblSalestransaction.objects.filter(Q(sales=request.data['salesorder_id']), (~Q(
                stockname='Total')), (Q(isdeleted=False))).aggregate(Sum('quantity'))
            sales_order_total_qty = queryset['quantity__sum']
            queryset = TblSalestransaction.objects.filter(Q(sales=request.data['salesorder_id']), (~Q(
                stockname='Total')), (Q(isdeleted=False))).aggregate(Sum('usedqty'))
            sales_order_received_qty = queryset['usedqty__sum']
            queryset = TblSales.objects.filter(
                id=request.data['salesorder_id']).aggregate(Sum('advanceused'))
            sales_order_advance_used = queryset['advanceused__sum']
            if sales_order_advance_used is None:
                sales_order_advance_used = 0
            if sales_order_total_qty == sales_order_received_qty:
                if int(float(request.data['totalamount'])) > int(float(request.data['advanceamount'])):
                    snippet = TblSales.objects.get(
                        id=request.data['salesorder_id'])
                    update_data = {
                        "status": "Dispatched",
                        "reference": request.data['reference'],
                        "advanceused": sales_order_advance_used+int(float(request.data['advanceamount'])),
                        "deliveryaddress": request.data['deliveryaddress']
                    }
                    serializer = SerializationSales(snippet, data=update_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        raise ValueError(serializer.errors,
                                         "SerializationSales failed")

                else:
                    snippet = TblSales.objects.get(
                        id=request.data['salesorder_id'])
                    update_data = {
                        "status": "Dispatched",
                        "reference": request.data['reference'],
                        "advanceused": sales_order_advance_used+int(float(request.data['totalamount'])),
                        "deliveryaddress": request.data['deliveryaddress']
                    }
                    serializer = SerializationSales(snippet, data=update_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        raise ValueError(
                            serializer.errors, "SerializationSales failed in else part")
            else:
                if int(float(request.data['totalamount'])) > int(float(request.data['advanceamount'])):
                    snippet = TblSales.objects.get(
                        id=request.data['salesorder_id'])
                    update_data = {
                        "status": "Partially Dispatched",
                        "reference": request.data['reference'],
                        "advanceused": sales_order_advance_used+int(float(request.data['advanceamount'])),
                        "deliveryaddress": request.data['deliveryaddress']
                    }
                    serializer = SerializationSales(snippet, data=update_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        raise ValueError(
                            serializer.errors, "SerializationSales failed while toatal amount is lesser")
                else:
                    snippet = TblSales.objects.get(
                        id=request.data['salesorder_id'])
                    update_data = {
                        "status": "Partially Dispatched",
                        "reference": request.data['reference'],
                        "advanceused": sales_order_advance_used+int(float(request.data['totalamount'])),
                        "deliveryaddress": request.data['deliveryaddress']
                    }
                    serializer = SerializationSales(snippet, data=update_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        raise ValueError(
                            serializer.errors, "SerializationSales failed SerializationSales failed while toatal amount is lesser else part")

        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)
