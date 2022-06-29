from http import client
from django.db.models import Q
from django.http import Http404
#from django.core import serializers
from rest_framework import serializers 
from rest_framework import status

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from TeamTask import models
from TeamTask import serialization
from TeamTask.models import TblBank, TblInvoicesummary, TblTasklist, TblTransaction, TblVouchermanagement
from TeamTask.serialization import serialization_bankname, seralizationTblInvoicesummary, SerializationTaskList


# First Storeproc Convert into Python django
# testing
# {
#     "userid": "17",
#     "client": "119",
#     "invoicestatus":"Unpaid",
#     "invoice_amount": "200",
#     "subtotal": "1999",
#     "date": "2022-04-29",
#     "companyid": "1",
#     "projectid": "58",
#     "tbltasklistid": null,
#     "projecttaskids":[9176,56,57,58]
# }


# class SP_CreateProjectInvoicedetails(APIView):
#     # Sp_createProjectInvoice
#     authentication_classes = [SessionAuthentication,
#                               BasicAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = seralizationTblInvoicesummary

#     def get_object(self, pk):
#         try:
#             return TblTasklist.objects.get(pk=pk)
#         except TblTasklist.DoesNotExist:
#             raise Http404

#     def post(self, request):
#         message = "check the details"
#         res = TblInvoicesummary.objects.filter(companyid=request.data['companyid']).aggregate(
#             max_id=Max('deliverynoteid'))
#         maxid = res['max_id']
#         request.data["deliverynoteid"] = maxid + 1
#         # request.data["tbltasklistid"]=""
#         # print(request.data)
#         serializer = seralizationTblInvoicesummary(data=request.data)
#         # print(serializer)
#         if serializer.is_valid():
#             serializer.save()
#             message = 'bankname {0}'
#             Response({'message': message})
#             self.invoice_Transaction(request.data)
#             for projecttaskid in request.data['projecttaskids']:
#                 print(projecttaskid)
#                 queryset = TblTasklist.objects.filter(id=projecttaskid).values()
#                 # print(queryset[0])
#                 # print(queryset[0])
#                 status = queryset[0]["status"]
#                 print(status)
#                 if status == "Pending":
#                     snippet = self.get_object(projecttaskid)
#                     # print(snippet,"PutOperation",projecttaskid)
#                     statusupdateddata = queryset[0];
#                     # print(statusupdateddata)
#                     statusupdateddata['status'] = 'Completed'
#                     my_dict = {
#                         'status': 'Completed',
#                         'client': queryset[0]['client_id'],
#                         'totalamount': '0',
#                         'taskproject': queryset[0]['taskproject_id'],
#                         'company': queryset[0]['company_id'],
#                         'invoiceidno': maxid + 1
#                     }
#                     # print(my_dict,snippet)
#                     responsedetails = serializationNewTodolist(snippet, data=my_dict)
#                     # print(responsedetails)
#                     if responsedetails.is_valid():
#                         # print(responsedetails,"fdgfgh")
#                         responsedetails.save()
#                         subtaskqueryset = models.TblSubtask.objects.filter(status__in=["Pending", "Todo"],
#                                                                            tasklist_id=projecttaskid).values()
#                         self.cloningPending_Task_Subtask(queryset, subtaskqueryset)
#                         # print(projecttaskid)
#                         # print(queryset)
#                         for subtask in subtaskqueryset:
#                             subtask_dict = {
#                                 'status': 'Completed',
#                                 'tasklist': subtask['tasklist_id']
#                             }
#                             # print(subtask_dict)
#                             # print(subtask)
#                             subtaskserialization = serialization.serializationSubtasks(
#                                 models.TblSubtask.objects.get(pk=subtask['id']), data=subtask_dict)
#                             # print(responsedetails)
#                             if subtaskserialization.is_valid():
#                                 #    print(subtaskserialization,"fdgfgh")
#                                 subtaskserialization.save()
#                                 Response(subtaskserialization.data)
#                         Response(responsedetails.data)
#                     Response(responsedetails.errors)
#                 else:
#                     if status == "Completed":
#                         snippet = self.get_object(projecttaskid)
#                         # print(snippet,"PutOperation",projecttaskid)
#                         # print(statusupdateddata)
#                         my_dict = {
#                             'client': queryset[0]['client_id'],
#                             'totalamount': '0',
#                             'taskproject': queryset[0]['taskproject_id'],
#                             'company': queryset[0]['company_id'],
#                             'invoiceidno': maxid + 1
#                         }
#                         # print(my_dict,snippet)
#                         responsedetails = serializationNewTodolist(snippet, data=my_dict)
#                         # print(responsedetails)
#                         if responsedetails.is_valid():
#                             # print(responsedetails,"fdgfgh")
#                             responsedetails.save()
#                             subtaskqueryset = models.TblSubtask.objects.filter(status__in=["Pending", "Todo"],
#                                                                                tasklist_id=projecttaskid).values()
#                             self.complete_Subtask(subtaskqueryset)
#                             # print(projecttaskid)
#                             # print(queryset)
#                             for subtask in subtaskqueryset:
#                                 subtask_dict = {
#                                     'status': 'Completed',
#                                     'tasklist': subtask['tasklist_id']
#                                 }
#                                 subtaskserialization = serialization.serializationSubtasks(
#                                     models.TblSubtask.objects.get(pk=subtask['id']), data=subtask_dict)
#                                 # print(responsedetails)
#                                 if subtaskserialization.is_valid():
#                                     #    print(subtaskserialization,"fdgfgh")
#                                     subtaskserialization.save()
#                                     Response(subtaskserialization.data)
#                             Response(responsedetails.data)
#                         Response(responsedetails.errors)

