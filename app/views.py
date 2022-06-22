from django.shortcuts import render
from django.contrib.auth.models import auth
from django.contrib import messages
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import *

# Create your views here.
tokens=[]
def home(request):
    return render(request,'Registration.html')

def explore(request):
    return render(request,'explore.html')

def postUser(request):
    if request.method == 'POST':
        user_id=request.POST['user_id']
    return render(request, 'createPost.html',{'user_id':user_id})

def Login(request):
    return render(request, 'Login.html')

def MyPosts(request):
    if request.method == 'POST':
        flag=True
        try:
            title=request.POST['title']
            posts = Post.objects.filter(Title=title)
            flag=False
        except:
            user_id=request.POST['user_id']
            posts = Post.objects.filter(user=user_id)
        serializers2 = PostSerializer(posts, many=True)

        if len(serializers2.data)==0:
            data=""
            if flag:
                data = "You"
            else:
                data = title
            return render(request, 'Empty.html', {'name': data})

        serializers2.data.__reversed__()
        return render(request,'MyPosts.html',{'posts':serializers2.data})

def loginFunc(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=User.objects.get(username=username)
        user_serializer = UserSerializer(user)
        if user_serializer!=None and user_serializer.data['password']==password:

            posts=Post.objects.exclude(user__isnull=True)
            serializers2 = PostSerializer(posts, many=True)
            serializers2=list(serializers2.data)

            for i in range(0,len(serializers2)):
                temp = User.objects.get(id=serializers2[i]["user"])
                serializer_temp = UserSerializer(temp)
                temp_username = serializer_temp["name"]
                serializers2[i]["username"]=temp_username.value

            user_id=user_serializer.data['id']
            serializers2.reverse()
            return render(request,'explore.html',{'posts':serializers2,'user_id':user_id,'username':user_serializer.data['username']})
        else:
            messages.info(request,'invalid credentials')
            return render(request, 'Login.html')

        return HttpResponse("fine")

class RegisterUser(APIView):
    def get(self,request):
        try:
            id=request.query_params['id']

            if id!=None:
                user = User.objects.get(id=id)
                serializers = UserSerializer(user)

        except:
            users = User.objects.all()
            serializers = UserSerializer(users, many=True)

        return Response({'status': 200, 'payload': serializers.data})

    def post(self,request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'status': 200, 'message': 'Wrong Credentials!!'})
        serializer.save()

        # user = User.objects.get(username=serializer.data['username'])
        # token_obj,_=Token.objects.get_or_create(user=user)
        #
        # tokens.append(str(token_obj))

        # return Response({
        #     'status':200,
        #     'payload':serializer.data,
        #     # 'token':str(token_obj),
        #     'message':'Your credentials are saved!'}
        # )

        return render(request, 'Login.html')

    def put(self,request):
        try:
            user_obj = User.objects.get(id=request.data['id'])
            serializer = UserSerializer(user_obj, data=request.data,partial=True)

            if not serializer.is_valid():
                print(serializer.errors())
                return Response({'status': 403, 'message': 'holona aar ki kora jabe!'})

            serializer.save()
            return Response({'status': 200, 'message': 'data updated!'})
        except Exception as e:
            print("this is your exception ",e)
            return Response({'status': 403, 'message': 'invalid id'})

    def delete(self,request):
        try:
            user_obj=User.objects.get(id=request.query_params['id'])
            user_obj.delete()
            return Response({'status': 200, 'message': 'data deleted!'})
        except Exception as e:
            return Response({'status': 403, 'message': 'invalid id'})

class PostAPI(APIView):

    #Authentication is checked here
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            id=request.query_params['id']

            if id!=None:
                item = Post.objects.get(id=id)
                serializers = PostSerializer(item)

        except:
            posts = Post.objects.all()
            serializers = PostSerializer(posts, many=True)

        return Response({'status': 200, 'payload': serializers.data})

    #authen-->user-->details-->id-->
    def post(self,request): #-->titile,cate,expe,id
        data=request.data
        serializer=PostSerializer(data=request.data) #--> models(POST)-->SQL tables

        if not serializer.is_valid():
            return Response({'status': 200, 'message': 'Wrong data!!'})
        serializer.save()
        # return Response({'status':200,'payload':data,'message':'Your data is saved!'})
        return render(request,'SuccessPage.html')


# login-->myPosts-->posts-->post[3]-->update(click to update)

    def put(self,request):
        try:
            post_obj = Post.objects.get(id=request.data['id'])
            serializer = PostSerializer(post_obj, data=request.data,partial=True)

            if not serializer.is_valid():
                print(serializer.errors())
                return Response({'status': 403, 'message': 'holona aar ki kora jabe!'})

            serializer.save()
            return Response({'status': 200, 'message': 'data updated!'})
        except Exception as e:
            print("this is your exception ",e)
            return Response({'status': 403, 'message': 'invalid id'})

    def delete(self,request):
        try:
            post_obj=Post.objects.get(id=request.query_params['id'])
            post_obj.delete()
            return Response({'status': 200, 'message': 'data deleted!'})
        except Exception as e:
            return Response({'status': 403, 'message': 'invalid id'})