# Generated by Django 3.1.4 on 2021-05-14 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plantype',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('planname', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'plantype',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblClient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('engineer_name', models.CharField(blank=True, db_column='Engineer_name', max_length=255, null=True)),
                ('emailid', models.CharField(blank=True, max_length=255, null=True)),
                ('phoneno', models.CharField(blank=True, db_column='phoneNo', max_length=255, null=True, unique=True)),
                ('clientid', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('isdeleted', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'tbl_client',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblInvoicesummary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.CharField(blank=True, db_column='DATE', max_length=100, null=True)),
                ('client', models.CharField(blank=True, db_column='CLIENT', max_length=100, null=True)),
                ('invoice_amount', models.CharField(blank=True, db_column='Invoice Amount', max_length=255, null=True)),
                ('amount_received', models.CharField(blank=True, db_column='Amount Received', max_length=255, null=True)),
                ('invoicestatus', models.CharField(blank=True, db_column='InvoiceStatus', max_length=255, null=True)),
                ('discount', models.CharField(blank=True, db_column='Discount', max_length=255, null=True)),
                ('subtotal', models.CharField(blank=True, db_column='Subtotal', max_length=255, null=True)),
                ('balancedue', models.CharField(blank=True, db_column='Balancedue', max_length=255, null=True)),
                ('paymentmode', models.CharField(blank=True, db_column='Paymentmode', max_length=255, null=True)),
                ('referenceno', models.CharField(blank=True, max_length=255, null=True)),
                ('duedate', models.CharField(blank=True, max_length=255, null=True)),
                ('comments', models.CharField(blank=True, db_column='Comments', max_length=255, null=True)),
            ],
            options={
                'db_table': 'tbl_invoicesummary',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblJoinInvoicesummary',
            fields=[
                ('inv_Id', models.IntegerField(primary_key=True, serialize=False)),
                ('client', models.CharField(blank=True, db_column='client', max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, db_column='company_name', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TblStock',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stockname', models.CharField(blank=True, db_column='Stockname', max_length=100, null=True)),
                ('defaultrate', models.CharField(blank=True, db_column='defaultRate', max_length=255, null=True)),
                ('unit', models.CharField(blank=True, max_length=255, null=True)),
                ('subunit', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'tbl_stock',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblSubtask',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.CharField(blank=True, db_column='Date', max_length=100, null=True)),
                ('subtask', models.CharField(blank=True, db_column='SubTask', max_length=100, null=True)),
                ('assignto', models.CharField(blank=True, db_column='AssignTo', max_length=100, null=True)),
                ('priority', models.CharField(blank=True, db_column='Priority', max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('time', models.CharField(blank=True, max_length=255, null=True)),
                ('isdeleted', models.CharField(blank=True, max_length=255, null=True)),
                ('completed_date', models.CharField(blank=True, max_length=255, null=True)),
                ('task_starttime', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'tbl_subtask',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblSummarizedBalance',
            fields=[
                ('client', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('client_name', models.CharField(blank=True, max_length=100, null=True)),
                ('invoice_amount', models.CharField(blank=True, max_length=250, null=True)),
                ('balance_due', models.CharField(blank=True, max_length=250, null=True)),
                ('amount_received', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TblTaxyear',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('taxyear', models.CharField(blank=True, max_length=100, null=True)),
                ('startdate', models.DateField(blank=True, null=True)),
                ('enddate', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tbl_taxyear',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblTransactionOverview',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.CharField(blank=True, max_length=100, null=True)),
                ('time', models.CharField(blank=True, max_length=100, null=True)),
                ('Task', models.CharField(blank=True, max_length=100, null=True)),
                ('Invoice', models.CharField(blank=True, max_length=100, null=True)),
                ('ClientName', models.CharField(blank=True, max_length=100, null=True)),
                ('Credit', models.CharField(blank=True, max_length=100, null=True)),
                ('Debit', models.CharField(blank=True, max_length=100, null=True)),
                ('ClientBalance', models.CharField(blank=True, max_length=250, null=True)),
                ('InvoiceAmount', models.CharField(blank=True, max_length=250, null=True)),
                ('InvoiceBalance', models.CharField(blank=True, max_length=250, null=True)),
                ('transactiontype', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TblTransactTable',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.CharField(blank=True, max_length=100, null=True)),
                ('time', models.CharField(blank=True, max_length=100, null=True)),
                ('task', models.CharField(blank=True, db_column='Task', max_length=100, null=True)),
                ('amount', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('invoiceid', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, db_column='DESCRIPTION', max_length=255, null=True)),
                ('transactiontype', models.CharField(blank=True, max_length=250, null=True)),
                ('clientbalance', models.CharField(blank=True, max_length=250, null=True)),
                ('invoicebalance', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TblWorkTimeTable',
            fields=[
                ('subtaskId', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.CharField(blank=True, max_length=100, null=True)),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('clientName', models.CharField(blank=True, db_column='company_name', max_length=100, null=True)),
                ('maintaskname', models.CharField(blank=True, db_column='task', max_length=100, null=True)),
                ('subtaskname', models.CharField(blank=True, db_column='subtask', max_length=100, null=True)),
                ('start_time', models.CharField(blank=True, max_length=100, null=True)),
                ('endtime', models.CharField(blank=True, max_length=100, null=True)),
                ('time', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Userdetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('fristname', models.CharField(blank=True, max_length=255, null=True)),
                ('lastname', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('postalcode', models.CharField(blank=True, max_length=255, null=True)),
                ('aboutme', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'userdetail',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('mailid', models.CharField(max_length=255, unique=True)),
                ('isadmin', models.CharField(blank=True, db_column='IsAdmin', max_length=255, null=True)),
                ('isapproved', models.CharField(blank=True, db_column='IsApproved', max_length=255, null=True)),
                ('default_rate', models.CharField(blank=True, db_column='Default_Rate', max_length=255, null=True)),
                ('superuser', models.CharField(blank=True, db_column='Superuser', max_length=255, null=True)),
                ('userprofile', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblTransaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('taskid', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.CharField(blank=True, max_length=100, null=True)),
                ('time', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.CharField(blank=True, max_length=100, null=True)),
                ('invoiceid', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, db_column='DESCRIPTION', max_length=255, null=True)),
                ('transactiontype', models.CharField(blank=True, max_length=250, null=True)),
                ('clientbalance', models.CharField(blank=True, max_length=250, null=True)),
                ('invoicebalance', models.CharField(blank=True, max_length=250, null=True)),
                ('clientid', models.ForeignKey(db_column='clientid', on_delete=django.db.models.deletion.DO_NOTHING, to='TeamTask.tblclient')),
                ('userid', models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.DO_NOTHING, to='TeamTask.users')),
            ],
            options={
                'db_table': 'tbl_transaction',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblTasklist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.CharField(blank=True, db_column='Date', max_length=100, null=True)),
                ('task', models.CharField(blank=True, db_column='Task', max_length=100, null=True)),
                ('assignto', models.CharField(blank=True, db_column='AssignTo', max_length=100, null=True)),
                ('priority', models.CharField(blank=True, db_column='Priority', max_length=100, null=True)),
                ('startdate', models.CharField(blank=True, db_column='Startdate', max_length=100, null=True)),
                ('enddate', models.CharField(blank=True, db_column='Enddate', max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('time', models.CharField(blank=True, max_length=255, null=True)),
                ('isdeleted', models.CharField(blank=True, max_length=255, null=True)),
                ('plantype', models.CharField(blank=True, max_length=255, null=True)),
                ('subclient', models.CharField(blank=True, db_column='Subclient', max_length=255, null=True)),
                ('task_starttime', models.CharField(blank=True, max_length=255, null=True)),
                ('clientname', models.CharField(blank=True, max_length=255, null=True)),
                ('file_path', models.CharField(blank=True, max_length=255, null=True)),
                ('completed_date', models.CharField(blank=True, max_length=255, null=True)),
                ('invoiceid', models.CharField(blank=True, max_length=255, null=True)),
                ('advanceamount', models.CharField(blank=True, max_length=255, null=True)),
                ('phonenumber', models.CharField(blank=True, max_length=255, null=True)),
                ('drawingtitle', models.CharField(blank=True, db_column='Drawingtitle', max_length=255, null=True)),
                ('parenttaskid', models.CharField(blank=True, max_length=255, null=True)),
                ('parenttaskbalance', models.IntegerField(default=0)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client_id', to='TeamTask.tblclient')),
            ],
            options={
                'db_table': 'tbl_tasklist',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblTaskinvoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.CharField(blank=True, max_length=100, null=True)),
                ('unit', models.CharField(blank=True, max_length=100, null=True)),
                ('rate', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.CharField(blank=True, max_length=255, null=True)),
                ('tasklistrowid', models.ForeignKey(db_column='tasklistrowid', on_delete=django.db.models.deletion.DO_NOTHING, to='TeamTask.tbltasklist')),
            ],
            options={
                'db_table': 'tbl_taskinvoice',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblSubtasktime',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('comments', models.CharField(blank=True, max_length=255, null=True)),
                ('time', models.CharField(blank=True, max_length=255, null=True)),
                ('endtime', models.CharField(blank=True, max_length=255, null=True)),
                ('start_time', models.CharField(blank=True, max_length=255, null=True)),
                ('subtask', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subtaskTime', to='TeamTask.tblsubtask')),
            ],
            options={
                'db_table': 'tbl_subtasktime',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='tblsubtask',
            name='tasklist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subtask', to='TeamTask.tbltasklist'),
        ),
        migrations.CreateModel(
            name='TblSubclient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='name', max_length=100, null=True)),
                ('phoneno', models.CharField(blank=True, db_column='PhoneNo', max_length=100, null=True)),
                ('clients', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='clients', to='TeamTask.tblclient')),
            ],
            options={
                'db_table': 'tbl_subclient',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblStockinvoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('types', models.CharField(blank=True, max_length=100, null=True)),
                ('unit', models.CharField(blank=True, max_length=100, null=True)),
                ('rate', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('tasklistrow', models.ForeignKey(db_column='tasklistrow', on_delete=django.db.models.deletion.DO_NOTHING, to='TeamTask.tbltasklist')),
            ],
            options={
                'db_table': 'tbl_stockinvoice',
                'managed': True,
            },
        ),
    ]