#         return Response(serializer.errors)

#     def invoice_Transaction(self, invoicedetilas):
#         # please update clientgroupid after applying the details
#         print(invoicedetilas)
#         now = datetime.now()
#         current_time = now.strftime("%H:%M:%S")
#         transaction_dict = {
#             "taskid": "",
#             "date": invoicedetilas['date'],
#             "time": current_time,
#             "amount": invoicedetilas['invoice_amount'],
#             "deliverynoteid": invoicedetilas['deliverynoteid'],
#             "originaldeliverynoteid": 0,
#             "originalcompanyid": 0,
#             "salesorderid": None,
#             "transactiontype": "invoice",
#             "companyid": invoicedetilas['companyid'],
#             "clientid": invoicedetilas['client'],
#             "userid": invoicedetilas['userid'],
#         }
#         serializer = serialization.SerializationTransaction(data=transaction_dict)
#         if serializer.is_valid():
#             serializer.save()
#             message = 'bankname {0}'
#             Response({'message': message})
#         Response(serializer.errors)

#     def cloningPending_Task_Subtask(self, maintask, subtask):
#         print(subtask);
#         maintask_dict = {
#             "date": maintask[0]['date'],
#             "task": maintask[0]['task'],
#             "assignto": maintask[0]['assignto'],
#             "priority": maintask[0]['priority'],
#             "startdate": maintask[0]['startdate'],
#             "enddate": maintask[0]['enddate'],
#             "status": maintask[0]['status'],
#             "time": maintask[0]['time'],
#             "isdeleted": maintask[0]['isdeleted'],
#             "plantype": maintask[0]['plantype'],
#             "subclient": maintask[0]['subclient'],
#             "clientname": maintask[0]['clientname'],
#             "advanceamount": maintask[0]['advanceamount'],
#             "phonenumber": maintask[0]['phonenumber'],
#             "drawingtitle": maintask[0]['drawingtitle'],
#             "parenttaskid": maintask[0]['parenttaskid'],
#             "projectname": maintask[0]['projectname'],
#             "totalamount": maintask[0]['totalamount'],
#             "companyname": maintask[0]['companyname'],
#             "invoiceidno": maintask[0]['invoiceidno'],
#             "client": maintask[0]['client_id'],
#             "taskproject": maintask[0]['taskproject_id'],
#             "company": maintask[0]['company_id']
#         }
#         print(maintask_dict, "check the process of data")
#         cloneserializer = serializationNewTodolist(data=maintask_dict)
#         if cloneserializer.is_valid():
#             cloneserializer.save()
#             print(cloneserializer.data, "sadfsaghkfsadfhgsdjfg183")
#             Response("Maintask created")
#             for subtaskdetails in subtask:
#                 print(subtaskdetails)
#                 subtask_dict = {
#                     "date": subtaskdetails['date'],
#                     "subtask": subtaskdetails['subtask'],
#                     "assignto": subtaskdetails['assignto'],
#                     "priority": subtaskdetails['priority'],
#                     "status": subtaskdetails['status'],
#                     "time": subtaskdetails['time'],
#                     "isdeleted": subtaskdetails['isdeleted'],
#                     "completed_date": subtaskdetails['completed_date'],
#                     "task_starttime": subtaskdetails['task_starttime'],
#                     "tasklist": subtaskdetails['tasklist_id']
#                 }
#                 print(subtask_dict)
#                 subtaskserializer = serialization.serializationSubtasks(data=subtask_dict)
#                 print(subtaskserializer)
#                 if subtaskserializer.is_valid():
#                     subtaskserializer.save()
#                     Response("subtask created")
#                 return Response(subtaskserializer.errors)
#             return Response(cloneserializer.errors)

