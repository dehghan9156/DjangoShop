from rest_framework import serializers
from ...models import Product,Category
from rest_framework.reverse import reverse_lazy

class ProductObjectsSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),slug_field='name')
    class Meta:
        model = Product
        fields = ["id","name","category","description","price","discount","stock","image","absolute_url"]

    def get_absolute_url(self,obj):
        url = reverse_lazy("product:api-v1:product-detail-api",kwargs={'pk':obj.id})
        request = self.context.get('request')
        return request.build_absolute_uri(url)