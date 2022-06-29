from django.contrib import admin
from django.urls import path, include
# from django.conf.urls import url
from TeamTask.view.calculating_balance_view import SpCalculateClosingBalance, SpCalculateOpeningBalance,SpReceivedAmountAdjustment
from TeamTask.views import UsersViewSet, Subtasks, SubtasksFilter, Subclients, Companyviewset, CompanyView

from rest_framework.routers import DefaultRouter
from TeamTask.views import Tasklistviewset, FiltersubtaskTime, Subtaskviewset, stockView, InvoicedetailView, Transactionviewset, TransactionFilterView
from TeamTask.views import UserdetailViewSet, UserdetailfilterView, TodoListView, stockFilterView, InvoicedetailFilter, stockInvoicedetailFilter
from TeamTask.views import ClientView, UsersFilter, PlandetailsViewSet, ClientFilter, stockInvoicedetailView
from TeamTask.views import current_user, UserList, InvoiceSummaryView, InvoiceSummaryFilterView, SubclientsFilterView
from TeamTask.views import Tasklistpaginationviewset, TodoListpaginationView, InvoiceSummaryFilterViewpagination, Bankviewset, Bankfilterview
from TeamTask.views import PurchaseStocks, PurchaseOrder, PurchaseStocksFilterView, PurchaseOrderFilterView
from TeamTask.views import UserpurchaseStocks, userpurchaserequestFilter, PurchaseInvocieFilter
from TeamTask.views import StockgroupView, ClientgroupView, StockgroupFilterView, ClientgroupFilterView, SalesRequestFilter, SalesRequestViews
from TeamTask.views import inventorytransaction, purchaseInvoice, BatchListApiView, BatchModelViewSet, LocationListApiView, LocationModelViewSet
from TeamTask.views import salestransaction, salestransactionFilter, sales, salesFilter
from TeamTask.views import VoucherManagementView, VoucherManagementfilter, VoucherDetailstView, VoucherDetailsfilter, Ledgergroup, LedgergroupFilter, Ledgertype, LedgertypeFilter
from TeamTask.views import PurchaseInvoiceStockFilter, PurchaseInvoiceStock
from TeamTask.views import salesquotationrequest, salesquotationFilter, salesquotationtransaction, salesquotationtransactionFilter, UnitTypefilter, UnitTypeView,Projectsfilter,ProjectsView
# ,InvoiceSummaryNonNullsalesorder JoinWorktimeView
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from TeamTask.views import Taxyear
from TeamTask.views import inventorytransactionFilter, expenses, expensesfilter
#PURCHASE ORDER VIEW
from TeamTask.view.purcharseorder_view import SpCreatePOwithUserRequest,SpDeletePurchaseOrder,SpPurchaseOrder,SpUpdatePurchaseOrder,SpReceiptHandling,SpCreatePurchaseStock,SpDeletePurchaseStock
from TeamTask.view.project_view import SpProjects,SpEditProjects,Sp_CreateProjectInvoiceDetails,SPUpdateProjectStatus,SpProjectTaskAmountCalculation
from TeamTask.view.salesorder_view import SpCreateSOwithQuotation,SpDeleteSalesorder,SpEditSalesTransaction,SpSalesQuotation,SpSalesTransaction,SpCreateQuoatationwithClientDetails,SpAddSalestockWithSalesRequest,SpDeleteSalesStock,SpMoveToDispatch,SpDispatchHandling
from TeamTask.view.invoice_view import sp_makeInvoice,sp_createinvocieandtransaction,sp_getcompanygreaterinvoice,sp_cancelinvoice,sp_payforcurrentinvoicetask,sp_updatecurrentinvoice
from TeamTask.view.invoice_view import getinvoicewithfilterdata,sp_moveselectedinvoice,sp_taskinvoiceinventorytransaction,sp_payforunpaidinvoice,SpDaterangeInvoiceReceivedAmount,SpJoinTransaction
from TeamTask.view.invoice_view import SpGetAvailableQTYTemptable,SpSummarizedBalance,SpTransactionOverView,JoinInvoiceSummaryRaw,Transactiondetails,sptransaction2
# from TeamTask.view.invoice_view import 
from TeamTask.view.availablity_view import SpAvailableStockbatch,SpGetAvailableStockQuantity, SpStoreDraftingCharges, SpStoreOutwardStock
from TeamTask.view.voucher_view import SpVoucherManagement
# SpAvailableStocknamesAndQuantity
router = DefaultRouter()
router.register(r'Tasklist', Tasklistviewset, basename='Tasklistis')
router.register(r'tasklistpagenation', Tasklistpaginationviewset,
                basename='tasklistpagenation')