#     def complete_Subtask(self, subtask):
#         for subtaskdetails in subtask:
#             print(subtaskdetails)
#             subtask_dict = {
#                 "date": subtaskdetails['date'],
#                 "subtask": subtaskdetails['subtask'],
#                 "assignto": subtaskdetails['assignto'],
#                 "priority": subtaskdetails['priority'],
#                 "status": "Completed",
#                 "time": subtaskdetails['time'],
#                 "isdeleted": subtaskdetails['isdeleted'],
#                 "completed_date": subtaskdetails['completed_date'],
#                 "task_starttime": subtaskdetails['task_starttime'],
#                 "tasklist": subtaskdetails['tasklist_id']
#             }
#             print(subtask_dict)
#             subtaskserializer = serialization.serializationSubtasks(data=subtask_dict)
#             print(subtaskserializer)
#             if subtaskserializer.is_valid():
#                 subtaskserializer.save()
#                 Response("subtask created")
#             return Response(subtaskserializer.errors)
#         # print(serializer.data)
#         # print(request.data['projecttaskids'])


# # {
# #     "clientid": "114",
# #     "clientname": "ALFA INFRA STRUCTURES",
# #     "subclient": "MADURA COATS",
# #     "phonenumber": "sadsadfsdfsd",
# #     "status": "Initiate",
# #     "company": "2",
# #     "companyname":"Pg Cadd Structures",
# #     "projectname": "Django custom views",
# #     "tasks":[
# #         {
# #             "plantype":"06Work Completion",
# #             "drawingtitle":"NewConfiguration",
# #             "taskname":"00506_MADURA COATS_NewConfiguration_20220430"
# #         },
# #         {
# #             "plantype":"15SiteLayouts",
# #             "drawingtitle":"TestingNewConfiguration",
# #             "taskname":"00515_MADURA COATS_TestingNewConfiguration_20220430"
# #         },
# #         {
# #             "plantype":"03Structural Plan",
# #             "drawingtitle":"sadfshfsdf",
# #             "taskname":"00503_MADURA COATS_sadfshfsdf_20220430"
# #         }
# #     ]
# # }

# class SP_Projects(APIView):
#     authentication_classes = [SessionAuthentication,
#                               BasicAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     serializer_class = serialization.SerializationProjects

#     def post(self, request):
#         serializer = serialization.SerializationProjects(data=request.data)
#         print(request.data)
#         # print(serializer)
#         if serializer.is_valid():
#             serializer.save()
#             print("projects successfully created")
#             self.create_Project_Task(request.data['tasks'], request.data)
#             Response(serializer.data)
#         return Response(serializer.errors)

