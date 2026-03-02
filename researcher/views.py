from django.shortcuts import render
from django.http import StreamingHttpResponse
from main import run_agent
import json
import sys
import os
import threading
import time


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_state import AgentState

def home(request):
    return render(request, 'researcher/home.html')

def run_research(request):
    query = request.GET.get('query', '')
    
    def stream():
        messages = []

        def send(message, status='default'):
            messages.append(json.dumps({'type': 'progress', 'message': message, 'status': status}))


        result = {}

        def run():
            result['state'] = run_agent(query, send=send)

        thread = threading.Thread(target=run)
        thread.start()

        while thread.is_alive():
            while messages:
                yield f"data: {messages.pop(0)}\n\n"
            time.sleep(0.1)

        while messages:
            yield f"data: {messages.pop(0)}\n\n"

        state = result['state']
        yield f"data: {json.dumps({'type': 'done', 'report': state['final_report'], 'source': state['search_source']})}\n\n"
    
    return StreamingHttpResponse(stream(), content_type='text/event-stream')




