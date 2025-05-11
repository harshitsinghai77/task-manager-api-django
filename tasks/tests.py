from datetime import datetime, timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tasks.models import Task
from tasks.serializers import TaskSerializer

class TaskAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'due_date': (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        }
        self.task = Task.objects.create(
            title='Existing Task',
            description='Existing Description',
            due_date=(datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d'),
            status='pending'
        )

    def test_create_task_success(self):
        """Test successful task creation"""
        with patch('config.celery_app.send_task') as mock_send_task:
            response = self.client.post(
                reverse('task-list'),
                self.valid_task_data,
                format='json'
            )
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Task.objects.count(), 2)
            self.assertEqual(response.data['title'], self.valid_task_data['title'])
            self.assertEqual(response.data['status'], 'pending')
            mock_send_task.assert_called_once_with(
                'tasks.process_task',
                args=[response.data['task_id']],
                queue='default'
            )

    def test_create_task_invalid_date(self):
        """Test task creation with past due date"""
        invalid_data = self.valid_task_data.copy()
        invalid_data['due_date'] = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        response = self.client.post(
            reverse('task-list'),
            invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('due_date', response.data)

    def test_list_tasks(self):
        """Test retrieving list of tasks"""
        response = self.client.get(reverse('task-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Existing Task')

    def test_list_tasks_empty(self):
        """Test retrieving empty list of tasks"""
        Task.objects.all().delete()
        response = self.client.get(reverse('task-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_retrieve_task(self):
        """Test retrieving a single task"""
        response = self.client.get(
            reverse('task-detail', kwargs={'pk': self.task.task_id})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Existing Task')

    def test_retrieve_nonexistent_task(self):
        """Test retrieving a non-existent task"""
        response = self.client.get(
            reverse('task-detail', kwargs={'pk': 999})
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task_status(self):
        """Test updating task status"""
        response = self.client.patch(
            reverse('task-detail', kwargs={'pk': self.task.task_id}),
            {'status': 'in_progress'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'in_progress')

    def test_update_task_invalid_status(self):
        """Test updating task with invalid status"""
        response = self.client.patch(
            reverse('task-detail', kwargs={'pk': self.task.task_id}),
            {'status': 'invalid_status'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)
        self.assertIn('Invalid status', str(response.data['status'][0]))

    def test_create_task_with_status(self):
        """Test task creation with non-pending status is overridden"""
        data = self.valid_task_data.copy()
        data['status'] = 'completed'
        
        response = self.client.post(
            reverse('task-list'),
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'pending')

    def test_update_multiple_fields(self):
        """Test updating multiple fields is not allowed"""
        response = self.client.patch(
            reverse('task-detail', kwargs={'pk': self.task.task_id}),
            {'status': 'completed', 'title': 'New Title'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Only status can be updated', str(response.data[0]))

    def test_create_task_with_invalid_due_date_format(self):
        """Test task creation with invalid due date format"""
        invalid_data = self.valid_task_data.copy()
        invalid_data['due_date'] = 'invalid-date'
        
        response = self.client.post(
            reverse('task-list'),
            invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('due_date', response.data)

    def test_update_task_other_fields(self):
        """Test updating fields other than status"""
        response = self.client.patch(
            reverse('task-detail', kwargs={'pk': self.task.task_id}),
            {'title': 'Updated Title'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_task(self):
        """Test deleting a task"""
        response = self.client.delete(
            reverse('task-detail', kwargs={'pk': self.task.task_id})
        )
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