#     def create_Project_Task(self, tasks, requestdata):
#         print(tasks)
#         for taskdetails in tasks:
#             print(taskdetails)
#             latestid = models.TblProjects.objects.latest('id').id
#             print(latestid)
#             currentdate = datetime.today().strftime('%Y-%m-%d')
#             maintask_dict = {
#                 "date": currentdate,
#                 "task": taskdetails['taskname'],
#                 "assignto": "General",
#                 "priority": "Medium",
#                 "startdate": currentdate,
#                 "enddate": currentdate,
#                 "status": "ToDo",
#                 "time": "00:00",
#                 "isdeleted": "0",
#                 "plantype": taskdetails['plantype'],
#                 "subclient": requestdata['subclient'],
#                 "clientname": requestdata['clientname'],
#                 "advanceamount": "0",
#                 "drawingtitle": taskdetails['drawingtitle'],
#                 "projectname": requestdata['projectname'],
#                 "companyname": requestdata['companyname'],
#                 "client": requestdata['clientid'],
#                 "taskproject": latestid,
#                 "company": requestdata['company']
#             }
#             serializer = serialization.serializationNewTodolist(data=maintask_dict)
#             if serializer.is_valid():
#                 serializer.save()
#                 Response("maintaskcreated")
#                 print("maintask successfully created")
#                 latesttaskid = models.TblTasklist.objects.latest('id').id
#                 self.create_subtask(maintask_dict, latesttaskid)
#                 Response(serializer.errors)

#     def create_subtask(self, maintaskdetails, maintaskid):
#         currentdate = datetime.today().strftime('%Y-%m-%d')
#         subtask_dict = {
#             "subtaskTime": [],
#             "date": currentdate,
#             "subtask": "Default",
#             "assignto": maintaskdetails['assignto'],
#             "priority": "Medium",
#             "status": "ToDo",
#             "time": "00:00",
#             "isdeleted": "0",
#             "completed_date": "",
#             "task_starttime": "",
#             "tasklist": maintaskid
#         }
#         serializer = serialization.serializationSubtasks(data=subtask_dict)
#         if serializer.is_valid():
#             serializer.save()
#             print("Subtask successfully created")
#             Response("maintaskcreated")
#         Response(serializer.errors)


# class SP_EditProjects(APIView):
#     authentication_classes = [SessionAuthentication,
#                               BasicAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     serializer_class = serialization.SerializationProjects

#     def post(self, request):
#         serializer = serialization.SerializationProjects(models.TblProjects.objects.get(pk=request.data['id']),
#                                                          request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # print(serializer.data)
#             print("projects successfully created")
#             Response(serializer.data)
#             self.Updateandcreate_Project_Task(request.data['tasks'], request.data)
#         return Response(request.data)

#     def Updateandcreate_Project_Task(self, tasks, requestdata):
#         print(tasks)
#         for taskdetails in tasks:
#             print(taskdetails)
#             taskid = models.TblTasklist.objects.filter(id=taskdetails['id']).values("id")
#             print(taskid)
#             arraylen = len(taskid)
#             if arraylen == 0:
#                 currentdate = datetime.today().strftime('%Y-%m-%d')
#                 maintask_dict = {
#                     "date": currentdate,
#                     "task": taskdetails['taskname'],
#                     "assignto": "General",
#                     "priority": "Medium",
#                     "startdate": currentdate,
#                     "enddate": currentdate,
#                     "status": "ToDo",
#                     "time": "00:00",
#                     "isdeleted": "0",
#                     "plantype": taskdetails['plantype'],
#                     "subclient": requestdata['subclient'],
#                     "clientname": requestdata['clientname'],
#                     "advanceamount": "0",
#                     "drawingtitle": taskdetails['drawingtitle'],
#                     "projectname": requestdata['projectname'],
#                     "companyname": requestdata['companyname'],
#                     "client": requestdata['clientid'],
#                     "taskproject": requestdata['id'],
#                     "company": requestdata['company']
#                 }
#                 serializer = serialization.serializationNewTodolist(data=maintask_dict)
#                 if serializer.is_valid():
#                     serializer.save()
#                     Response("maintaskcreated")
#                     print("maintask successfully created")
#                     latesttaskid = models.TblTasklist.objects.latest('id').id
#                     self.create_subtask(maintask_dict, latesttaskid)
#                     Response(serializer.errors)
#             else:
#                 updatemaintask_dict = {
#                     "task": taskdetails['taskname'],
#                     "plantype": taskdetails['plantype'],
#                     "drawingtitle": taskdetails['drawingtitle'],
#                     "client": requestdata['clientid'],
#                     "taskproject": requestdata['id'],
#                     "company": requestdata['company']
#                 }
#                 serializer = serialization.serializationNewTodolist(
#                     models.TblTasklist.objects.get(pk=taskdetails['id']), updatemaintask_dict)
#                 if serializer.is_valid():
#                     serializer.save()
#                     Response(serializer.data)
#                     print('subtask update')
#                 Response(serializer.errors)

