

class TaskTypeDefinitionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'tasks/personal' in request.path:
            request.tasks_type = 'personal'
        elif 'tasks/work' in request.path:
            request.tasks_type = 'work'
        response = self.get_response(request)
        return response
