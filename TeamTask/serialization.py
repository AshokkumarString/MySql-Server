from django.db.models import fields
from rest_framework import serializers
import django_filters

from TeamTask.models import TblClientGroup, TblStockGroup, TblSubtasktime
from TeamTask.models import TblTasklist
from TeamTask.models import Users
from TeamTask.models import Userdetail, TblPurchaseorder, TblPurchasestocks, TblSalesrequest
from TeamTask.models import TblClient, TblBank
from TeamTask.models import Plantype, TblSubtask, TblInvoicesummary, TblTransaction, TblWorkTimeTable
from TeamTask.models import TblStock, TblTaskinvoice, TblStockinvoice, TblTaxyear
from TeamTask.models import TblSubclient, TblCompany, TblPurchaseUserrequest, TblInventorytransaction
from TeamTask.models import TblStockGroup, TblClientGroup, TblPurchasebillinvoice, TblBatch, TblLocation
from TeamTask.models import TblSales, TblSalestransaction, TblExpenses, TblVouchermanagement, TblVoucherdetails
from TeamTask.models import TblPurchasebillstocks
from TeamTask.models import TblLedgergroups, TblLedgertypes, TblQuotationrequest, TblQuotationtransaction, TblUnitType, \
    TblProjects
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password')


class SerializationNewSubtask(serializers.ModelSerializer):
    class Meta:
        model = TblSubtasktime
        fields = '__all__'


class SerializationSubtasks(serializers.ModelSerializer):
    subtaskTime = SerializationNewSubtask(read_only=True, many=True)

    class Meta:
        model = TblSubtask
        fields = '__all__'


class SerializeJoinWorktime(serializers.ModelSerializer):
    class Meta:
        model = TblWorkTimeTable
        fields = '__all__'



class serialization_bankname(serializers.ModelSerializer):
    companydetails_pk = serializers.PrimaryKeyRelatedField(
        queryset=TblCompany.objects.all(), source='companydetails_id'
    )
    class Meta:
        model = TblBank
        fields = '__all__'
        depth = 1

class serialization_companyname(serializers.ModelSerializer):
    class Meta:
        model = TblCompany
        fields = '__all__'


class serialization_bankname(serializers.ModelSerializer):
    class Meta:
        model = TblBank
        fields = '__all__'

class SerializationTransaction(serializers.ModelSerializer):
    transactiontaskid = serializers.PrimaryKeyRelatedField(allow_null=True,
                                                queryset=TblTasklist.objects.all(), source='transactiontask')
    
    userid_id=serializers.PrimaryKeyRelatedField(allow_null=True,
                                                queryset=Users.objects.all(), source='userid')
    transaction_clientid=serializers.PrimaryKeyRelatedField(allow_null=True,queryset=TblClient.objects.all(), source='transaction_client')
    companyid=serializers.PrimaryKeyRelatedField(allow_null=True,queryset=TblCompany.objects.all(), source='company_id')
    voucherid=serializers.PrimaryKeyRelatedField(allow_null=True,queryset=TblVouchermanagement.objects.all(), source='voucher')
   
    class Meta:
        model = TblTransaction
        fields = '__all__'
        depth=1

class SerializationUsers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class SerializationUserdetails(serializers.ModelSerializer):
    class Meta:
        model = Userdetail
        fields = '__all__'


class serializationPlandetails(serializers.ModelSerializer):
    class Meta:
        model = Plantype
        fields = '__all__'


class seralizationTblStock(serializers.ModelSerializer):
    class Meta:
        model = TblStock
        fields = '__all__'


class seralizationTblTaskinvoicedetails(serializers.ModelSerializer):
    class Meta:
        model = TblTaskinvoice
        fields = '__all__'


class seralizationTblStockinvoice(serializers.ModelSerializer):
    class Meta:
        model = TblStockinvoice
        fields = '__all__'



class SerializationTaskList(serializers.ModelSerializer):
    subtask = SerializationSubtasks(read_only=True, many=True)

    class Meta:
        model = TblTasklist
        fields = '__all__'

class SerializationSubClient(serializers.ModelSerializer):
    class Meta:
        model = TblSubclient
        fields = '__all__'


class SerializationVoucherDetails(serializers.ModelSerializer):
    class Meta:
        model = TblVoucherdetails
        fields = '__all__'


class SerializationVoucherManagement(serializers.ModelSerializer):
    vouchermanagement = SerializationVoucherDetails(read_only=True, many=True)
    voucher = SerializationTransaction(allow_null=True, read_only=True, many=True)

    class Meta:
        model = TblVouchermanagement
        fields = '__all__'

class SerializarionTaxyear(serializers.ModelSerializer):
    class Meta:
        model = TblTaxyear
        fields = '__all__'

class SerializarionPurchasestocks(serializers.ModelSerializer):
    class Meta:
        model = TblPurchasestocks
        fields = '__all__'


class SerializationPurchaseorder(serializers.ModelSerializer):
    purchasestock = SerializarionPurchasestocks(read_only=True, many=True)

    class Meta:
        model = TblPurchaseorder
        fields = '__all__'


