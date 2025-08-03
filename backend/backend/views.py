from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .langgraph_runner import run_graph
import json

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

        answers = run_graph(doc_url, questions)

        return JsonResponse({"answers": answers})

    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)
