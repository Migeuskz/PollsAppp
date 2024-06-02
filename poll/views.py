import json
from django.shortcuts import get_object_or_404, redirect, render
from .models import Question, Choice

# Create your views here.
def home(request):
    questions =  Question.objects.all()
    return render(request, 
                  'poll/home.html',
                  {
                      "questions": questions
                  }
                  )

def vote(request, q_id):
    q = get_object_or_404(Question, pk=q_id)
    # q = Question.objects.get(pk=q_id)
    if request.method == 'POST':
        try:
            choice_id = request.POST.get('choice')
            choice = q.choice_set.get(pk=choice_id)
            choice.votes += 1
            choice.save()
            return redirect('poll:result', q_id)
        except(KeyError, Choice.DoesNotExist):
            return render(request, 'poll/vote.html', {
                "question": q,
                "error_message": "Debes elegir algo :0"
            })  
    return render(request, 'poll/vote.html',
                  {
                      "question": q
                  })

def result(request, q_id):
    q = get_object_or_404(Question, pk=q_id)
    
    try:
        q = Question.objects.get(pk=q_id)
    except Question.DoesNotExist:
        return redirect('poll:home')
    
    labels = []
    data = []
    
    
    for item in q.choice_set.all():
        labels.append(item.choice_text)
        data.append(item.votes)
    
    info ={
        'labels': labels,
        'data': data,
    }
        
    
    return render(request, 'poll/result.html', {
        "question": q,
        
        "info": json.dumps(info)
    })
    
    
    