from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from myapp.serializers import UserSerializer,CategorySerializer,TransactionSerializer
from rest_framework import authentication,permissions
from myapp.models import Category,Transactions
from django.db.models import Sum
from django.core.mail import send_mail
from myapp.models import User


class UserCreationView(generics.CreateAPIView):
    serializer_class=UserSerializer
    

class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class=CategorySerializer
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        
        return serializer.save(owner=self.request.user)
    
    queryset=Category.objects.all()

class CategoryRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]


class TransactionListCreateView(generics.ListCreateAPIView):

    serializer_class=TransactionSerializer

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    queryset=Transactions.objects.all()

   
    
    


    def perform_create(self, serializer):




        return serializer.save(owner=self.request.user)

    

class TransactionRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=TransactionSerializer
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    queryset=Transactions.objects.all()

    def perform_update(self, serializer):

        amount=serializer.validated_data.get("amount")

        title=serializer.validated_data.get("title")

        print(amount,"============================")

        transaction_obj=Transactions.objects.get(title=title)


        category_obj=transaction_obj.category_object

        cat=Category.objects.get(name=category_obj,owner=self.request.user)
        
        user_obj=User.objects.get(username=self.request.user)

        print(user_obj.email)
        
    
        if amount>=cat.budget:
            subject="monthly transactions"
            message=f"your reached budget{cat.budget} in {category_obj} category this month"
            from_= "midhuncr125@gmail.com"

            send_mail(
                      subject=subject,
                      message=message,
                      from_email=from_,
                      recipient_list=["midhuncr2020@gmail.com"],
                       fail_silently=False,
                        )
            

        

        return serializer.save()
    


class ExpensesummaryView(APIView):

    def get(self,request,*args,**kwargs):

        qs=Transactions.objects.filter(owner=request.user)

        print(qs,"==============================")
        
        category_obj=qs.values_list("category_object__name").annotate(total=Sum("amount"))

      
        payment_summary=qs.values("payment_method").annotate(total=Sum("amount"))
        
        total_transaction=qs.values("amount").aggregate(total=Sum("amount"))

        print(total_transaction)
        

        data={
            "total expense":total_transaction,
            "category total":category_obj,
            "payment method summary":payment_summary,
            
        }

       
        return Response(data=data)

        



        


        



