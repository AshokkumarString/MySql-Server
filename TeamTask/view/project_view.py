from django.db.models import Max,Min,Sum
from django.http import Http404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import math
from datetime import datetime
from TeamTask import models
from TeamTask import serialization
from TeamTask.models import TblInvoicesummary, TblTasklist
from TeamTask.serialization import seralizationTblInvoicesummary, SerializationTaskList


# {
#     "clientid": "114",
#     "clientname": "ALFA INFRA STRUCTURES",
#     "subclient": "MADURA COATS",
#     "phonenumber": "sadsadfsdfsd",
#     "status": "Initiate",
#     "company": "2",
#     "companyname":"Pg Cadd Structures",
#     "projectname": "Django custom views",
#     "tasks":[
#         {
#             "plantype":"06Work Completion",
#             "drawingtitle":"NewConfiguration",
#             "taskname":"00506_MADURA COATS_NewConfiguration_20220430"
#         },
#         {
#             "plantype":"15SiteLayouts",
#             "drawingtitle":"TestingNewConfiguration",
#             "taskname":"00515_MADURA COATS_TestingNewConfiguration_20220430"
#         },
#         {
#             "plantype":"03Structural Plan",
#             "drawingtitle":"sadfshfsdf",
#             "taskname":"00503_MADURA COATS_sadfshfsdf_20220430"
#         }
#     ]
# }

