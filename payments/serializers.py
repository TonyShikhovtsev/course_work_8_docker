from rest_framework import serializers

from payments.models import Payment



class PaymentSerializer(serializers.ModelSerializer):
    """ Payment serializer """


    class Meta:
        model = Payment
        fields = "__all__"