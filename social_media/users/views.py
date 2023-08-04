import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = CustomUserCreationForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'User registered successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})