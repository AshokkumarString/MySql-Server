from email import message
from http import client
from django.db import models
from django.db.models.lookups import Exact
import django_filters
from TeamTask.models import TblUnitType
from TeamTask.serialization import SerializationUnitType
from TeamTask.serialization import SerializationTaskList, SerializarionTaxyear, SerializationCompany
from TeamTask.serialization import SerializationNewSubtask, seralizationTblTaskinvoicedetails, SerializationTransaction, SerializeJoinWorktime
from TeamTask.serialization import SerializationClient, SerializationSubtasks, seralizationTblStock, seralizationTblStockinvoice
from TeamTask.serialization import SerializationUsers, SerializationUserdetails, serializationPlandetails, seralizationTblInvoicesummary, SerializationSubClient
from TeamTask.serialization import serialization_companyname, serialization_bankname, SerializationBillstocks
from TeamTask.serialization import SerializationPurchaseorder, SerializarionPurchasestocks, SerializarionUserpurchaserequest
from TeamTask.serialization import SerializationStockgroup, SerializationClientgroup, SerializationInventorytransaction
from TeamTask.serialization import SerializationPurchaseInvocie, Serializationbatch, Serializationlocation, SerializationPurchaseInvocie
from TeamTask.serialization import Serializationsalestransaction, SerializationSales, SerializationExpenses, SerializationSalesRequest
from TeamTask.serialization import SerializationVoucherManagement, SerializationVoucherDetails, SerializationLedgertype, SerializationLedgergroup
from TeamTask.serialization import Serializationquotationtransaction, Serializationquotationrequest,SerializationProjects
# from TeamTask.serialization import
from django.shortcuts import render
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django_filters.utils import translate_validation
from django.http import Http404
from TeamTask.models import TblTasklist, TblTransaction, TblWorkTimeTable
from TeamTask.models import TblSubtasktime, TblStockinvoice
from TeamTask.models import Userdetail, TblSubtask, TblTaxyear
from TeamTask.models import Users, TblTaskinvoice, TblStock, TblInvoicesummary
from TeamTask.models import Plantype, TblPurchasebillinvoice, TblQuotationtransaction, TblQuotationrequest
from TeamTask.models import TblClient, TblSubclient, TblCompany, TblBank, TblInventorytransaction
from TeamTask.models import TblPurchasestocks, TblPurchaseorder, TblPurchaseUserrequest, TblClientGroup, TblStockGroup
from TeamTask.models import TblBatch, TblLocation, TblSalestransaction, TblSales, TblExpenses, TblSalesrequest
from TeamTask.models import TblVouchermanagement, TblVoucherdetails, TblPurchasebillstocks, TblLedgertypes, TblLedgergroups,TblProjects
from django.db import connection
from rest_framework import serializers, viewsets
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from TeamTask.serialization import UserSerializer, UserSerializerWithToken
from django.db.models import Lookup
from django.db.models import Field
from rest_framework.pagination import PageNumberPagination
from django.views.generic import View
# from .filters import InvoiceFilter

# Pagination Start


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 5000


class Tasklistpaginationviewset(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = SerializationTaskList
    queryset = TblTasklist.objects.all()
    pagination_class = StandardResultsSetPagination


class TodoListpaginationView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = TblTasklist.objects.all()
    serializer_class = SerializationTaskList
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'startdate': ['gte', 'lte', 'exact'], 'enddate': ['gte', 'lte', 'exact'], 'id': ['exact'], 'date': ['exact'], 'task': ['exact'], 'assignto': ['exact'],
                        'status': ['in', 'exact'], 'priority': ['exact'], 'time': ['exact'], 'isdeleted': ['exact'], 'plantype': ['exact'], 'client': ['exact'],
                        'advanceamount': ['exact'], 'company': ['exact'],'projectname':['exact'],'totalamount':['exact'],'invoiceidno':['exact']}
    pagination_class = StandardResultsSetPagination


