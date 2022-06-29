from datetime import date
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum,Max,Q
from TeamTask.models import TblInventorytransaction, TblTaskinvoice
from TeamTask.serialization import SerializationInventorytransaction, seralizationTblTaskinvoicedetails


# (storeproc Reactla update pannala)
# class SpAvailableStocknamesAndQuantity(APIView):
#     authentication_classes = [SessionAuthentication,
#                               BasicAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self,request):
#         queryset=TblInventorytransaction.objects.values('stockname').annotate(quantity=Sum('quantity')).filter(quantity__gt=0)
#         return Response(queryset, status=status.HTTP_201_CREATED)

class SpGetAvailableStockQuantity(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        queryset=TblInventorytransaction.objects.values('stockname').annotate(quantity=Sum('quantity')).filter(quantity__gt=0,stockname=request.data['stockname'])
        return Response(queryset, status=status.HTTP_201_CREATED)

class SpAvailableStockbatch(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        tmp_availablebatch=TblInventorytransaction.objects.values('stockname','batch').annotate(quantity=Sum('quantity')).filter(stockname=request.data['stock'],quantity__gt=0)
        output=[]
        for data in tmp_availablebatch:
            variable=TblInventorytransaction.objects.filter(batch=data['batch'],stockname=data['stockname']).values('stockname','quantity','batch','rate')
            queryset=variable.filter(~Q(status="Sales")).values('rate').distinct()
            for rate in queryset:
                distinct_rate={
                    "stockanme":data['stockname'],
                    "quantity":data['quantity'],
                    "batch":data['batch'],
                    "rate":rate['rate']
                }
                output.append(distinct_rate)
        return Response(output)

class SpStoreOutwardStock(APIView):
    def post(self,request):
        try:
            outward_data=[]
            for outward in request.data['outward_details']:
                queryset=TblInventorytransaction.objects.filter(stockname=outward['stockname']).aggregate(Max('batch'))
                max_batch_id=queryset['batch__max']
                if (str(max_batch_id==0) or max_batch_id is None):
                    max_batch_id=9999
                new_max_id=max_batch_id+1
                inventory_transaction={
                    "date":date.today(),
                    "username":request.data['username'],
                    "stockname":outward['stockname'],
                    "productcode":outward['productcode'],
                    "quantity":outward['quantity'],
                    "rate":outward['quantity'],
                    "amount":outward['rate'],
                    "cgstpercentage":"0",
                    "sgstpercentage":"0",
                    "total":outward['total'],
                    "batch":new_max_id,
                    "location":"0",
                    "status":"Converted",
                    "invoiceno":"0",
                    "purchaseorderid":"0",
                    "length":"0",
                    "purchaseinvoice":""
                }
                serializer=SerializationInventorytransaction(data=inventory_transaction)
                if serializer.is_valid():
                    serializer.save()
                    outward_data.append(outward)
                else:
                    raise ValueError(serializer.errors)
            return Response({"Outwards Data":outward_data},status=status.HTTP_201_CREATED)   
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)   

class SpStoreDraftingCharges(APIView):
    def post(self,request):
        try:
            for drafting in request.data['drafting_data']:
                drafting_id=TblTaskinvoice.objects.filter(tasklistrowid=drafting['taskid'],user=drafting['name']).values('id')
                if len(drafting_id) ==0:
                    if (drafting['time'] != '00:00' and drafting['amount'] != '0'):
                        task_invoice={
                            "user":drafting['name'],
                            "unit":drafting['time'],
                            "rate":drafting['rate'],
                            "amount":drafting['amount'],
                            "tasklistrowid":drafting['taskid']
                        }
                        serializer=seralizationTblTaskinvoicedetails(data=task_invoice)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            raise ValueError(serializer.errors)
                else:
                    try:
                        snippet=TblTaskinvoice.objects.get(id=drafting_id[0]['id'])
                        update_data={
                            "unit":drafting['time'],
                            "rate":drafting['rate'],
                            "amount":drafting['amount'],
                            "tasklistrowid":drafting['taskid']
                        }
                        serializer=seralizationTblTaskinvoicedetails(snippet,data=update_data)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            raise ValueError(serializer.errors)
                    except:
                            pass
            return Response("Drafting Charges has been calculated",status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(str(ex),status=status.HTTP_400_BAD_REQUEST)
