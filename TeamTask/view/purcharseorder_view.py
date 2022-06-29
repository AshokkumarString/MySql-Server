from rest_framework.response import Response
from TeamTask.models import TblCompany, TblPurchaseUserrequest, TblPurchasebillinvoice, TblPurchaseorder, \
    TblPurchasestocks, TblStock
from TeamTask.serialization import SerializarionPurchasestocks, SerializarionUserpurchaserequest, \
    SerializationInventorytransaction, SerializationPurchaseInvocie, SerializationPurchaseorder
from django.db.models import Sum, Q
from rest_framework import status
from rest_framework.views import APIView
from datetime import date, datetime
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class SpPurchaseOrder(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.data['advancepaid'] = "0"
        request.data['advanceused'] = "0"
        serializer = SerializationPurchaseorder(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                self.create_purchase_order(
                    request.data['stockdetails'], request.data)
                return Response({"sucessfully created": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    def create_purchase_order(self, stockdetails, requestdata):
        latestid = TblPurchaseorder.objects.latest('id').id
        for stockdetails in stockdetails:
            stockdetails['date'] = requestdata['date']
            stockdetails['purchasesorderid'] = latestid
            serializer_stock = SerializarionPurchasestocks(data=stockdetails)
            if serializer_stock.is_valid():
                serializer_stock.save()
            else:
                raise ValueError(
                    'purchase stock serilaization failed', serializer_stock.errors)

            if stockdetails['type'] == 'Requested':
                snippet = TblPurchaseUserrequest.objects.get(
                    pk=stockdetails['requestid'])
                userrequest = {
                    "purchaseorderid": latestid,
                    "status": "AddedPO"
                }
                serializer_request = SerializarionUserpurchaserequest(
                    snippet, data=userrequest)
                if serializer_request.is_valid():
                    serializer_request.save()
                else:
                    raise ValueError(
                        'purchase request serilaization failed', serializer_request.errors)


class SpUpdatePurchaseOrder(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        snippet = TblPurchaseorder.objects.get(pk=request.data['purchaseid'])
        serializer = SerializationPurchaseorder(snippet, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                self.update_purchase_order(
                    request.data['stockdetails'], request.data)
                return Response("sucessfully created", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    def update_purchase_order(self, stockdetails, requestdata):
        for stockdetails in stockdetails:
            stockdetails['purchasesorderid'] = requestdata['purchaseid']
            hsncode = TblStock.objects.filter(
                stockname=stockdetails['name']).values('hsncode')
            alreadythere = TblPurchasestocks.objects.filter(id=stockdetails['stockid'],
                                                            purchasesorderid=requestdata['purchaseid']).values()
            if len(alreadythere) <= 0:
                stockdetails['date'] = date.today()
                stockdetails['hsncode'] = hsncode[0]['hsncode']
                serializer_stock = SerializarionPurchasestocks(
                    data=stockdetails)
                if serializer_stock.is_valid():
                    serializer_stock.save()
                else:
                    raise ValueError(
                        'purchase stock serilaization failed', serializer_stock.errors)
            else:
                snippet = TblPurchasestocks.objects.get(
                    pk=stockdetails['stockid'])
                purchasestock = {
                    "date": date.today(),
                    "name": stockdetails['name'],
                    "productcode": stockdetails['productcode'],
                    "quantity": stockdetails['quantity'],
                    "rate": stockdetails['rate'],
                    "amount": stockdetails['amount'],
                    "cgstdiscount": stockdetails['cgstdiscount'],
                    "sgstdiscount": stockdetails['sgstdiscount'],
                    "cgstdiscountpercentage": stockdetails['cgstdiscountpercentage'],
                    "sgstdiscountpercentage": stockdetails['sgstdiscountpercentage'],
                    "gsttype": requestdata['gsttype'],
                    "total": stockdetails['total'],
                    "status": requestdata['status'],
                    "purchasesorderid": requestdata['purchaseid']

                }
                serializer_stock_update = SerializarionPurchasestocks(
                    snippet, data=purchasestock)
                if serializer_stock_update.is_valid():
                    serializer_stock_update.save()
                else:
                    raise ValueError(
                        'purchase stock serilaization failed', serializer_stock.errors)


class SpCreatePOwithUserRequest(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data['date'] = date.today()
        request.data['total'] = "0"
        request.data['payment'] = "Cash"
        request.data['advancepaid'] = "0"
        request.data['advanceused'] = "0"
        request.data['status'] = "Draft"
        request.data['roundoff'] = "0"
        request.data['isdeleted'] = False
        serializer = SerializationPurchaseorder(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                self.purchase_user_request(
                    request.data['stockdetails'], request.data)
                self.insert_total(request.data)
                return Response({"sucessfully created": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    def purchase_user_request(self, stockdetails, requestdata):
        latestid = TblPurchaseorder.objects.latest('id').id
        isgst = TblCompany.objects.filter(
            id=requestdata['companyid']).values('isgst')
        for stockdetails in stockdetails:
            queryset = TblStock.objects.filter(
                stockname=stockdetails['stockname']).values()
            cgstpercentage = queryset[0]['cgstpercentage']
            sgstpercentage = queryset[0]['sgstpercentage']
            hsncode = queryset[0]['hsncode']
            if isgst == True:
                cgstpercentage = cgstpercentage
                sgstpercentage = sgstpercentage
            else:
                cgstpercentage = 0
                sgstpercentage = 0
            snippet = TblPurchaseUserrequest.objects.get(
                pk=stockdetails['requestedid'])
            userrequest = {
                "status": "AddedPO",
                "purchaseorderid": latestid
            }
            serializer_user_request = SerializarionUserpurchaserequest(
                snippet, data=userrequest)
            if serializer_user_request.is_valid():
                serializer_user_request.save()
            else:
                raise ValueError(
                    'Can not create purchase order from user request', serializer_user_request.errors)
            stockdata = {
                "total": "0",
                "date": requestdata['date'],
                "name": stockdetails['stockname'],
                "quantity": stockdetails['quantity'],
                "rate": "0",
                "amount": "0",
                "cgstdiscount": "0",
                "sgstdiscount": "0",
                "cgstdiscountpercentage": cgstpercentage,
                "sgstdiscountpercentage": sgstpercentage,
                "gsttype": "sgst",
                "total": "0",
                "isdeleted": False,
                "status": "Draft",
                "received": "0",
                "remaining": "0",
                "invoiceno": "0",
                "hsncode": hsncode,
                "purchasesorderid": latestid
            }
            serializer_stocks = SerializarionPurchasestocks(data=stockdata)
            if serializer_stocks.is_valid():
                serializer_stocks.save()
            else:
                raise ValueError(
                    'purchase stock serilaization failed', serializer_stocks.errors)

    def insert_total(self, requestdata):
        latestid = TblPurchaseorder.objects.latest('id').id
        queryset = TblPurchasestocks.objects.filter(
            purchasesorderid=latestid).aggregate(Sum('quantity'))
        total_quantity = queryset['quantity__sum']
        stockdata_total = {
            "total": "0",
            "date": requestdata['date'],
            "name": "Total",
            "quantity": total_quantity,
            "rate": "0",
            "amount": "0",
            "cgstdiscount": "0",
            "sgstdiscount": "0",
            "cgstdiscountpercentage": "0",
            "sgstdiscountpercentage": "0",
            "total": "0",
            "isdeleted": False,
            "received": "0",
            "remaining": "0",
            "invoiceno": "0",
            "purchasesorderid": latestid
        }
        serializer_stocks_total = SerializarionPurchasestocks(
            data=stockdata_total)
        if serializer_stocks_total.is_valid():
            serializer_stocks_total.save()
        return Response(serializer_stocks_total.errors, status=status.HTTP_400_BAD_REQUEST)


class SpDeletePurchaseOrder(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            snippet = TblPurchaseorder.objects.get(
                pk=request.data["purchaseorderid"])
            purchaseorder = {
                "status": "Cancelled",
                "isdeleted": True
            }
            serializer = SerializationPurchaseorder(
                snippet, data=purchaseorder)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError(serializer.errors)

            snippet_stocks = TblPurchasestocks.objects.filter(
                purchasesorderid=request.data["purchaseorderid"]).values('id')
            for id in snippet_stocks:
                snippet = TblPurchasestocks.objects.get(pk=id['id'])
                purchasestock = {
                    "status": "Cancelled",
                    "isdeleted": True,
                    "purchasesorderid": request.data['purchaseorderid']
                }
                serializer_stocks = SerializarionPurchasestocks(
                    snippet, data=purchasestock)
                if serializer_stocks.is_valid():
                    serializer_stocks.save()
                else:
                    raise ValueError(serializer_stocks.errors)

            snippet_request = TblPurchaseUserrequest.objects.filter(
                purchaseorderid=request.data["purchaseorderid"]).values('id')
            for id in snippet_request:
                snippet = TblPurchaseUserrequest.objects.get(pk=id['id'])
                purchaserequest = {
                    "status": "Returned",
                    "purchaseorderid": ""
                }
                serializer_request = SerializarionUserpurchaserequest(
                    snippet, data=purchaserequest)
                if serializer_request.is_valid():
                    serializer_request.save()
                else:
                    raise ValueError(serializer_request.errors)
            return Response("Deleted Sucessfully", status=status.HTTP_200_OK)
            # return Response({"Didn't Create Purchase order from Purchase Request":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)


class SpReceiptHandling(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            self.advance_amount(request.data)
            self.purchase_stock(request.data['inventorydetails'], request.data)
            queryset = TblPurchasestocks.objects.filter(Q(purchasesorderid=request.data['purchaseorderid']),
                                                        (~Q(name="Total"))).aggregate(Sum('quantity'))
            purchase_order_total_qty = queryset['quantity__sum']
            queryset = TblPurchasestocks.objects.filter(Q(purchasesorderid=request.data['purchaseorderid']),
                                                        (~Q(name="Total"))).aggregate(Sum('received'))
            purchase_order_received_qty = queryset['received__sum']
            purchaseorderadvanceused = TblPurchaseorder.objects.filter(id=request.data['purchaseorderid']).values(
                'advanceused')
            snippet = TblPurchasestocks.objects.get(
                purchasesorderid=request.data['purchaseorderid'], name='Total')
            total_update_data = {
                "received": int(purchase_order_received_qty),
                "purchasesorderid": request.data['purchaseorderid']
            }
            serializer = SerializarionPurchasestocks(
                snippet, data=total_update_data)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError(serializer.errors)
            if int(purchase_order_total_qty) == int(purchase_order_received_qty):
                if int(request.data['totalamount']) > int(request.data['advanceamount']):
                    snippet = TblPurchaseorder.objects.get(
                        pk=request.data['purchaseorderid'])
                    update_data = {
                        "status": "Received",
                        "advanceused": int(purchaseorderadvanceused[0]['advanceused']) + request.data['advanceamount']
                    }
                    serializer = SerializationPurchaseorder(
                        snippet, data=update_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    return Response(serializer.errors)
                else:
                    snippet = TblPurchaseorder.objects.get(
                        pk=request.data['purchaseorderid'])
                    update_data = {
                        "status": "Received",
                        "advanceused": int(purchaseorderadvanceused[0]['advanceused']) + request.data['totalamount']
                    }
                    serializer = SerializationPurchaseorder(
                        snippet, data=update_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    return Response(serializer.errors)
            else:
                if int(request.data['totalamount']) > int(request.data['advanceamount']):
                    snippet = TblPurchaseorder.objects.get(
                        pk=request.data['purchaseorderid'])
                    update_data = {
                        "status": "Partially Received",
                        "advanceused": int(purchaseorderadvanceused[0]['advanceused']) + int(
                            request.data['advanceamount'])
                    }
                    serializer = SerializationPurchaseorder(
                        snippet, data=update_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    return Response(serializer.errors)
                else:
                    snippet = TblPurchaseorder.objects.get(
                        pk=request.data['purchaseorderid'])
                    update_data = {
                        "status": "Partially Received",
                        "advanceused": int(purchaseorderadvanceused[0]['advanceused']) + int(
                            request.data['totalamount'])
                    }
                    serializer = SerializationPurchaseorder(
                        snippet, data=update_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    def advance_amount(self, requestdata):
        if int(requestdata['advanceamount']) > 0:
            if int(requestdata['advanceamount']) > int(requestdata['totalamount']):
                purchase_bill_invoice = {
                    "date": requestdata['receiptdate'],
                    "purchaseinvoiceno": requestdata['invoiceno'],
                    "supplier": requestdata['supplier'],
                    "company": requestdata['company'],
                    "amount": requestdata['totalamount'],
                    "reference": requestdata['reference'],
                    "roundoff": requestdata['roundoff'],
                    "status": "Paid",
                    "amountreceived": requestdata['totalamount'],
                    "invoicedate": requestdata['invoicedate']
                }
                serializer = SerializationPurchaseInvocie(
                    data=purchase_bill_invoice)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(serializer.errors)

            else:
                purchase_bill_invoice = {
                    "date": requestdata['receiptdate'],
                    "purchaseinvoiceno": requestdata['invoiceno'],
                    "supplier": requestdata['supplier'],
                    "company": requestdata['company'],
                    "amount": requestdata['totalamount'],
                    "reference": requestdata['reference'],
                    "roundoff": requestdata['roundoff'],
                    "status": "Partially Paid",
                    "amountreceived": requestdata['advanceamount'],
                    "invoicedate": requestdata['invoicedate']
                }
                serializer = SerializationPurchaseInvocie(
                    data=purchase_bill_invoice)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(serializer.errors)
        else:
            purchase_bill_invoice = {
                "date": requestdata['receiptdate'],
                "purchaseinvoiceno": requestdata['invoiceno'],
                "supplier": requestdata['supplier'],
                "company": requestdata['company'],
                "amount": requestdata['totalamount'],
                "reference": requestdata['reference'],
                "roundoff": requestdata['roundoff'],
                "status": "UnPaid",
                "amountreceived": requestdata['advanceamount'],
                "invoicedate": requestdata['invoicedate']
            }
            serializer = SerializationPurchaseInvocie(
                data=purchase_bill_invoice)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError(serializer.errors)

    def purchase_stock(self, inventory, requestdata):
        latestid = TblPurchasebillinvoice.objects.latest('id').id
        order_id = requestdata['purchaseorderid']
        for inventorydetails in inventory:
            hsncode = TblStock.objects.filter(
                stockname=inventorydetails['stockname']).values('hsncode')
            inventory_data = {
                "date": requestdata['receiptdate'],
                "username": requestdata['userid'],
                "stockname": inventorydetails['stockname'],
                "productcode": inventorydetails['productcode'],
                "quantity": inventorydetails['quantity'],
                "rate": inventorydetails['rate'],
                "amount": inventorydetails['amount'],
                "cgstpercentage": inventorydetails['cgstpercentage'],
                "sgstpercentage": inventorydetails['sgstpercentage'],
                "total": inventorydetails['total'],
                "invoiceno": requestdata['invoiceno'],
                "purchaseorderid": order_id,
                "purchaseinvoice": latestid,
                "length": "0",
                "location": inventorydetails['location'],
                "batch": inventorydetails['batch'],
                "hsncode": hsncode[0]['hsncode'],
                "status": "Received",
                "invoice_company": requestdata['company']
            }
            serializer = SerializationInventorytransaction(data=inventory_data)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError(serializer.errors)
            if int(inventorydetails['orderquantity']) == int(inventorydetails['quantity']):
                already_received_qty = TblPurchasestocks.objects.filter(id=inventorydetails['purchasestockid']).values(
                    'received')
                snippet = TblPurchasestocks.objects.get(
                    pk=inventorydetails['purchasestockid'])
                update_data = {
                    "status": "Received",
                    "received": int(already_received_qty[0]['received']) + int(inventorydetails['quantity']),
                    "purchasesorderid": requestdata['purchaseorderid']
                }
                serializer = SerializarionPurchasestocks(
                    snippet, data=update_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(serializer.errors)
            else:
                already_received_qty = TblPurchasestocks.objects.filter(id=inventorydetails['purchasestockid']).values(
                    'received')
                snippet = TblPurchasestocks.objects.get(
                    pk=inventorydetails['purchasestockid'])
                update_data = {
                    "status": "Partially Received",
                    "received": int(already_received_qty[0]['received']) + int(inventorydetails['quantity']),
                    "purchasesorderid": requestdata['purchaseorderid']
                }
                serializer = SerializarionPurchasestocks(
                    snippet, data=update_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(serializer.errors)


class SpCreatePurchaseStock(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            queryset = TblPurchaseUserrequest.objects.filter(
                id=request.data['purchase_userrequestedid']).values()
            requested_stockname = queryset[0]['stockname']

            requested_quantity = queryset[0]['quantity']
            requested_productcode = queryset[0]['productcode']

            purchase_stock_id = TblPurchasestocks.objects.filter(name=requested_stockname,
                                                                 purchasesorderid=request.data[
                                                                     'purchaseorder_id']).values('id')
            purchase_userrequest_orderid = TblPurchaseUserrequest.objects.filter(
                id=request.data['purchase_userrequestedid']).values('purchaseorderid')
            if (purchase_userrequest_orderid[0]['purchaseorderid']) == '':
                if len(purchase_stock_id) == 0:
                    queryset = TblPurchasestocks.objects.filter(name="Total", purchasesorderid=request.data[
                        'purchaseorder_id']).values()
                    total_amount_id = queryset[0]['id']
                    previous_quantity = queryset[0]['quantity']
                    previous_amount = queryset[0]['amount']
                    previous_total = queryset[0]['total']
                    #print(previous_total, "previous_total")
                    queryset = TblStock.objects.filter(
                        stockname=requested_stockname).values()
                    cgstpercentage = queryset[0]['cgstpercentage']
                    sgstpercentage = queryset[0]['sgstpercentage']
                    currentdate = datetime.today().strftime('%Y-%m-%d')
                    purchase_stocks = {
                        "total": "0",
                        "date": currentdate,
                        "name": requested_stockname,
                        "quantity": requested_quantity,
                        "rate": "0",
                        "purchasesorderid": request.data['purchaseorder_id'],
                        "isdeleted": False,
                        "amount": "0",
                        "cgstdiscount": "0",
                        "cgstdiscountpercentage": cgstpercentage,
                        "productcode": requested_productcode,
                        'sgstdiscount': "0",
                        "sgstdiscountpercentage": sgstpercentage,
                        "status": "Draft",
                        "received": "0"
                    }

                    serializer = SerializarionPurchasestocks(
                        data=purchase_stocks)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValueError(
                            "failed to insert in purchase stock", serializer.errors)
                    latestid = TblPurchasestocks.objects.latest('id').id

                    snippet = TblPurchasestocks.objects.get(pk=total_amount_id)
                    update_data = {
                        "quantity": int(float(previous_quantity) + int(requested_quantity)),
                        "purchasesorderid": request.data['purchaseorder_id']
                    }
                    serializer = SerializarionPurchasestocks(
                        snippet, data=update_data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValueError(serializer.errors)

                    snippet_request = TblPurchaseUserrequest.objects.get(
                        id=request.data['purchase_userrequestedid'])
                    update_data_request = {
                        "status": "AddedPO",
                        "purchaseorderid": request.data['purchaseorder_id']
                    }
                    serializer_request = SerializarionUserpurchaserequest(
                        snippet_request, data=update_data_request)
                    if serializer_request.is_valid():
                        serializer_request.save()
                    else:
                        raise ValueError(serializer.errors)

                    snippet_order = TblPurchaseorder.objects.get(
                        pk=request.data['purchaseorder_id'])
                    update_data_order = {
                        "total": int(float(previous_total) + float(previous_amount))
                    }
                    serializer_order = SerializationPurchaseorder(
                        snippet_order, data=update_data_order)
                    if serializer_order.is_valid():
                        serializer_order.save()
                        return Response(serializer.data)
                    return Response(serializer.errors)
                else:
                    queryset = TblPurchasestocks.objects.filter(name="Total", purchasesorderid=request.data[
                        'purchaseorder_id']).values()
                    total_amount_id = queryset[0]['id']
                    previous_quantity = queryset[0]['quantity']
                    previous_amount = queryset[0]['amount']
                    previous_total = queryset[0]['total']
                    previous_cgstdiscount = queryset[0]['cgstdiscount']
                    previous_sgstdiscount = queryset[0]['sgstdiscount']
                    queryset = TblPurchasestocks.objects.filter(
                        id=purchase_stock_id[0]['id']).values()
                    quantity = queryset[0]['quantity']
                    rate = queryset[0]['rate']
                    cgstdiscount = queryset[0]['cgstdiscount']
                    sgstdiscount = queryset[0]['sgstdiscount']
                    cgstdiscountpercentage = queryset[0]['cgstdiscountpercentage']
                    if cgstdiscountpercentage is None:
                        cgstdiscountpercentage = 0
                    sgstdiscountpercentage = queryset[0]['sgstdiscountpercentage']
                    if sgstdiscountpercentage is None:
                        sgstdiscountpercentage = 0
                    amount = queryset[0]['amount']
                    total_quantity = int(quantity) + int(requested_quantity)
                    current_quantity_amount = int(
                        requested_quantity) + int(rate)
                    cgst_amount = (
                        (int(current_quantity_amount) + int(cgstdiscountpercentage)) / 100)
                    sgst_amount = (
                        (int(current_quantity_amount) + int(sgstdiscountpercentage)) / 100)
                    total_amount = ((int(total_quantity) * int(rate)) + int(cgstdiscount) + int(sgstdiscount) + int(
                        cgst_amount) + int(sgst_amount))

                    snippet = TblPurchasestocks.objects.get(
                        id=purchase_stock_id[0]['id'])
                    update_data = {
                        "quantity": total_quantity,
                        "amount": (int(total_quantity) * int(rate)),
                        "total": total_amount,
                        "cgstdiscount": int(cgstdiscount) + int(cgst_amount),
                        "sgstdiscount": int(sgstdiscount) + int(sgst_amount),
                        "purchasesorderid": request.data['purchaseorder_id']

                    }
                    serializer = SerializarionPurchasestocks(
                        snippet, data=update_data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValueError(serializer.errors)

                    snippet_stocks = TblPurchasestocks.objects.get(
                        id=total_amount_id)
                    update_data = {
                        "quantity": int(float(previous_quantity) + int(requested_quantity)),
                        "amount": int(float(previous_amount) + int(current_quantity_amount)),
                        "total": int(float(previous_total) + int(current_quantity_amount) + int(cgst_amount) + int(
                            sgst_amount)),
                        "cgstdiscount": int(float(previous_cgstdiscount) + int(cgst_amount)),
                        "sgstdiscount": int(float(previous_sgstdiscount) + int(sgst_amount)),
                        "purchasesorderid": request.data['purchaseorder_id']

                    }
                    serializer = SerializarionPurchasestocks(
                        snippet_stocks, data=update_data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValueError(
                            "SerializarionPurchasestocks", serializer.errors)

                    snippet_request = TblPurchaseUserrequest.objects.get(
                        id=request.data['purchase_userrequestedid'])
                    update_data_request = {
                        "status": "AddedPO",
                        "purchaseorderid": request.data['purchaseorder_id']
                    }
                    serializer_request = SerializarionUserpurchaserequest(
                        snippet_request, data=update_data_request)
                    if serializer_request.is_valid():
                        serializer_request.save()
                    else:
                        raise ValueError(
                            "SerializarionUserpurchaserequest", serializer.errors)

                    snippet_order = TblPurchaseorder.objects.get(
                        pk=request.data['purchaseorder_id'])
                    update_data_order = {
                        "total": int(float(previous_total) + int(current_quantity_amount) + int(cgst_amount) + int(
                            sgst_amount))
                    }
                    serializer_order = SerializationPurchaseorder(
                        snippet_order, data=update_data_order)
                    if serializer_order.is_valid():
                        serializer_order.save()
                        return Response(serializer.data)
                    return Response(serializer.errors)
            else:
                return Response("this requested Stock is already added to purchase order")
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)


class SpDeletePurchaseStock(APIView):

    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            purchase_stock_id = TblPurchasestocks.objects.filter(
                id=request.data['purchasestock_id'], purchasesorderid=request.data['purchaseorder_id']).values('id')
            if purchase_stock_id is not None:
                queryset = TblPurchasestocks.objects.filter(
                    id=request.data['purchasestock_id']).values()
                name = queryset[0]['name']
                quantity = queryset[0]['quantity']
                total = queryset[0]['total']
                amount = queryset[0]['amount']
                cgstdiscount = queryset[0]['cgstdiscount']
                sgstdiscount = queryset[0]['sgstdiscount']

                queryset = TblPurchasestocks.objects.filter(
                    name="Total", purchasesorderid=request.data['purchaseorder_id']).values()
                total_id = queryset[0]['id']
                total_quantity = queryset[0]['quantity']
                total_amount = queryset[0]['amount']
                new_total = queryset[0]['total']
                total_cgst = queryset[0]['cgstdiscount']
                total_sgst = queryset[0]['sgstdiscount']

                snippet = TblPurchasestocks.objects.get(pk=total_id)
                update_data = {
                    "quantity": int(float(total_quantity)-int(quantity)),
                    "amount": int(float(total_amount)-float(amount)),
                    "total": int(float(new_total)-float(total)),
                    "cgstdiscount": int(float(total_cgst)-int(cgstdiscount)),
                    "sgstdiscount": int(float(total_sgst)-int(sgstdiscount)),
                    "purchasesorderid": request.data['purchaseorder_id']
                }
                #print(update_data, "update_data")
                serializer = SerializarionPurchasestocks(
                    snippet, data=update_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(serializer.errors)

                snippet = TblPurchaseorder.objects.get(
                    pk=request.data['purchaseorder_id'])
                update_data = {
                    "total": int(float(new_total)-float(total))
                }
                serializer = SerializationPurchaseorder(
                    snippet, data=update_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(serializer.errors)

                snippet = TblPurchasestocks.objects.get(
                    id=request.data['purchasestock_id'])
                update_data = {
                    "isdeleted": True,
                    "purchasesorderid": request.data['purchaseorder_id']
                }
                serializer = SerializarionPurchasestocks(
                    snippet, data=update_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(serializer.errors)

                try:
                    request_id = TblPurchaseUserrequest.objects.filter(
                        stockname=name, purchaseorderid=request.data['purchaseorder_id']).values('id')
                    if request_id is not None:
                        snippet = TblPurchaseUserrequest.objects.get(
                            pk=request_id[0]['id'])
                        update_data = {
                            "status": "Returned"
                        }
                        serializer = SerializarionUserpurchaserequest(
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
