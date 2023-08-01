from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .forms import CommunityForm

class CommunityList(APIView):
    def get_object(self, pk):
        try:
            return Community.objects.get(pk=pk)
        except Community.DoesNotExist:
            return None

        def get(self, request, pk):
            community = self.get_object(pk)
            if not community:
                return Response({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = CommunitySerializer(community)
            return Response(serializer.data)

    # def get(self, request,pk):
    #     communities = Community.objects.all()
    #     serializer = CommunitySerializer(communities, many=True)
    #     return Response(serializer.data)

    def post(self, request):
        form = CommunityForm(request.data)

        if form.is_valid():
            # Extract validated data from the form
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            topic = form.cleaned_data.get('topic')

            # Perform additional validation checks
            if len(title) < 3:
                return Response({'error': 'Name must be at least 3 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

            if len(description) < 10:
                return Response({'error': 'Description must be at least 10 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

            if Community.objects.filter(topic=topic).exists():
                return Response({'error': 'Community with this topic already exists.'},status=status.HTTP_400_BAD_REQUEST)

            form.save()
            return Response({'success': 'Community created successfully!'}, status=status.HTTP_201_CREATED)
        else:
            # Return form errors with better error messages
            errors = {}
            for field, error_msgs in form.errors.items():
                errors[field] = [error_msg for error_msg in error_msgs]
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class CommunityDetail(APIView):
    def get_object(self, pk):
        try:
            return Community.objects.get(pk=pk)
        except Community.DoesNotExist:
            return None

    def put(self, request, pk):
        community = Community.objects.get(id=pk)
        if not community:
            return Response({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CommunitySerializer(community, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        community = Community.objects.get(id=pk)
        if not community:
            return Response({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ChatRoomList(APIView):
    def get(self, request):
        chat_rooms = Topic.objects.all()
        serializer = TopicSerializer(chat_rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageList(APIView):
    def get(self, request, room_id):
        messages = communitieschat.objects.filter(room_id=room_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, room_id):
        request.data['room'] = room_id
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
