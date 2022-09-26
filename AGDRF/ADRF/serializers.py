from rest_framework import serializers
from ADRF.models import person,dept
from django.contrib.auth.models import User

class loginserializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()
    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('Username already exists')
        
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('Email already exists')
        
        return data

    def create(self,validated_data):
        user=User.objects.create(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

class deptserializer(serializers.ModelSerializer):
    class Meta:
        model=dept
        fields='__all__'

class personserializer(serializers.ModelSerializer):
    #department=deptserializer(read_only=True)
    #accounts=serializers.SerializerMethodField()
    class Meta:
        model=person
        fields='__all__'
        #depth=1
    
    def get_accounts(self,obj):
        acc_obj=dept.objects.get(id=obj.department.id)
        return {'Dept_name':acc_obj.dept_name,'decuctions':2500}
    
    def validate_age(self, age):
        if age<18:
            raise serializers.ValidationError('Age cannot be less than 18')
        return age

    def validate_name(self,name):
        spec_char='!@#$%^&*?'
        if any(i in spec_char for i in name):
            raise serializers.ValidationError('cannot contain special characters')
        return name
    