class Tasklistviewset(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = SerializationTaskList
    queryset = TblTasklist.objects.all()


@api_view()
@permission_classes([IsAuthenticated])
def tasklistFunction(request):
    print(request.query_params)
    d1 = request.query_params['startdate']
    d2 = request.query_params['enddate']
    d3 = request.query_params['status']
    d4 = request.query_params['assignto']

    try:
        tasklist = TblTasklist.objects.filter(
            startdate__gte=d1, enddate__lte=d2, status=d3, assignto=d4)
    except TblTasklist.DoesNotExist:
        return Response([])

    if request.method == 'GET':
        serializer = SerializationTaskList(tasklist, many=True)
        return Response(serializer.data)


class Subtaskviewset(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = SerializationNewSubtask
    queryset = TblSubtasktime.objects.all()


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = SerializationUsers
    queryset = Users.objects.all()


class UserdetailViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = SerializationUserdetails
    queryset = Userdetail.objects.all()


class UserdetailfilterView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Userdetail.objects.all()
    serializer_class = SerializationUserdetails
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'username': ['exact'], 'email': ['exact'], 'fristname': ['exact'], 'lastname': ['exact'], 'address': ['exact'],
                        'city': ['exact'], 'country': ['exact'], 'postalcode': ['exact'], 'aboutme': ['exact']}


class Companyviewset(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationCompany
    queryset = TblCompany.objects.all()


class Bankviewset(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = serialization_bankname
    queryset = TblBank.objects.all()


class Bankfilterview(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = TblBank.objects.all()
    serializer_class = serialization_bankname
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'bankname': ['exact'],
                        'accountno': ['exact'], 'upi': ['exact'], 'comments': ['exact'], 'ifsc': ['exact'], 'companydetails': ['exact']}

class CompanyView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = TblCompany.objects.all()
    serializer_class = serialization_companyname
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'companyname': [
        'exact'], 'isactive': ['exact'], 'isvisible': ['exact'], 'isgst': ['exact']}


class TodoListView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = TblTasklist.objects.all()
    serializer_class = SerializationTaskList
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'startdate': ['gte', 'lte', 'exact'], 'enddate': ['gte', 'lte', 'exact'], 'id': ['exact'], 'date': ['exact'], 'task': ['exact'], 'assignto': ['exact'],
                        'status': ['in', 'exact'], 'priority': ['exact'], 'time': ['exact'], 'isdeleted': ['exact'], 'plantype': ['exact'], 'client': ['exact'],'subclient':['exact'],
                        'advanceamount': ['exact']}


class FiltersubtaskTime(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = SerializationNewSubtask
    queryset = TblSubtasktime.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'username': [
        'exact'], 'comments': ['exact'], 'time': ['exact'], 'subtask': ['exact']}


class ClientView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationClient
    queryset = TblClient.objects.all()


class UsersFilter(generics.ListAPIView):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = SerializationUsers
    queryset = Users.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'name': ['exact'], 'mailid': ['exact'], 'isadmin': [
        'exact'], 'isapproved': ['exact'], 'default_rate': ['exact'], 'superuser': ['exact'], 'userprofile': ['exact'],'task':['exact'],'admin':['exact'],'report':['exact'],
        'invoice': ['exact'],'inventory': ['exact'],'sales': ['exact'],'voucher': ['exact'],'purchase': ['exact'],'reload':['exact'],'initial':['exact'],'colour':['exact']}


class PlandetailsViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = serializationPlandetails
    queryset = Plantype.objects.all()


class ClientFilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = SerializationClient
    queryset = TblClient.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'company_name': ['exact'], 'engineer_name': [
        'exact'], 'emailid': ['exact'], 'phoneno': ['exact'], 'clientid': ['exact'], 'isdeleted': ['exact'], 'pannumber': ['exact'], 'gstnumber': ['exact']}


class Subclients(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationSubClient
    queryset = TblSubclient.objects.all()


class SubclientsFilterView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationSubClient
    queryset = TblSubclient.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'],
                        'name': ['exact'], 'clients': ['exact']}


class Subtasks(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationSubtasks
    queryset = TblSubtask.objects.all()


class SubtasksFilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationSubtasks
    queryset = TblSubtask.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'subtask': ['exact'], 'assignto': ['exact'], 'priority': ['exact'], 'status': ['in', 'exact'], 'time': ['exact'], 'isdeleted': ['exact'],
                        'completed_date': ['exact'], 'tasklist': ['exact']}


class stockView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = seralizationTblStock
    queryset = TblStock.objects.all()


class stockFilterView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = seralizationTblStock
    queryset = TblStock.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'stockname': [
        'exact'], 'productcode': ['exact'], 'defaultrate': ['exact'], 'cgstpercentage': ['exact'], 'sgstpercentage': ['exact'], 'length': ['exact'], 'liquid': ['exact'], 'hsncode': ['exact']}


class InvoicedetailView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = seralizationTblTaskinvoicedetails
    queryset = TblTaskinvoice.objects.all()


class InvoicedetailFilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = seralizationTblTaskinvoicedetails
    queryset = TblTaskinvoice.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'user': ['exact'], 'unit': [
        'exact'], 'rate': ['exact'], 'amount': ['exact'], 'tasklistrowid': ['exact']}


class stockInvoicedetailView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = seralizationTblStockinvoice
    queryset = TblStockinvoice.objects.all()


class stockInvoicedetailFilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = seralizationTblStockinvoice
    queryset = TblStockinvoice.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'types': ['exact'], 'unit': [
        'exact'], 'rate': ['exact'], 'amount': ['exact'], 'tasklistrow': ['exact']}


class InvoiceSummaryView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = seralizationTblInvoicesummary
    queryset = TblInvoicesummary.objects.all()


class VoucherManagementView(viewsets.ModelViewSet):

    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationVoucherManagement
    queryset = TblVouchermanagement.objects.all()


class VoucherManagementfilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationVoucherManagement
    queryset = TblVouchermanagement.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'username': ['exact'], 'clientname': ['exact'], 'companyname': ['exact'],
                        'paymentmode': ['exact'], 'client': ['exact'], 'vouchersubtype': ['exact'], 'vouchersubreferencetype': ['exact'], 'vouchertype': ['exact']}


class VoucherDetailstView(viewsets.ModelViewSet):

    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationVoucherDetails
    queryset = TblVoucherdetails.objects.all()


class VoucherDetailsfilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationVoucherDetails
    queryset = TblVoucherdetails.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'name': ['exact'], 'amount': ['exact'], 'status': ['exact'],
                        'vouchermanagement': ['exact'], 'salesid': ['exact'], 'purchase': ['exact']}

class ProjectsView(viewsets.ModelViewSet):
    
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationProjects
    queryset = TblProjects.objects.all()


class Projectsfilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationProjects
    queryset = TblProjects.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'clientid': ['exact'], 'clientname': ['exact'],
                        'subclient': ['exact'], 'phonenumber': ['exact'], 'status': ['in', 'exact'],  'company': ['exact'],'projectname':['exact'],'totalamount':['exact'],'invoiceid':['exact']}


@api_view(['GET', ])
def invoice_detail_set1(request):
    filters = {'id'}

    if request.method == 'GET':
        # invoice = TblInvoicesummary.objects.all()
        invoice = TblInvoicesummary.objects.filter(**filters)
        print(invoice)
        serializer = seralizationTblInvoicesummary(invoice, many=True)
        return JsonResponse(serializer.data, safe=False)


class InvoiceSummaryFilterViewpagination(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = seralizationTblInvoicesummary
    queryset = TblInvoicesummary.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'invoicesummaryclient': ['in', 'exact'], 'invoice_amount': ['exact'],
                        'amount_received': ['exact'], 'invoicestatus': ['in', 'exact'], 'duedate': ['exact'], 'discount': ['exact'],
                        'deliverynoteid': ['exact'], 'originaldeliverynoteid': ['exact'], 'originalcompanyid': ['exact'], 'balancedue': ['exact'], 'comments': ['exact'], 'companyinvoiceid': ['exact'], 'clientgroupid': ['exact'],'invoice_company': ['exact']}
    pagination_class = StandardResultsSetPagination


class InvoiceSummaryFilterView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = seralizationTblInvoicesummary
    queryset = TblInvoicesummary.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'invoicesummaryclient': ['exact'], 'invoice_amount': ['exact'],
                        'amount_received': ['exact'], 'invoicestatus': ['in', 'exact'], 'duedate': ['exact'], 'discount': ['exact'], 'deliverynoteid': ['exact'], 'originaldeliverynoteid': ['exact'], 'originalcompanyid': ['exact'], 'subtotal': ['exact'], 'balancedue': ['exact'], 'comments': ['exact'], 'salesorder': ['exact'], 'vehiclenumber': ['exact'], 'invoicetype': ['exact'], 'clientgroupid': ['exact'],'project_id':['exact'],'tbltasklist':['exact'],'invoice_company': ['exact']}

class Transactionviewset(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationTransaction
    queryset = TblTransaction.objects.all()


class TransactionFilterView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]  

    serializer_class = SerializationTransaction
    queryset = TblTransaction.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact', 'gt'], 'transactiontask': ['exact'], 'date': ['gte', 'lte', 'exact'], 'time': ['exact'], 'transaction_client': ['exact'], 'userid': ['exact'],
                        'amount': ['exact'], 'pmtmode': ['exact'], 'pmtreference': ['exact'], 'description': ['exact'], 'transactiontype': ['exact'],
                        'vouchertype': ['exact'], 'voucherreferencetype': ['exact'], 'voucher': ['exact'], 'salesorderid': ['exact'], 'client_groupid': ['exact'],'company_id': ['exact']}


class Subclients(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationSubClient
    queryset = TblSubclient.objects.all()


class SubclientsFilterView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationSubClient
    queryset = TblSubclient.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'subclientname': [
        'exact'], 'clientrefId': ['exact']}


