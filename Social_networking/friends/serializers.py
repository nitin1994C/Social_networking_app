from rest_framework import serializers
from account.models import Friendship, User
from account.serializers import UserSerializer


class FriendshipSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'sender', 'receiver', 'status']

    def create(self, validated_data):
        sender_data = validated_data.pop('sender')
        receiver_data = validated_data.pop('receiver')

        sender = User.objects.get(pk=sender_data['id'])
        receiver = User.objects.get(pk=receiver_data['id'])

        friendship = Friendship.objects.create(sender=sender, receiver=receiver, **validated_data)
        return friendship

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