#     def create_subtask(self, maintaskdetails, maintaskid):
#         currentdate = datetime.today().strftime('%Y-%m-%d')
#         subtask_dict = {
#             "subtaskTime": [],
#             "date": currentdate,
#             "subtask": "Default",
#             "assignto": maintaskdetails['assignto'],
#             "priority": "Medium",
#             "status": "ToDo",
#             "time": "00:00",
#             "isdeleted": "0",
#             "completed_date": "",
#             "task_starttime": "",
#             "tasklist": maintaskid
#         }
#         serializer = serialization.serializationSubtasks(data=subtask_dict)
#         if serializer.is_valid():
#             serializer.save()
#             print("Subtask successfully created")
#             Response("maintaskcreated")
#         Response(serializer.errors)


# class SP_MakeInvoice(APIView):
#     authentication_classes = [SessionAuthentication,
#                               BasicAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     serializer_class = serialization.seralizationTblInvoicesummary

#     def post(self, request):
#         print(request.data)
#         res = TblInvoicesummary.objects.filter(companyid=request.data['companyid']).aggregate(
#             max_id=Max('companyinvoiceid'))
#         print(request.data['deliverynoteid'])
#         invoiceid = TblInvoicesummary.objects.filter(deliverynoteid=request.data['deliverynoteid']).values()
#         maxid = res['max_id']
#         print(maxid, "asdjhsagdfasd", invoiceid)
#         print(invoiceid[0]['id'])
#         updateinvoicesummary = {
#             "companyinvoiceid": maxid + 1,
#             "tbltasklistid": invoiceid[0]['tbltasklist_id'],
#             "projectid": invoiceid[0]['project_id']
#         }
#         serializer = serialization.seralizationTblInvoicesummary(
#             models.TblInvoicesummary.objects.get(pk=invoiceid[0]['id']), updateinvoicesummary)
#         print(serializer)
#         if serializer.is_valid():
#             serializer.save()
#             Response(serializer.data)
#         return Response(serializer.errors)


# udemy class learning
@api_view(['POST'])
def storebankname(request):
    bank = TblBank()
    bank.bankname = request.data['bankname']
    bank.accountno = request.data['accountno']
    bank.upi = request.data['upi']
    bank.comments = request.data['comments']
    bank.ifsc = request.data['ifsc']
    bank.companydetails_id = request.data['companydetails_id']
    bank.save()
    # status=status.HTTP_201_CREATED
    return Response(status=status.HTTP_201_CREATED)


class SP_CreateProjectInvoice1(APIView):
    def post(self, request):
        for projecttaskid in request.data['details']:

            serializer = serialization_bankname(data=projecttaskid)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# REferecence
