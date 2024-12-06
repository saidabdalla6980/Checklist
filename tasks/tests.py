from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task

class TaskViewTests(TestCase):

    def setUp(self):
        # Set up a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create some tasks for the test user
        self.task1 = Task.objects.create(
            user=self.user,
            title='Test Task 1',
            description='Test Task 1 Description'
        )
        self.task2 = Task.objects.create(
            user=self.user,
            title='Test Task 2',
            description='Test Task 2 Description'
        )

    def test_task_list_view(self):
        """Test that the task list view returns a status code of 200 and uses the correct template."""
        self.client.login(username='testuser', password='12345')  # Log in the test user
        response = self.client.get(reverse('task_list'))  # Access the task list view

        self.assertEqual(response.status_code, 200)  # Check for HTTP 200 status
        self.assertTemplateUsed(response, 'MyToDoList/task_list.html')  # Check the correct template is used
        self.assertContains(response, 'Test Task 1')  # Check that the task title is displayed
        self.assertContains(response, 'Test Task 2')  # Check that another task title is displayed

    def test_task_detail_view(self):
        """Test that the task detail view shows the correct task details."""
        self.client.login(username='testuser', password='12345')  # Log in the test user
        response = self.client.get(reverse('task_detail', kwargs={'task_id': self.task1.id}))  # Access the task detail view

        self.assertEqual(response.status_code, 200)  # Check for HTTP 200 status
        self.assertTemplateUsed(response, 'MyToDoList/task_detail.html')  # Check the correct template is used
        self.assertContains(response, 'Test Task 1')  # Check that the task title is displayed
        self.assertContains(response, 'Test Task 1 Description')  # Check that the task description is displayed

    def test_task_create_view(self):
        """Test that the task create view works correctly."""
        self.client.login(username='testuser', password='12345')  # Log in the test user
        data = {
            'title': 'New Test Task',
            'description': 'New Task Description',
        }
        response = self.client.post(reverse('task_create'), data)  # Post data to create a new task

        # Check that the task was created and redirected to the task list page
        self.assertEqual(response.status_code, 302)  # Expect a redirect after form submission
        self.assertRedirects(response, reverse('task_list'))  # Ensure it redirects to the task list page
        self.assertEqual(Task.objects.count(), 3)  # Check that a new task was created

    def test_task_update_view(self):
        """Test that the task update view works correctly."""
        self.client.login(username='testuser', password='12345')  # Log in the test user
        data = {
            'title': 'Updated Test Task',
            'description': 'Updated Task Description',
        }
        response = self.client.post(reverse('task_update', kwargs={'task_id': self.task1.id}), data)  # Update the task

        # Check that the task was updated and redirected to the task detail page
        self.assertEqual(response.status_code, 302)  # Expect a redirect after update
        self.assertRedirects(response, reverse('task_detail', kwargs={'task_id': self.task1.id}))  # Redirects to the updated task
        self.task1.refresh_from_db()  # Reload the task from the database
        self.assertEqual(self.task1.title, 'Updated Test Task')  # Check that the title was updated
        self.assertEqual(self.task1.description, 'Updated Task Description')  # Check that the description was updated

    def test_task_delete_view(self):
        """Test that the task delete view works correctly."""
        self.client.login(username='testuser', password='12345')  # Log in the test user
        response = self.client.post(reverse('task_delete', kwargs={'task_id': self.task1.id}))  # Send delete request

        # Check that the task was deleted and redirected to the task list page
        self.assertEqual(response.status_code, 302)  # Expect a redirect after deletion
        self.assertRedirects(response, reverse('task_list'))  # Redirect to the task list page
        self.assertEqual(Task.objects.count(), 1)  # Check that only 1 task remains
