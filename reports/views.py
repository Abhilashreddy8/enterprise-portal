from django.shortcuts import render, redirect
from .models import Report
from .forms import ReportUploadForm
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReportSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

def dashboard(request):

    reports = Report.objects.all()
    form = ReportUploadForm()

    chart_labels = []
    chart_data = []

    if request.method == "POST":

        form = ReportUploadForm(request.POST, request.FILES)

        if form.is_valid():

            report = form.save(commit=False)
            #report.uploaded_by = request.user
            if request.user.is_authenticated:
                report.uploaded_by = request.user
            else:
                report.uploaded_by = User.objects.first()
                
            report.status = "Uploaded"
            report.save()

            #file_path = report.file.path
            file = request.FILES.get('file')

            if file:
                df = pd.read_csv(file)

                # Example analytics
                chart_labels = list(df.columns)

                #chart_data = [df[col].count() for col in df.columns]
                chart_data = [int(df[col].count()) for col in df.columns]

                print('chart_data', chart_data)

            #return redirect("dashboard")

    context = {
        "reports": reports,
        "form": form,
        "labels": chart_labels,
        "data": chart_data
    }

    return render(request, "reports/dashboard.html", context)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def report_list(request):

    if request.method == 'GET':

        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)

    if request.method == 'POST':

        serializer = ReportSerializer(data=request.data)

        if serializer.is_valid():
            #serializer.save(uploaded_by=request.user)
            serializer.save(uploaded_by=User.objects.first())
            return Response(serializer.data)

        return Response(serializer.errors)

@api_view(['GET','PUT','DELETE'])
def report_detail(request, pk):

    report = Report.objects.get(id=pk)

    if request.method == 'GET':

        serializer = ReportSerializer(report)
        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = ReportSerializer(report, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'DELETE':

        report.delete()
        return Response({"message":"Report deleted"})