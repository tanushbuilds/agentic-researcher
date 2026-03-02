from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.shortcuts import redirect
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



def memory(request):
    memory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'memory.json')
    if os.path.exists(memory_path):
        with open(memory_path, 'r') as f:
            memory_data = json.load(f)
    else:
        memory_data = {}
    return render(request, 'researcher/memory.html', {'memory': memory_data})


def delete_memory(request, key):
    memory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'memory.json')
    if os.path.exists(memory_path):
        with open(memory_path, 'r') as f:
            memory_data = json.load(f)
        if key in memory_data:
            del memory_data[key]
        with open(memory_path, 'w') as f:
            json.dump(memory_data, f, indent=4)
    return redirect('memory')


def clear_memory(request):
    memory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'memory.json')
    with open(memory_path, 'w') as f:
        json.dump({}, f)
    return redirect('memory')



