from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required  # Make sure this is imported
from .models import Task  # Import your Task model

# List all tasks for the logged-in user
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')  # Show only user's tasks
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# View details of a specific task
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Ensure user owns the task
    return render(request, 'tasks/task_detail.html', {'task': task})

# Create a new task
@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        category = request.POST.get('category', 'General')
        priority = request.POST.get('priority', 'Medium')
        deadline = request.POST.get('deadline')

        # Create and save the new task
        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category,
            priority=priority,
            deadline=deadline,
        )
        return redirect('task_list')  # Redirect to task list after creation

    return render(request, 'tasks/task_form.html')  # Show task creation form

# Update an existing task
@login_required
def task_form(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Ensure user owns the task

    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.category = request.POST.get('category', task.category)
        task.priority = request.POST.get('priority', task.priority)
        task.deadline = request.POST.get('deadline', task.deadline)
        task.completed = request.POST.get('completed') == 'on'  # Handle checkbox for completed
        task.save()
        return redirect('task_list')

    return render(request, 'tasks/task_form.html', {'task': task})

# Delete a task
@login_required
def task_confirm_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Ensure user owns the task

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