class Taxyear(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializarionTaxyear
    queryset = TblTaxyear.objects.all()

    # Purchase and Inventory Start


class PurchaseStocks(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializarionPurchasestocks
    queryset = TblPurchasestocks.objects.all()


class PurchaseStocksFilterView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializarionPurchasestocks
    queryset = TblPurchasestocks.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'name': ['exact'], 'productcode': ['exact'], 'quantity': ['exact'], 'rate': ['exact'],
                        'amount': ['exact'], 'cgstdiscount': ['exact'], 'sgstdiscount': ['exact'], 'cgstdiscountpercentage': ['exact'],
                        'sgstdiscountpercentage': ['exact'], 'total': ['exact'], 'isdeleted': ['exact'], 'purchasesorderid': ['exact'],
                        'status': ['in', 'exact'], 'received': ['exact'], 'remaining': ['exact'], 'invoiceno': ['exact'], 'hsncode': ['exact']}


class PurchaseOrder(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationPurchaseorder
    queryset = TblPurchaseorder.objects.all()


class PurchaseOrderFilterView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationPurchaseorder
    queryset = TblPurchaseorder.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'companyid': ['exact'], 'date': ['gte', 'lte', 'exact'], 'total': [
        'exact'], 'supplier': ['exact'], 'payment': ['exact'], 'status': ['in', 'exact'], 'isdeleted': ['exact'], 'advancepaid': ['exact'], 'advanceused': ['exact'], 'deliverydate': ['gte', 'lte', 'exact']}


class UserpurchaseStocks(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializarionUserpurchaserequest
    queryset = TblPurchaseUserrequest.objects.all()


class userpurchaserequestFilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializarionUserpurchaserequest
    queryset = TblPurchaseUserrequest.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'time': ['exact'], 'username': ['exact'], 'stockname': ['exact'], 'productcode': ['exact'],
                        'quantity': ['exact'], 'status': ['in', 'exact'], 'description': ['exact'], 'purchaseorderid': ['exact'], 'isdeleted': ['exact']}


class inventorytransaction(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationInventorytransaction
    queryset = TblInventorytransaction.objects.all()


class inventorytransactionFilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationInventorytransaction
    queryset = TblInventorytransaction.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'username': ['exact'], 'stockname': ['exact'], 'productcode': ['exact'],
                        'quantity': ['exact'], 'status': ['in', 'exact'], 'purchaseorderid': ['exact'], 'invoiceno': ['exact'], 'length': ['exact'], 'purchaseinvoice': ['exact'], 'salesid': ['exact'], 'companyid': ['exact'], 'hsncode': ['exact']}

# Purchase and Inventory End


class purchaseInvoice(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationPurchaseInvocie
    queryset = TblPurchasebillinvoice.objects.all()


class PurchaseInvocieFilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationPurchaseInvocie
    queryset = TblPurchasebillinvoice.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'purchaseinvoiceno': ['exact'], 'supplier': ['exact'], 'company': ['exact'], 'amount': ['exact'],
                        'status': ['in', 'exact'], 'amountreceived': ['exact'], 'invoicedate': ['gte', 'lte', 'exact']}


# BillStocks


class PurchaseInvoiceStock(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationBillstocks
    queryset = TblPurchasebillstocks.objects.all()


class PurchaseInvoiceStockFilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationBillstocks
    queryset = TblPurchasebillstocks.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'username': ['exact'], 'stockname': ['exact'], 'productcode': ['exact'], 'quantity': ['exact'], 'status': ['in', 'exact'],
                        'purchaseorderid': ['exact'], 'length': ['exact'], 'rate': ['exact'], 'amount': ['exact'], 'cgstpercentage': ['exact'], 'invoiceno': ['exact'],
                        'sgstpercentage': ['exact'], 'total': ['exact'], 'isdeleted': ['exact'], 'batch': ['exact'], 'location': ['exact'], 'bill': ['exact']}


# end of Bill stock


class SalesRequestViews(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationSalesRequest
    queryset = TblSalesrequest.objects.all()


class SalesRequestFilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationSalesRequest
    queryset = TblSalesrequest.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'time': ['exact'], 'username': ['exact'], 'stockname': ['exact'], 'productcode': ['exact'],
                        'quantity': ['exact'], 'status': ['in', 'exact'], 'Salesid': ['exact'], 'isdeleted': ['exact'], 'clientid': ['exact'], 'companyid': ['exact']}


class StockgroupView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationStockgroup
    queryset = TblStockGroup.objects.all()


class StockgroupFilterView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationStockgroup
    queryset = TblStockGroup.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'name': ['exact'], }


