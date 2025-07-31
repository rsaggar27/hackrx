from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .langgraph_runner import run_graph
import json
import tempfile
import requests
import os

@csrf_exempt
def run_hackrx(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    try:
        body = json.loads(request.body)
        doc_url = body.get("documents")
        questions = body.get("questions")

        if not doc_url or not questions:
            return JsonResponse({"error": "Missing 'documents' URL or 'questions' list"}, status=400)

        # Download the file temporarily
        response = requests.get(doc_url)
        if response.status_code != 200:
            return JsonResponse({"error": "Unable to download document"}, status=400)

        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(response.content)
        temp_file.flush()
        temp_file_name = temp_file.name
        temp_file.close()

        # Run graph
        answers = run_graph(temp_file_name, questions)

        # Clean up the file
        os.unlink(temp_file_name)

        return JsonResponse({"answers": answers})

    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)
