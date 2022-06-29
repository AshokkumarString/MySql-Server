from TeamTask.models import TblInvoicesummary, TblPurchasebillinvoice, TblPurchaseorder, TblSales
from TeamTask.serialization import SerializationPurchaseInvocie, SerializationPurchaseorder, SerializationSales, \
    SerializationTransaction, SerializationVoucherDetails, seralizationTblInvoicesummary
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime


class SpVoucherManagement(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if request.data['vouchertype'] == 'Payment':
                for data in request.data['requesteddata']:
                    if ((request.data['detailtype'] == 'PurchaseAdvance') or request.data[
                        'detailtype'] == 'PurchaseBills'):
                        if (request.data['detailtype'] == 'PurchaseAdvance'):
                            voucher_concat = request.data['detailtype'] + '_Orders'
                            voucher_refer_concat = data['vouchertype']
                            # print(voucher_concat)
                        else:
                            voucher_concat = request.data['detailtype'] + '_Bills'
                            voucher_refer_concat = data['vouchertype']
                            # print(voucher_refer_concat)
                    else:
                        voucher_concat = request.data['detailtype']
                        voucher_refer_concat = data['vouchertype'] + '_' + data['voucherreferencetype']
                        # print(voucher_refer_concat)
                    voucher_data = {
                        "amount": data['amount'],
                        "voucherreferencetype": data['voucherreferencetype'],
                        "vouchertype": data['vouchertype'],
                        "vouchermanagement": request.data['vouchermanagement_id']
                    }
                    # print(voucher_data)
                    serilaizer_voucher_details = SerializationVoucherDetails(data=voucher_data)
                    if serilaizer_voucher_details.is_valid():
                        # serilaizer_voucher_details.validated_data
                        serilaizer_voucher_details.save()
                    else:
                        raise ValueError(serilaizer_voucher_details.errors, "serilaizer_voucher_details failed")

                    currentdate = datetime.today().strftime('%Y-%m-%d')
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    transaction_data = {
                        "transactiontaskid": "",
                        "transaction_clientid": request.data['client_id'],
                        "userid_id": request.data['user_id'],
                        "amount": data['amount'],
                        "deliverynoteid": "",
                        "description": "",
                        "time": current_time,
                        "transactiontype": "PaymentVoucher",
                        "date": currentdate,
                        "companyid": request.data['company_id'],
                        "originalcompanyid": 0,
                        "originaldeliverynoteid": 0,
                        "pmtmode": request.data['paymentmode'],
                        "pmtreference": "",
                        "voucherid": request.data['vouchermanagement_id'],
                        "vouchertype": voucher_concat,
                        "voucherreferencetype": voucher_refer_concat
                    }
                    print(transaction_data)
                    serilaizer_transaction = SerializationTransaction(data=transaction_data)
                    if serilaizer_transaction.is_valid():
                        serilaizer_transaction.save()
                    else:
                        raise ValueError(serilaizer_transaction.errors, "serilaizer_transaction failed")

                    if ((request.data['detailtype'] == 'PurchaseAdvance') or request.data[
                        'detailtype'] == 'PurchaseBills'):
                        if (request.data['detailtype'] == 'PurchaseAdvance'):
                            amount_paid = TblPurchaseorder.objects.filter(id=data['vouchertype']).values('advancepaid')
                            print(amount_paid, "amount_paid")
                            if amount_paid is None:
                                amount_paid = 0
                            total = int(amount_paid[0]['advancepaid']) + int(data['amount'])
                            print(total, "total")
                            snippet = TblPurchaseorder.objects.get(pk=data['vouchertype'])
                            update_data = {
                                "advancepaid": total
                            }
                            serilaizer_purchase = SerializationPurchaseorder(snippet, data=update_data)
                            if serilaizer_purchase.is_valid():
                                serilaizer_purchase.save()
                                # serilaizer_purchase.validated_data
                            else:
                                raise ValueError(serilaizer_purchase.errors, "serilaizer_purchase failed")

                        else:
                            amount_received = TblPurchasebillinvoice.objects.filter(id=data['vouchertype']).values(
                                'amountreceived')
                            # print(amount_received,"amount_received")
                            bill_amount = TblPurchasebillinvoice.objects.filter(id=data['vouchertype']).values('amount')
                            if amount_received is None:
                                amount_received = 0
                            total = int(amount_received[0]['amountreceived']) + int(data['amount'])
                            # print({total,bill_amount})

                            if (int(bill_amount[0]['amount']) == total):
                                snippet = TblPurchasebillinvoice.objects.get(pk=data['vouchertype'])
                                update_data = {
                                    "amountreceived": total,
                                    "status": "Paid"
                                }
                                serilaizer_purchasebill = SerializationPurchaseInvocie(snippet, data=update_data)
                                if serilaizer_purchasebill.is_valid():
                                    serilaizer_purchasebill.save()
                                    # serilaizer_purchasebill.validated_data
                                else:
                                    raise ValueError(serilaizer_purchasebill.errors, "serilaizer_purchasebill failed")
                            else:
                                snippet = TblPurchasebillinvoice.objects.get(pk=data['vouchertype'])
                                update_data = {
                                    "amountreceived": total,
                                    "status": "Partially Paid"
                                }
                                serilaizer_purchasebill = SerializationPurchaseInvocie(snippet, data=update_data)
                                if serilaizer_purchasebill.is_valid():
                                    serilaizer_purchasebill.save()
                                    # serilaizer_purchasebill.validated_data
                                else:
                                    raise ValueError(serilaizer_purchasebill.errors,
                                                     "serilaizer_purchasebill Partially Paid failed")
                return Response("Voucher Has Been Created Successfully for Purchase", status=status.HTTP_201_CREATED)
            else:
                for data in request.data['requesteddata']:
                    # print(data,"data")
                    if ((request.data['detailtype'] == 'SalesInvoice') or request.data['detailtype'] == 'SalesAdvance'):
                        if (request.data['detailtype'] == 'SalesAdvance'):
                            voucher_concat = request.data['detailtype'] + '_Orders'
                            voucher_refer_concat = data['vouchertype']
                        else:
                            voucher_concat = request.data['detailtype'] + '_Invoices'
                            voucher_refer_concat = data['vouchertype']
                    else:
                        voucher_concat = request.data['detailtype']
                        voucher_refer_concat = data['vouchertype'] + '_' + data['voucherreferencetype']
                    voucher_data = {
                        "amount": data['amount'],
                        "voucherreferencetype": data['voucherreferencetype'],
                        "vouchertype": data['vouchertype'],
                        "vouchermanagement": request.data['vouchermanagement_id']
                    }
                    # print(voucher_data)
                    serilaizer_voucher_details = SerializationVoucherDetails(data=voucher_data)
                    if serilaizer_voucher_details.is_valid():
                        # serilaizer_voucher_details.validated_data
                        serilaizer_voucher_details.save()
                    else:
                        raise ValueError(serilaizer_voucher_details.errors, "serilaizer_voucher_details failed")

                    currentdate = datetime.today().strftime('%Y-%m-%d')
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    if request.data['detailtype'] == 'SalesInvoice':

                        transaction_data = {
                            "transactiontaskid": "",
                            "transaction_clientid": request.data['client_id'],
                            "userid_id": request.data['user_id'],
                            "amount": data['amount'],
                            "deliverynoteid": voucher_refer_concat,
                            "description": "",
                            "time": current_time,
                            "transactiontype": "Received",
                            "date": currentdate,
                            "companyid": request.data['company_id'],
                            "originalcompanyid": 0,
                            "originaldeliverynoteid": 0,
                            "pmtmode": request.data['paymentmode'],
                            "pmtreference": "",
                            "voucherid": request.data['vouchermanagement_id'],
                            "vouchertype": voucher_concat,
                            "voucherreferencetype": voucher_refer_concat
                        }
                        serilaizer_transaction = SerializationTransaction(data=transaction_data)
                        if serilaizer_transaction.is_valid():
                            # serilaizer_transaction.validated_data
                            serilaizer_transaction.save()
                        else:
                            raise ValueError(serilaizer_transaction.errors,
                                             "serilaizer_transaction for 'sales' received is failed")

                        transaction_data = {
                            "transactiontaskid": "",
                            "transaction_clientid": request.data['client_id'],
                            "userid_id": request.data['user_id'],
                            "amount": data['amount'],
                            "deliverynoteid": voucher_refer_concat,
                            "description": "",
                            "time": current_time,
                            "transactiontype": "Spend",
                            "date": currentdate,
                            "companyid": request.data['company_id'],
                            "originalcompanyid": 0,
                            "originaldeliverynoteid": 0,
                            "pmtmode": request.data['paymentmode'],
                            "pmtreference": "",
                            "voucherid": request.data['vouchermanagement_id'],
                            "vouchertype": voucher_concat,
                            "voucherreferencetype": voucher_refer_concat
                        }
                        serilaizer_transaction = SerializationTransaction(data=transaction_data)
                        if serilaizer_transaction.is_valid():
                            # serilaizer_transaction.validated_data
                            serilaizer_transaction.save()
                        else:
                            raise ValueError(serilaizer_transaction.errors,
                                             "serilaizer_transaction for 'sales' spend is failed")
                    else:
                        transaction_data = {
                            "transactiontaskid": "",
                            "transaction_clientid": request.data['client_id'],
                            "userid_id": request.data['user_id'],
                            "amount": data['amount'],
                            "deliverynoteid": "",
                            "description": "",
                            "time": current_time,
                            "transactiontype": "ReceiptVoucher",
                            "date": currentdate,
                            "companyid": request.data['company_id'],
                            "originalcompanyid": 0,
                            "originaldeliverynoteid": 0,
                            "pmtmode": request.data['paymentmode'],
                            "pmtreference": "",
                            "voucherid": request.data['vouchermanagement_id'],
                            "vouchertype": voucher_concat,
                            "voucherreferencetype": voucher_refer_concat
                        }
                        serilaizer_transaction = SerializationTransaction(data=transaction_data)
                        if serilaizer_transaction.is_valid():
                            # serilaizer_transaction.validated_data
                            serilaizer_transaction.save()
                        else:
                            raise ValueError(serilaizer_transaction.errors,
                                             "serilaizer_transaction for 'sales' receipt voucher is failed")

                    if (request.data['detailtype'] == 'SalesInvoice') or request.data['detailtype'] == 'SalesAdvance':
                        if request.data['detailtype'] == 'SalesAdvance':
                            amount_received = TblSales.objects.filter(id=data['vouchertype']).values('advancereceived')
                            if amount_received is None:
                                amount_received = 0
                            total = int(amount_received[0]['advancereceived']) + int(data['amount'])
                            snippet = TblSales.objects.get(pk=data['vouchertype'])
                            update_data = {
                                "advancereceived": total
                            }
                            serilaizer_sales = SerializationSales(snippet, data=update_data)
                            if serilaizer_sales.is_valid():
                                serilaizer_sales.save()
                                # serilaizer_sales.validated_data
                            else:
                                raise ValueError(serilaizer_sales.errors, "serilaizer_sales failed")
                        else:
                            queryset = TblInvoicesummary.objects.filter(Q(deliverynoteid=voucher_refer_concat),
                                                                        Q(invoice_company=request.data[
                                                                            'invoice_company']),
                                                                        (~Q(salesorder=None))).values()
                            amount_received = queryset[0]['amount_received']
                            print(amount_received, "amount_received")
                            duebalance = queryset[0]['balancedue']
                            bill_amount = queryset[0]['invoice_amount']
                            if amount_received is None:
                                amount_received = 0
                            total = int(amount_received) + int(data['amount'])
                            new_due_balance = int(bill_amount) - total

                            if (int(bill_amount) == total):
                                snippet = TblInvoicesummary.objects.get(Q(deliverynoteid=voucher_refer_concat),
                                                                        Q(invoice_company=request.data[
                                                                            'invoice_company']), (~Q(salesorder=None)))
                                print(snippet, "snippet")
                                update_data = {
                                    "invoicestatus": "Paid",
                                    "amount_received": total,
                                    "balancedue": new_due_balance
                                }
                                serilaizer_invoicesummary = seralizationTblInvoicesummary(snippet, data=update_data)
                                if serilaizer_invoicesummary.is_valid():
                                    serilaizer_invoicesummary.save()
                                    # serilaizer_invoicesummary.validated_data
                                else:
                                    raise ValueError(serilaizer_invoicesummary.errors,
                                                     "serilaizer_invoicesummary paid failed")
                            else:
                                snippet = TblInvoicesummary.objects.get(Q(deliverynoteid=voucher_refer_concat),
                                                                        Q(invoice_company=request.data[
                                                                            'invoice_company']), (~Q(salesorder=None)))
                                update_data = {
                                    "invoicestatus": "Partially Paid",
                                    "amount_received": total,
                                    "balancedue": new_due_balance
                                }
                                serilaizer_invoicesummary = seralizationTblInvoicesummary(snippet, data=update_data)
                                if serilaizer_invoicesummary.is_valid():
                                    serilaizer_invoicesummary.save()
                                    # serilaizer_invoicesummary.validated_data
                                else:
                                    raise ValueError(serilaizer_invoicesummary.errors,
                                                     "serilaizer_invoicesummary Partially Paid failed")
                return Response("Voucher Has Been Created Successfully for Sales", status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)
