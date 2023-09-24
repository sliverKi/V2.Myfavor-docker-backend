from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase
from boards.models import Board  
from boards.serializers import BoardSerializer  


class BoardTypeTestCase(APITestCase):

    def setUp(self):
        # Test setup 코드. 예를 들어, Board 객체 생성.
        self.board1 = Board.objects.create(type="event")
        self.board2 = Board.objects.create(type="release")
        self.url = '/api/v2/board/'  

    def test_get_board_type(self):
        response = self.client.get(self.url)
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)



