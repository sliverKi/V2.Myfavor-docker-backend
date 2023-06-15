from rest_framework import serializers
from users.models import User

        
class FindPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Check that the email belongs to an existing user
        """
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('No user with this email.')
        return value