router.register(r'subtasktime', Subtaskviewset, basename='Todosubtask')
router.register(r'users', UsersViewSet, basename='users')
router.register(r'userdetail', UserdetailViewSet, basename='userdetail')
router.register(r'client', ClientView)
router.register(r'Plans', PlandetailsViewSet)
router.register(r'subtasks', Subtasks)
router.register(r'stocks', stockView, basename='stocks')
router.register(r'invoice', InvoicedetailView, basename='invoivedetail')
router.register(r'stockinvoice', stockInvoicedetailView)
router.register(r'summary', InvoiceSummaryView)
router.register(r'subclients', Subclients)
router.register(r'transactions', Transactionviewset)
router.register(r'taxyear', Taxyear)
router.register(r'company', Companyviewset)
router.register(r'bank', Bankviewset)
router.register(r'purchasestock', PurchaseStocks)
router.register(r'purchaseorder', PurchaseOrder)
router.register(r'purchaserequest', UserpurchaseStocks)
router.register(r'clientgroup', ClientgroupView)
router.register(r'stockgroup', StockgroupView)
router.register(r'inventorytransaction', inventorytransaction)
router.register(r'purchaseinvoice', purchaseInvoice)
router.register(r'batch', BatchModelViewSet)
router.register(r'location', LocationModelViewSet)
router.register(r'salestransaction', salestransaction)
router.register(r'sales', sales)
router.register(r'expenses', expenses)
router.register(r'salesrequest', SalesRequestViews)
router.register(r'vouchermanagement', VoucherManagementView)
router.register(r'voucherdetails', VoucherDetailstView)
router.register(r'purchasebill', PurchaseInvoiceStock)
router.register(r'ledgergroup', Ledgergroup)
router.register(r'ledgertype', Ledgertype)
router.register(r'salesquotation', salesquotationrequest)
router.register(r'salesquotationtransaction', salesquotationtransaction)
router.register(r'unittype', UnitTypeView)
router.register(r'project', ProjectsView)