class serializationbankdetailView(APIView):
    serializer_class = serialization_bankname

    def get_object(self, pk):
        try:
            return TblBank.objects.get(pk=pk)
        except TblBank.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = serialization_bankname(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        print(snippet, "PutOperation", pk)
        print(request.data)
        serializer = serialization_bankname(snippet, data=request.data)
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class serializationwithgetpost(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = serialization_bankname

    def get_object(self, pk):
        try:
            return TblBank.objects.get(pk=pk)
        except TblBank.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        snippets = TblBank.objects.all()
        serializer = serialization_bankname(snippets, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data, "Postoperation")
        serializer = serialization_bankname(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            # deleted=self.delete(serializer.data.get('id'))
            bankname = serializer.data.get('bankname')
            message = 'bankname {0}'.format(bankname)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        print(pk, "Working after post opertaion show to deleted the data")
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



            # cd E:\github current\WebSites\Projects\Wealthify\Django Apps

            # cd E:\github current\OrganServer

            # eb-virt\scripts\activate.bat


# joins .select_related()




class Testingapi(APIView):
    def post(self,request):
        a='2019-01-01'
        que=TblInvoicesummary.objects.filter(client=request.data['client']).values()
        return Response(que)
        #queryset=TblInvoicesummary.objects.select_related('invoice_company','tbltasklist','invoicesummaryclient').all()
        #serializer = serialization.seralizationTblInvoicesummary(queryset,many=True)
        # output=[]
        # for data in queryset:
        #     data={
        #         "id":data.id,
        #         "client":data.client,
        #         "invoice_amount":data.invoice_amount,
        #         "amount_received":data.amount_received,
        #         "invoicestatus":data.invoicestatus,
        #         "discount":data.discount,
        #         "subtotal":data.subtotal,
        #         "balancedue":data.balancedue,
        #         "duedate":data.duedate,
        #         "comments":data.comments,
        #         "tbltasklist_id":data.tbltasklist.id,
        #         "date":data.tbltasklist.date,
        #         "deliverynoteid":data.deliverynoteid,
        #         "ismoved":data.ismoved,
        #         "companyid":data.companyid,
        #         "originalcompanyid":data.originalcompanyid,
        #         "originaldeliverynoteid":data.originaldeliverynoteid,
        #         "companyinvoiceid":data.companyinvoiceid,
        #         "salesorder_id":data.salesorder,
        #         "vehiclenumber":data.vehiclenumber,
        #         "invoicetype":data.invoicetype,
        #         "clientgroupid_id":data.clientgroupid,
        #         "project_id":data.project,
        #         "invoicesummaryclient_id":data.invoicesummaryclient,
        #         "invoice_company_id":data.invoice_company.id,
        #         "receivedamount":data.amount_received,
        #         "invoiceamount":data.invoice_amount,
        #         "companyname":data.invoice_company.companyname,
        #         "companycode":data.invoice_company.companycode,
        #         "taskid":data.tbltasklist.id,
        #         "task":data.tbltasklist.task,
        #         "company_name":data.invoicesummaryclient.company_name,
        #         "engineer_name":data.invoicesummaryclient.engineer_name
        #     }
        #     output.append(data)
        return Response(serializer.data)




# class Testingapi(APIView):
#     def post(self,request):
#         queryset=models.TblTransaction.objects.select_related('clientid').filter(clientid=request.data['clientid']).values()
#         print(queryset)
        
        
#         serializer = serialization.SerializationTaskList(queryset, many=True)
        
#         for data in queryset:
#             print(data.clientid.engineer_name)
            
#         return Response(serializer.data, content_type="application/json")


#print(queryset[0]["engineer_name"])
        # for data in queryset:
        #     if data.taskproject is not None:
        #          print(data.taskproject.id)
        #           #b=data.clientid.engineer_name
        #          b=print(data.taskproject.projectname,"project name")
        #          print(data.taskproject.totalamount,"totalamount")
                 
        #          c = serializers.serialize(queryset)
                  #print(serilaize)
                  #print(serilaize)
                #   if serilaize.is_valid():
                #       serilaize.validated_data
##return HttpResponse(data, content_type="application/json")

# if data.taskproject is not None:
            #     c = serialization.SerializationTransaction('json',queryset)
            #     #c = serializers.Serializer('json',data.taskproject.projectname)
            #     #print(c,"works like charm")
            #     if c.is_valid():
            #       print('true')
            #       print(c)
            #     else:
            #         print("do it again")

            #queryset=TblTasklist.objects.select_related('taskproject').all()
        #print(queryset)