class SpProjects(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serialization.SerializationProjects

    def post(self, request):
        serializer = serialization.SerializationProjects(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                self.create_project_task(request.data['tasks'], request.data)
                return Response("sucessfully created",status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  # ToDo:  check response status
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)
    def create_project_task(self, tasks, requestdata):
        for taskdetails in tasks:
            latestid = models.TblProjects.objects.latest('id').id
            currentdate = datetime.today().strftime('%Y-%m-%d')
            maintask_dict = {
                "date": currentdate,
                "task": taskdetails['taskname'],
                "assignto": "General",
                "priority": "Medium",
                "startdate": currentdate,
                "enddate": currentdate,
                "status": "ToDo",
                "time": "00:00",
                "isdeleted": "0",
                "plantype": taskdetails['plantype'],
                "subclient": requestdata['subclient'],
                "clientname": requestdata['clientname'],
                "advanceamount": "0",
                "drawingtitle": taskdetails['drawingtitle'],
                "projectname": requestdata['projectname'],
                "companyname": requestdata['companyname'],
                "client": requestdata['clientid'],
                "taskproject": latestid,
                "company": requestdata['company']
            }
            serializer = serialization.SerializationTaskList(data=maintask_dict)
            # try:
            if serializer.is_valid():
                serializer.save()
                latesttaskid = models.TblTasklist.objects.latest('id').id
                self.create_subtask(maintask_dict, latesttaskid)
            # except:
            #     print(serializer.errors)
            else:
                raise ValueError('Task serialisation failed', serializer.errors)

    def create_subtask(self, maintaskdetails, maintaskid):
        currentdate = datetime.today().strftime('%Y-%m-%d')
        subtask_dict = {
            "subtaskTime": [],
            "date": currentdate,
            "subtask": "Default",
            "assignto": maintaskdetails['assignto'],
            "priority": "Medium",
            "status": "ToDo",
            "time": "00:00",
            "isdeleted": "0",
            "completed_date": "",
            "task_starttime": "",
            "tasklist": maintaskid
        }
        serializer = serialization.SerializationSubtasks(data=subtask_dict)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError('Task serialisation failed', serializer.errors)

        # return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)


class SpEditProjects(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = serialization.SerializationProjects

    def post(self, request):
        serializer = serialization.SerializationProjects(models.TblProjects.objects.get(pk=request.data['id']),
                                                         request.data)
        if serializer.is_valid():
            serializer.save()
            Response(serializer.data)
            self.updateandcreate_Project_Task(request.data['tasks'], request.data)
        return Response(request.data)

    def updateandcreate_Project_Task(self, tasks, requestdata):
        try:
            for taskdetails in tasks:
                print(taskdetails)
                taskid = models.TblTasklist.objects.filter(id=taskdetails['id'],taskproject=requestdata['id']).values("id")
                arraylen = len(taskid)
                if arraylen == 0:
                    currentdate = datetime.today().strftime('%Y-%m-%d')
                    maintask_dict = {
                        "date": currentdate,
                        "task": taskdetails['taskname'],
                        "assignto": "General",
                        "priority": "Medium",
                        "startdate": currentdate,
                        "enddate": currentdate,
                        "status": "ToDo",
                        "time": "00:00",
                        "isdeleted": "0",
                        "plantype": taskdetails['plantype'],
                        "subclient": requestdata['subclient'],
                        "clientname": requestdata['clientname'],
                        "advanceamount": "0",
                        "drawingtitle": taskdetails['drawingtitle'],
                        "projectname": requestdata['projectname'],
                        "companyname": requestdata['companyname'],
                        "client": requestdata['clientid'],
                        "taskproject": requestdata['id'],
                        "company": requestdata['company']
                    }
                    createserializer = serialization.SerializationTaskList(data=maintask_dict)
                    if createserializer.is_valid():
                        createserializer.save()
                        latesttaskid = models.TblTasklist.objects.latest('id').id
                        self.create_subtask(maintask_dict, latesttaskid)
                    else:
                        raise ValueError('Task serialisation failed', createserializer.errors)
                else:
                    updatemaintask_dict = {
                        "task": taskdetails['taskname'],
                        "plantype": taskdetails['plantype'],
                        "drawingtitle": taskdetails['drawingtitle'],
                        "client": requestdata['clientid'],
                        "taskproject": requestdata['id'],
                        "company": requestdata['company']
                    }
                    updatetasklistserializer = serialization.SerializationTaskList(
                        models.TblTasklist.objects.get(pk=taskdetails['id']), updatemaintask_dict)
                    if updatetasklistserializer.is_valid():
                        updatetasklistserializer.save()
                    else:
                        raise ValueError('Task serialisation failed', updatetasklistserializer.errors)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    def create_subtask(self, maintaskdetails, maintaskid):
        currentdate = datetime.today().strftime('%Y-%m-%d')
        subtask_dict = {
            "subtaskTime": [],
            "date": currentdate,
            "subtask": "Default",
            "assignto": maintaskdetails['assignto'],
            "priority": "Medium",
            "status": "ToDo",
            "time": "00:00",
            "isdeleted": "0",
            "completed_date": "",
            "task_starttime": "",
            "tasklist": maintaskid
        }
        serializer = serialization.SerializationSubtasks(data=subtask_dict)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError('Task serialisation failed', serializer.errors)

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


class Sp_CreateProjectInvoiceDetails(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = seralizationTblInvoicesummary

    def get_object(self, pk):
        try:
            return TblTasklist.objects.get(pk=pk)
        except TblTasklist.DoesNotExist:
            raise Http404

    def post(self, request):
        try:
            res = TblInvoicesummary.objects.filter(invoice_company=request.data['companyid']).aggregate(
                max_id=Max('deliverynoteid'))
            maxid = res['max_id']
            request.data["deliverynoteid"] = maxid + 1
            serializer = seralizationTblInvoicesummary(data=request.data)
            if serializer.is_valid():
                serializer.save()
                self.invoice_transaction(request.data)
                for projecttaskid in request.data['projecttaskids']:
                    queryset = TblTasklist.objects.filter(id=projecttaskid).values()
                    taskstatus = queryset[0]["status"]
                    if taskstatus == "Pending":
                        snippet = self.get_object(projecttaskid)
                        statusupdateddata = queryset[0];
                        statusupdateddata['status'] = 'Completed'
                        my_dict = {
                            'status': 'Completed',
                            'client': queryset[0]['client_id'],
                            'taskproject': queryset[0]['taskproject_id'],
                            'company': queryset[0]['company_id'],
                            'invoiceidno': maxid + 1
                        }
                        responsedetails = SerializationTaskList(snippet, data=my_dict)
                        if responsedetails.is_valid():
                            responsedetails.save()
                            subtaskqueryset = models.TblSubtask.objects.filter(status__in=["Pending", "Todo"],
                                                                            tasklist_id=projecttaskid).values()
                            self.cloningpending_task_subtask(queryset, subtaskqueryset)
                            for subtask in subtaskqueryset:
                                subtask_dict = {
                                    'status': 'Completed',
                                    'tasklist': subtask['tasklist_id']
                                }
                                subtaskserialization = serialization.SerializationSubtasks(
                                    models.TblSubtask.objects.get(pk=subtask['id']), data=subtask_dict)
                                if subtaskserialization.is_valid():
                                    subtaskserialization.save()
                    else:
                        if taskstatus == "Completed":
                            snippet = self.get_object(projecttaskid)
                            my_dict = {
                                'client': queryset[0]['client_id'],
                                'taskproject': queryset[0]['taskproject_id'],
                                'company': queryset[0]['company_id'],
                                'invoiceidno': maxid + 1
                            }
                            responsedetails = SerializationTaskList(snippet, data=my_dict)
                            if responsedetails.is_valid():
                                responsedetails.save()
                                subtaskqueryset = models.TblSubtask.objects.filter(status__in=["Pending", "Todo"],
                                                                                tasklist_id=projecttaskid).values()
                                self.complete_subtask(subtaskqueryset)
                                for subtask in subtaskqueryset:
                                    subtask_dict = {
                                        'status': 'Completed',
                                        'tasklist': subtask['tasklist_id']
                                    }
                                    subtaskserialization = serialization.SerializationSubtasks(
                                        models.TblSubtask.objects.get(pk=subtask['id']), data=subtask_dict)
                                    if subtaskserialization.is_valid():
                                        subtaskserialization.save()
                                        Response(subtaskserialization.data)
                                Response(responsedetails.data)
                            Response(responsedetails.errors)
            return Response(serializer.errors)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    def invoice_transaction(self, invoicedetilas):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        transaction_dict = {
            "transactiontaskid": "",
            "date": invoicedetilas['date'],
            "time": current_time,
            "amount": invoicedetilas['invoice_amount'],
            "deliverynoteid": invoicedetilas['deliverynoteid'],
            "originaldeliverynoteid": 0,
            "originalcompanyid": 0,
            "salesorderid": None,
            "transactiontype": "invoice",
            "companyid": invoicedetilas['companyid'],
            "transaction_clientid": invoicedetilas['client'],
            "userid_id": invoicedetilas['userid'],
            "voucherid":""
        }
        serializer = serialization.SerializationTransaction(data=transaction_dict)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError('transaction failed', serializer.errors)

    def cloningpending_task_subtask(self, maintask, subtask):
        maintask_dict = {
            "date": maintask[0]['date'],
            "task": maintask[0]['task'],
            "assignto": maintask[0]['assignto'],
            "priority": maintask[0]['priority'],
            "startdate": maintask[0]['startdate'],
            "enddate": maintask[0]['enddate'],
            "status": "Pending",
            "time": maintask[0]['time'],
            "isdeleted": maintask[0]['isdeleted'],
            "plantype": maintask[0]['plantype'],
            "subclient": maintask[0]['subclient'],
            "clientname": maintask[0]['clientname'],
            "advanceamount": maintask[0]['advanceamount'],
            "phonenumber": maintask[0]['phonenumber'],
            "drawingtitle": maintask[0]['drawingtitle'],
            "parenttaskid": maintask[0]['parenttaskid'],
            "projectname": maintask[0]['projectname'],
            "totalamount":0,
            "companyname": maintask[0]['companyname'],
            "invoiceidno": "",
            "client": maintask[0]['client_id'],
            "taskproject": maintask[0]['taskproject_id'],
            "company": maintask[0]['company_id']
        }
        cloneserializer = SerializationTaskList(data=maintask_dict)
        if cloneserializer.is_valid():
            cloneserializer.save()
            for subtaskdetails in subtask:
                subtask_dict = {
                    "date": subtaskdetails['date'],
                    "subtask": subtaskdetails['subtask'],
                    "assignto": subtaskdetails['assignto'],
                    "priority": subtaskdetails['priority'],
                    "status": subtaskdetails['status'],
                    "time": subtaskdetails['time'],
                    "isdeleted": subtaskdetails['isdeleted'],
                    "completed_date": subtaskdetails['completed_date'],
                    "task_starttime": subtaskdetails['task_starttime'],
                    "tasklist": cloneserializer.data['id']
                }
                subtaskserializer = serialization.SerializationSubtasks(data=subtask_dict)
                if subtaskserializer.is_valid():
                    subtaskserializer.save()
                else:
                    raise ValueError('subtask failed', subtaskserializer.errors)
        else:
            raise ValueError('tasklist failed', cloneserializer.errors)   

    def complete_subtask(self, subtask):
        for subtaskdetails in subtask:
            subtask_dict = {
                "date": subtaskdetails['date'],
                "subtask": subtaskdetails['subtask'],
                "assignto": subtaskdetails['assignto'],
                "priority": subtaskdetails['priority'],
                "status": "Completed",
                "time": subtaskdetails['time'],
                "isdeleted": subtaskdetails['isdeleted'],
                "completed_date": subtaskdetails['completed_date'],
                "task_starttime": subtaskdetails['task_starttime'],
                "tasklist": subtaskdetails['tasklist_id']
            }
            subtaskserializer = serialization.SerializationSubtasks(data=subtask_dict)
            if subtaskserializer.is_valid():
                subtaskserializer.save()
            else:
                raise ValueError('updateprojectamount failed', subtaskserializer.errors)


class SPUpdateProjectStatus(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = seralizationTblInvoicesummary

    def put(self,request):
        try:
            print(request.data)
            data={
                "status":"InProgress"
            }
            filterdata=models.TblTasklist.objects.filter(id=request.data['taskid']).values('taskproject_id')
            querysetdata=serialization.SerializationProjects(models.TblProjects.objects.get(pk=filterdata[0]['taskproject_id']),data=data)
            if querysetdata.is_valid():
                querysetdata.save()
            return Response(querysetdata.errors)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

class SpProjectTaskAmountCalculation(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        import datetime
        import math
        draftingcharges=0
        printingchargers=0
        try:
            filterdata=models.TblSubtask.objects.filter(tasklist_id=request.data['taskid']).values()
            for subtask in filterdata:
                subtasktimefilter=models.TblSubtasktime.objects.filter(subtask_id=subtask['id']).values()
                time='00:00'
                for indivutal in subtasktimefilter:
                    t1 = datetime.datetime.strptime(indivutal['time'], '%H:%M')
                    t2 = datetime.datetime.strptime(time, '%H:%M')
                    time_zero = datetime.datetime.strptime('00:00', '%H:%M')
                    time=(t1 - time_zero + t2).time()
                    time=str(time.hour)+':'+str(time.minute)
                    # print(time)
            # print(filterdata)
                subtask['time']=time
            for subtaskdetails in filterdata:
                defaultamount_dict=models.Users.objects.filter(name=subtaskdetails['assignto']).values('default_rate')
                defaultamount=int(defaultamount_dict[0]['default_rate'])
                print(defaultamount) 
                timesubtask=subtaskdetails['time']
                hour,minute=timesubtask.split(':')
                print(hour,minute)
                hourtotalamount=int(hour)*defaultamount+math.ceil(int(minute)*defaultamount/60)
                draftingcharges=hourtotalamount+draftingcharges
                print(hourtotalamount)
                print(subtaskdetails)
            printingchargers=models.TblStockinvoice.objects.filter(tasklistrow=request.data['taskid']).aggregate(Sum('amount'))
            print(printingchargers,"line452")
            print(models.TblStockinvoice.objects.filter(tasklistrow=request.data['taskid']))
            printing= 0 if printingchargers['amount__sum']==None else  printingchargers['amount__sum']
            printingchargers= 0 if draftingcharges==None else  draftingcharges
            currenttask=models.TblTasklist.objects.filter(id=request.data['taskid']).values()
            # print(currenttask[0])
            # print(currenttask[0]['client_id'])
            print(draftingcharges, printing)
            tasklist_dict={
                "totalamount":draftingcharges+printing,
                "client":currenttask[0]['client_id'],
                "company":currenttask[0]['company_id']
            }
            queryset=serialization.SerializationTaskList(models.TblTasklist.objects.get(pk=request.data['taskid']),tasklist_dict)
            if queryset.is_valid():
                queryset.save()
                self.update_projecttotalamount(currenttask[0]['taskproject_id'])
            return Response(queryset.errors)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)
        
    def update_projecttotalamount(self,projectid):
            totalamount=models.TblTasklist.objects.filter(taskproject_id=projectid).aggregate(Sum('totalamount'))
            print(totalamount)
            project_dict={
                "totalamount":totalamount['totalamount__sum'],
            }
            update_projects=serialization.SerializationProjects(models.TblProjects.objects.get(pk=projectid),project_dict) 
            if update_projects.is_valid():
               update_projects.save()
            else:
                raise ValueError('updateprojectamount failed', update_projects.errors)

           
       




