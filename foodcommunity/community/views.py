from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .forms import CommunityForm
from rest_framework.views import APIView


class CommunityList(APIView):
    def get(self, request):
        communities = Community.objects.all()
        if not communities:
            return Response({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data)

    def post(self, request):
        form = CommunityForm(request.data)

        if form.is_valid():
            # Extract validated data from the form
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            topic = form.cleaned_data['topic']

            # Perform additional validation checks
            if len(title) < 3:
                return Response({'error': 'Name must be at least 3 characters long.'},
                                status=status.HTTP_400_BAD_REQUEST)

            if len(description) < 10:
                return Response({'error': 'Description must be at least 10 characters long.'},
                                status=status.HTTP_400_BAD_REQUEST)

            if Community.objects.filter(topic=topic).exists():
                return Response({'error': 'Community with this topic already exists.'},
                                status=status.HTTP_400_BAD_REQUEST)

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
        try:
            community = Community.objects.get(id=pk)
        except Community.DoesNotExist:
            return Response({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Only update the specified fields (title and description)
        data = {
            'title': request.data.get('title', community.title),
            'description': request.data.get('description', community.description)
        }

        serializer = CommunitySerializer(community, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            community = Community.objects.get(id=pk)
        except Community.DoesNotExist:
            return Response({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user making the request is a member of the community
        if request.user not in community.users.all():
            return Response({'error': 'You are not a member of this community.'}, status=status.HTTP_403_FORBIDDEN)

        # Check if the user making the request is the admin of the community
        is_admin = community.admin == request.user

        # If the user is the admin, transfer admin role to another member
        if is_admin:
            # Find another member to become the admin of the community
            # Again, this could be a complex logic, but for simplicity, we'll just pick the first member available
            new_admin = community.members.exclude(id=request.user.id).first()

            # Transfer admin role to the new admin
            community.admin = new_admin
            community.save()

        # Remove the user from the community
        community.members.remove(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageList(APIView):
    def get(self, request, room_id):
        messages = communitiesChat.objects.filter(room_id=room_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, room_id):
        request.data['room'] = room_id
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JoinCommunity(APIView):
    def post(self, request, community_id):
        try:
            community = Community.objects.get(pk=community_id)
        except Community.DoesNotExist:
            return Response({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if user in community.users.all():
            return Response({'message': 'You are already a member of this community.'}, status=status.HTTP_200_OK)

        community.users.add(user)
        return Response({'message': 'Joined the community successfully.'}, status=status.HTTP_200_OK)


class SearchCommunity(APIView):
    def get(self, request):
        query = request.GET.get('q', '')

        if query:
            communities = Community.objects.filter(title__icontains=query)
            serializer = CommunitySerializer(communities, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'Please provide a search query.'}, status=status.HTTP_400_BAD_REQUEST)


class CommunityMembers(APIView):
    def get(self, request, community_id):
        try:
            community = Community.objects.get(pk=community_id)
        except Community.DoesNotExist:
            return Response({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)

        members = community.users.all()
        member_ids = [member.id for member in members]
        return Response(member_ids, status=status.HTTP_200_OK)


class LeaveCommunity(APIView):
    def post(self, request, community_id):
        try:
            community = Community.objects.get(pk=community_id)
        except Community.DoesNotExist:
            return Response({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if user not in community.users.all():
            return Response({'message': 'You are not a member of this community.'}, status=status.HTTP_200_OK)

        community.users.remove(user)
        return Response({'message': 'You have left the community successfully.'}, status=status.HTTP_200_OK)

class CommunityChat(APIView):
    def get(self, request, community_id):
        try:
            community = Community.objects.get(pk=community_id)
        except Community.DoesNotExist:
            return Response({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve all chat messages related to the community
        chats = communitiesChat.objects.filter(topic=community)

        chat_data = [
            {
                'topic': chat.topic.title,
                'sender': chat.sender.username,
                'message': chat.message,
                'timestamp': chat.timestamp
            }
            for chat in chats
        ]

        return Response(chat_data, status=status.HTTP_200_OK)


class StartChatWithCommunity(APIView):
    def post(self, request, community_id):
        try:
            community = Community.objects.get(pk=community_id)
        except Community.DoesNotExist:
            return Response({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)

        sender = request.user
        message = request.data.get('message', '')

        chat = communitiesChat.objects.create(topic=community, sender=sender, message=message)
        serializer = communitieschatSerializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserCommunityList(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        communities = Community.objects.filter(user=user)
        serializer = CommunityListSerializer(communities, many=True)
        return Response(serializer.data)