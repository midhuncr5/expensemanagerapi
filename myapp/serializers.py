from rest_framework import serializers
from myapp.models import User
from myapp.models import Category,Transactions
from django.db.models import Sum


class UserSerializer(serializers.ModelSerializer):
    phone=serializers.CharField()
    class Meta:
        model=User
        fields=["id","username","email","password","phone",]

    def create(self, validated_data):

        password1=validated_data.pop("password")

        return User.objects.create_user(**validated_data,password=password1)
    
class CategorySerializer(serializers.ModelSerializer):

    owner=serializers.StringRelatedField(read_only=True)

    class Meta:
        model=Category

        fields="__all__"

        read_only_fields=["id","owner"]

     

import json   

class TransactionSerializer(serializers.ModelSerializer):
    
    owner=serializers.StringRelatedField(read_only=True)
    
    
    
    class Meta:

        model=Transactions

        fields="__all__"

        read_only_fields=["id","owner"]

    
  
   



    


 



    



    




        

    

        