urlpatterns = [
    path('', include(router.urls)),
    path('current_user/', current_user),
    path('user/', UserList.as_view()),
    path('token-auth/', obtain_jwt_token),
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('userdetailfilter/', UserdetailfilterView.as_view()),
    path('tasklistfilter/', TodoListView.as_view()),
    path('tasklistfilterpagination/', TodoListpaginationView.as_view()),
    path('userfilter/', UsersFilter.as_view()),
    path('clientFilter/', ClientFilter.as_view()),
    path('subtaskTimeFilter/', FiltersubtaskTime.as_view()),
    path('subtasksfilter/', SubtasksFilter.as_view()),
    path('stockfilter/', stockFilterView.as_view()),
    path('invoicefilter/', InvoicedetailFilter.as_view()),
    path('stockinvoicefilter/', stockInvoicedetailFilter.as_view()),
    path('summaryfilter/', InvoiceSummaryFilterView.as_view()),
    path('summaryfilterpagination/', InvoiceSummaryFilterViewpagination.as_view()),
    path('subclientfilter/', SubclientsFilterView.as_view()),
    path('transactionfilter/', TransactionFilterView.as_view()),
    path('clientgroupfilter/', ClientgroupFilterView.as_view()),
    path('stockgroupfilter/', StockgroupFilterView.as_view()),
    path('companyfilter/', CompanyView.as_view()),
    path('bankfilter/', Bankfilterview.as_view()),
    #Inventory and purchase
    path('purchasestockfilter/', PurchaseStocksFilterView.as_view()),
    path('purchaseorderfilter/', PurchaseOrderFilterView.as_view()),
    path('purchaserequestfilter/', userpurchaserequestFilter.as_view()),
    path('inventorytransactionfilter/', inventorytransactionFilter.as_view()),
    path('locationfilter/', LocationListApiView.as_view()),
    path('batchfilter/', BatchListApiView.as_view()),
    path('salestransactionfilter/', salestransactionFilter.as_view()),
    path('salesfilter/', salesFilter.as_view()),
    path('expensesfilter/', expensesfilter.as_view()),
    path('salesrequestfilter/', SalesRequestFilter.as_view()),
    path('purchaseinvoicebillfilter/', PurchaseInvocieFilter.as_view()),
    path('vouchermanagementfilter/', VoucherManagementfilter.as_view()),
    path('voucherdetailsfilter/', VoucherDetailsfilter.as_view()),
    path('purchasebillinvoicefilter/', PurchaseInvoiceStockFilter.as_view()),
    path('ledgertypefilter/', LedgertypeFilter.as_view()),
    path('ledgergroupfilter/', LedgergroupFilter.as_view()),
    path('quotationfilter/', salesquotationFilter.as_view()),
    path('quotaiontransactionfilter/', salesquotationtransactionFilter.as_view()),
    path('unittypefilter/', UnitTypefilter.as_view()),
    path('projectfilter/', Projectsfilter.as_view()),
    #PROJECT STOREPROC
    path('sp_createprojectinvoicedetails/', Sp_CreateProjectInvoiceDetails.as_view()),
    path('sp_createproject/', SpProjects.as_view()),
    path('sp_editprojcts/', SpEditProjects.as_view()),
    path('updateprojectstatus/',SPUpdateProjectStatus.as_view()),
    path('projecttaskamountcalculation/',SpProjectTaskAmountCalculation.as_view()),
    #INVOICE STOREPROC
    path('makeinvoice/', sp_makeInvoice.as_view()),
    path('sp_createinvocieandtransaction/', sp_createinvocieandtransaction.as_view()),
    path('sp_getcompanygreaterinvoice/',sp_getcompanygreaterinvoice.as_view()),
    path('sp_cancelinvoice/',sp_cancelinvoice.as_view()),
    path('sp_payforcurrentinvoicetask/',sp_payforcurrentinvoicetask.as_view()),
    path('sp_updatecurrentinvoice/',sp_updatecurrentinvoice.as_view()),
    path('sp_moveselectedinvoice/',sp_moveselectedinvoice.as_view()),
    path('getinvoicewithfilterdata/', getinvoicewithfilterdata),
    path('sp_payforunpaidinvoice/',sp_payforunpaidinvoice.as_view()),
    path('sp_taskinvoiceinventorytransaction/',sp_taskinvoiceinventorytransaction.as_view()),
    path('daterangeinvoicereceivedamount/',SpDaterangeInvoiceReceivedAmount.as_view()),
    path('jointransaction/',SpJoinTransaction.as_view()),
    path('getavailableqtytemplate/',SpGetAvailableQTYTemptable.as_view()),
    path('summarizedbalance/',SpSummarizedBalance.as_view()),
    path('sptransactionoverview/',SpTransactionOverView.as_view()),
    path('jointclientdetails/',JoinInvoiceSummaryRaw.as_view()),
    path('transactiondetails/',Transactiondetails.as_view()),
    #PURCHASE ORDER STORED PROCEDURE
    path('sp_purchaseorder/', SpPurchaseOrder.as_view()),
    path('sp_updatepurchaseorder/', SpUpdatePurchaseOrder.as_view()),
    path('sp_createpowithuserrequest/', SpCreatePOwithUserRequest.as_view()),
    path('sp_deletepurchaseorder/', SpDeletePurchaseOrder.as_view()),
    path('sp_receipthandling/',SpReceiptHandling.as_view()),
    path('sp_createpurchasestock/',SpCreatePurchaseStock.as_view()),
    path("sp_deletepurchasestock/",SpDeletePurchaseStock.as_view()),
    #SALES ORDER STORED PROCEDURE
    path('sp_salestransaction/', SpSalesTransaction.as_view()),
    path('sp_editsalestransaction/', SpEditSalesTransaction.as_view()),
    path('sp_salesquotation/', SpSalesQuotation.as_view()),
    path('sp_createsowithquotation/', SpCreateSOwithQuotation.as_view()),
    path('sp_deletesalesorder/', SpDeleteSalesorder.as_view()),
    path('sp_createquotationwithclientdetails/',SpCreateQuoatationwithClientDetails.as_view()),
    path('sp_addsalestockwithsalesrequest/',SpAddSalestockWithSalesRequest.as_view()),
    path('sp_deletesalesstock/',SpDeleteSalesStock.as_view()),
    path('sp_movetodispatch/',SpMoveToDispatch.as_view()),
    path('sp_dispatchhandling/',SpDispatchHandling.as_view()),
    path('sp_calculateclosingbalance/',SpCalculateClosingBalance.as_view()),
    path('sp_calculateopeningbalance/',SpCalculateOpeningBalance.as_view()),
    path('sp_receivedamountadjustment/',SpReceivedAmountAdjustment.as_view()),
    path('sp_availablestockbatch/',SpAvailableStockbatch.as_view()),
    path('sp_getavailablestockquantity/',SpGetAvailableStockQuantity.as_view()),
    path('sp_storeoutwardstock/',SpStoreOutwardStock.as_view()),
    path('sp_storedraftingcharges/',SpStoreDraftingCharges.as_view()),
    path('sp_vouchermanagement/',SpVoucherManagement.as_view()),
    path('sptransaction2/',sptransaction2.as_view()),    
]

