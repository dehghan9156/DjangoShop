from rest_framework import serializers
from ...models import HeaderFactor,Factor
from product.models import Category


class HeaderFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderFactor
        fields =["id","profile","total_price"]

class FactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factor
        fields =["id","headerfactor","product","quantity","total_price","created_date"]