class SerializarionUserpurchaserequest(serializers.ModelSerializer):
    class Meta:
        model = TblPurchaseUserrequest
        fields = '__all__'


class SerializationStockgroup(serializers.ModelSerializer):
    stockgroup = seralizationTblStock(read_only=True, many=True)

    class Meta:
        model = TblStockGroup
        fields = '__all__'


class Serializationsalestransaction(serializers.ModelSerializer):
    class Meta:
        model = TblSalestransaction
        fields = '__all__'


class SerializationClient(serializers.ModelSerializer):
    clients = SerializationSubClient(read_only=True, many=True)
    client = SerializationVoucherManagement(read_only=True, many=True)
    # transactionclient=SerializationTransaction(read_only=True, many=True)
    # invoicesummaryclient= seralizationTblInvoicesummary(read_only=True, many=True)
    class Meta:
        model = TblClient
        fields = '__all__'


class seralizationTblInvoicesummary(serializers.ModelSerializer):
    invoicesummaryclientid = serializers.PrimaryKeyRelatedField(allow_null=True,
                                                queryset=TblClient.objects.all(), source='invoicesummaryclient')
    tbltasklistid = serializers.PrimaryKeyRelatedField(allow_null=True,
                                                       queryset=TblTasklist.objects.all(), source='tbltasklist'
                                                       )
    projectid = serializers.PrimaryKeyRelatedField(allow_null=True,
                                                   queryset=TblProjects.objects.all(), source='project'
                                                   )
    invoice_companyid = serializers.PrimaryKeyRelatedField(allow_null=True,
                                                   queryset=TblCompany.objects.all(), source='invoice_company'
                                                   )
    task_invoiceno = Serializationsalestransaction(allow_null=True,
                                                  read_only=True, many=True)
  
    class Meta:
        model = TblInvoicesummary
        fields = '__all__'
        depth = 1


class SerializationCompany(serializers.ModelSerializer):
    company = SerializationTaskList(read_only=True, many=True)
    # company_id=SerializationTransaction(read_only=True,many=True)
    invoice_company=seralizationTblInvoicesummary(read_only=True,many=True)
    # company_id=SerializationTransaction(read_only=True,many=True)
    # companydetails=serialization_bankname(read_only=True, many=True)

    class Meta:
        model = TblCompany
        fields = '__all__'
        depth = 1


class SerializationClientgroup(serializers.ModelSerializer):
    clientgroup = SerializationClient(read_only=True, many=True)

    class Meta:
        model = TblClientGroup
        fields = '__all__'


class SerializationInventorytransaction(serializers.ModelSerializer):
    class Meta:
        model = TblInventorytransaction
        fields = '__all__'


class SerializationBillstocks(serializers.ModelSerializer):
    class Meta:
        model = TblPurchasebillstocks
        fields = '__all__'


class SerializationPurchaseInvocie(serializers.ModelSerializer):
    purchaseinvoice = SerializationInventorytransaction(allow_null=True,
                                                        read_only=True, many=True)
    bill = SerializationBillstocks(read_only=True, many=True)

    class Meta:
        model = TblPurchasebillinvoice
        fields = '__all__'


class Serializationbatch(serializers.ModelSerializer):
    class Meta:
        model = TblBatch
        fields = '__all__'


class Serializationlocation(serializers.ModelSerializer):
    class Meta:
        model = TblLocation
        fields = '__all__'


# sales




class SerializationExpenses(serializers.ModelSerializer):
    purchaseexpense = SerializationPurchaseInvocie(read_only=True, many=True)

    class Meta:
        model = TblExpenses
        fields = '__all__'


class SerializationSalesRequest(serializers.ModelSerializer):
    class Meta:
        model = TblSalesrequest
        fields = '__all__'



class SerializationSales(serializers.ModelSerializer):
    sales = Serializationsalestransaction(read_only=True, many=True)
    salesorder = seralizationTblInvoicesummary(read_only=True, many=True)

    class Meta:
        model = TblSales
        fields = '__all__'


class SerializationLedgertype(serializers.ModelSerializer): 
    class Meta:
        model = TblLedgertypes
        fields = '__all__'


class SerializationLedgergroup(serializers.ModelSerializer):
    ledgertypegroup = SerializationLedgertype(read_only=True, many=True)

    class Meta:
        model = TblLedgergroups
        fields = '__all__'


class Serializationquotationtransaction(serializers.ModelSerializer):
    class Meta:
        model = TblQuotationtransaction
        fields = '__all__'


class Serializationquotationrequest(serializers.ModelSerializer):
    salesquotation = Serializationquotationtransaction(
        read_only=True, many=True)

    class Meta:
        model = TblQuotationrequest
        fields = '__all__'


class SerializationUnitType(serializers.ModelSerializer):
    class Meta:
        model = TblUnitType
        fields = '__all__'


class SerializationProjects(serializers.ModelSerializer):
    taskproject=SerializationTaskList(read_only=True,many=True)
    project=seralizationTblInvoicesummary(read_only=True,many=True)

    class Meta:
        model = TblProjects
        fields = '__all__'



