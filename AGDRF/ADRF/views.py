from rest_framework.decorators import api_view
from rest_framework.response import Response
from ADRF.models import person
from ADRF.serializers import loginserializer, personserializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator
# Create your views here.

class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self,request):
        try:
            print(request.user)
            obj=person.objects.filter(department__isnull=False)
            page=request.GET.get('page',1)
            page_size=3
            paginator=Paginator(obj,page_size)
            serializer=personserializer(paginator.page(page),many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "status":False,
                "message":"invalid page no"

            })
    def post(self,request):
        data=request.data
        serializer=personserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self,request):
        data=request.data
        obj=person.objects.get(id=data['id'])
        serializer=personserializer(obj,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def patch(self,request):
        data=request.data
        obj=person.objects.get(id=data['id'])
        serializer=personserializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self,request):
        data=request.data
        obj=person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message':'employee deleted'})

class LoginAPI(APIView):
    def post(self,request):
        data=request.data
        serializer=loginserializer(data=data)
        if not serializer.is_valid():
            return Response({"status": False,
            "message":'login failed'},
            status.HTTP_201_CREATED)
        user=authenticate(username=serializer.data['username'],password=serializer.data['password'])
        if not user:
            return Response({"status": False,
            "message":'login failed'},
            status.HTTP_201_CREATED)
        token,_=Token.objects.get_or_create(user=user)
        return Response({"status":True,"message":"login success","token":str(token)},status.HTTP_201_CREATED)

class RegisterAPI(APIView):
    def post(self,request):
        data=request.data
        serializer=RegisterSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "status":False,
                "message":serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response({'status':True,"message":"user_created"},status=status.HTTP_201_CREATED)


@api_view(['GET','POST','PUT','PATCH','DELETE'])
def employee(request):
    if request.method=='GET':
        obj=person.objects.filter(department__isnull=False)
        serializer=personserializer(obj,many=True)
        return Response(serializer.data)
        
    elif request.method=='POST':
        data=request.data
        serializer=personserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method=='PUT':
        data=request.data
        obj=person.objects.get(id=data['id'])
        serializer=personserializer(obj,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method=='PATCH':
        data=request.data
        obj=person.objects.get(id=data['id'])
        serializer=personserializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method=='DELETE':
        data=request.data
        obj=person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message':'employee deleted'})
    

@api_view(['POST'])
def login(request):

    data=request.data
    serializer=loginserializer(data=data)
    if serializer.is_valid():
        data=serializer.validated_data
        print(data)
        return Response({'message':'success'})
    return Response(serializer.errors)


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class=personserializer
    queryset=person.objects.all()

    def list(self,request):
        search=request.GET.get('search')
        queryset=self.queryset
        if search:
            queryset=queryset.filter(name__startswith=search)
        serializer=personserializer(queryset,many=True)
        return Response({"status":200,"data":serializer.data},status=status.HTTP_200_OK)
