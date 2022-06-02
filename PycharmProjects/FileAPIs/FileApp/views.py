from django.shortcuts import render
from rest_framework import generics, status, filters, serializers, permissions
import io, csv, pandas as pd
from rest_framework.response import Response
from rest_framework import pagination
from .models import File
from FileApp import filter
from .serializers import FileUploadSerializer, SaveFileSerializer, UserSerializer, RegisterSerializer
from knox.models import AuthToken


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


def index(request):
    return render(request, 'index.html')


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'


class UploadFileView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        reader = pd.read_csv(file)
        for _, row in reader.iterrows():
            new_file = File(
                id=row["id"],
                staff_name=row["Staff_Name"],
                position=row["Designated_Position"],
                age=row["Age"],
                year_joined=row["Year_Joined"]
            )
            new_file.save()
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class FileDataAPIView(generics.ListAPIView):
    search_fields = ['age', 'staff_name', 'position', 'year_joined']
    filter_backends = [filters.SearchFilter]
    # filter_fields = (
    #     'staff_name',
    #     'age',
    #     'year_joined',
    # )
    queryset = File.objects.all()
    serializer_class = SaveFileSerializer
    pagination_class = StandardResultsSetPagination


def FileViewData(request):
    f = filter.FileDataFilter(request.GET, queryset=File.objects.all())
    return render(request, 'filedata.html', {'filter': f})