class ClientgroupView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationClientgroup
    queryset = TblClientGroup.objects.all()


class ClientgroupFilterView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationClientgroup
    queryset = TblClientGroup.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'name': ['exact'], }


#batch and location

class BatchListApiView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = Serializationbatch
    queryset = TblBatch.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'batchno': [
        'exact'], 'description': ['exact'], }


class BatchModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = Serializationbatch
    queryset = TblBatch.objects.all()


class LocationListApiView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = Serializationlocation
    queryset = TblLocation.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'location': [
        'exact'], 'shortlocation': ['exact'], 'description': ['exact'], 'godown': ['exact']}


class LocationModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = Serializationlocation
    queryset = TblLocation.objects.all()

# End of batch and location

#Sales and Transaction


class salestransaction(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = Serializationsalestransaction
    queryset = TblSalestransaction.objects.all()


class salestransactionFilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = Serializationsalestransaction
    queryset = TblSalestransaction.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'stockname': ['exact'], 'productcode': ['exact'],
                        'quantity': ['exact'], 'usedqty': ['exact'], 'status': ['in', 'exact'], 'rate': ['exact'], 'amount': ['exact'], 'cgstpercentage': ['exact'],
                        'sgstpercentage': ['exact'], 'total': ['exact'], 'sales': ['exact'], 'isdeleted': ['exact'], 'hsncode': ['exact'], 'task_invoiceno': ['exact']}


class sales(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationSales
    queryset = TblSales.objects.all()


class salesFilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationSales
    queryset = TblSales.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'supplier': ['exact'], 'company': ['exact'], 'amount': ['exact'],
                        'status': ['in', 'exact'], 'advancereceived': ['exact'], 'advanceused': ['exact'], 'dispatchdate': ['gte', 'lte', 'exact'], 'paymentterms': ['exact'], 'deliveryaddress': ['exact']}
# End of Sales and Transaction

# Sales quotation tables


class salesquotationrequest(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = Serializationquotationrequest
    queryset = TblQuotationrequest.objects.all()


class salesquotationFilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = Serializationquotationrequest
    queryset = TblQuotationrequest.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'supplier': ['exact'], 'company': ['exact'], 'amount': ['exact'],
                        'status': ['in', 'exact'], 'advancereceived': ['exact'], 'advanceused': ['exact'], 'dispatchdate': ['gte', 'lte', 'exact'], 'paymentterms': ['exact'], 'salesorderid': ['exact'], 'users': ['exact'], 'phoneno': ['exact']}


class salesquotationtransaction(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = Serializationquotationtransaction
    queryset = TblQuotationtransaction.objects.all()


class salesquotationtransactionFilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = Serializationquotationtransaction
    queryset = TblQuotationtransaction.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'stockname': ['exact'], 'productcode': ['exact'],
                        'quantity': ['exact'], 'usedqty': ['exact'], 'status': ['in', 'exact'], 'rate': ['exact'], 'amount': ['exact'], 'cgstpercentage': ['exact'],
                        'sgstpercentage': ['exact'], 'total': ['exact'], 'sales': ['exact'], 'isdeleted': ['exact'], 'hsncode': ['exact']}


# Sales quotation end


class expenses(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationExpenses
    queryset = TblExpenses.objects.all()


class expensesfilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationExpenses
    queryset = TblExpenses.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'date': ['gte', 'lte', 'exact'], 'itemname': ['exact'], 'purchasefrom': ['exact'], 'status': ['exact'],
                        'purchaseexpense': ['exact'], 'paid': ['exact'], 'amount': ['exact']}


class Ledgergroup(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationLedgergroup
    queryset = TblLedgergroups.objects.all()


class LedgergroupFilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationLedgergroup
    queryset = TblLedgergroups.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'ledgergroupname': [
        'exact'], 'isvisible': ['exact'], 'isdeleted': ['exact']}


class Ledgertype(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationLedgertype
    queryset = TblLedgertypes.objects.all()


class LedgertypeFilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationLedgertype
    queryset = TblLedgertypes.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'ledgertypename': [
        'exact'], 'ledgertypegroup': ['exact'], 'isvisible': ['exact']}


class UnitTypeView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationUnitType
    queryset = TblUnitType.objects.all()


class UnitTypefilter(generics.ListAPIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializationUnitType
    queryset = TblUnitType.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['exact'], 'unitname': [
        'exact'], }


@api_view(['GET'])
def current_user(request):

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# STORE PROCEDURE SECTION
