from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuestionForm, CommentForm
from .models import Question, Comment
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    questions = Question.objects.all()
    context = {
        'questions': questions,
    }
    return render(request, 'gallery/index.html', context)

@login_required
def create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('gallery:index')
    else:
        form = QuestionForm()
    return render(request, 'gallery/form.html', {'form': form})

@login_required
def update(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == "POST":
        if question.user == request.user:
            form = QuestionForm(request.POST, instance=question)
            if form.is_valid():
                form = form.save()
                return redirect('gallery:detail', id)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'gallery/form.html', {'form': form})

@login_required
def delete(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == "POST":
        if question.user == request.user:
            question.delete()
        return redirect('gallery:index')

def detail(request, id):
    question = get_object_or_404(Question, id=id)
    form = CommentForm()
    comments = Comment.objects.filter(question=question).order_by('-id')
    cnt_a = question.comment_set.filter(pick="1").count()
    cnt_b = question.comment_set.filter(pick="2").count()
    if question.comment_set.all():
        cnt_all = cnt_a + cnt_b
        ratio_a = cnt_a / cnt_all * 100
        ratio_b = cnt_b / cnt_all * 100

        cnt = {
            'ratio_a': ratio_a,
            'ratio_b': ratio_b,
            'cnt_a': cnt_a,
            'cnt_b': cnt_b,
        }
    else:
        cnt = {
            'ratio_a': '0.0',
            'ratio_b': '0.0',
            'cnt_a': cnt_a,
            'cnt_b': cnt_b,
        }

    context = {
        'question': question,
        'form': form,
        'cnt': cnt,
        'comments': comments,
    }
    return render(request, 'gallery/detail.html', context)

@login_required
def create_comment(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == "POST":
        comment = CommentForm(request.POST)
        if comment.is_valid():
            comment = comment.save(commit=False)
            comment.question = question
            comment.user = request.user
            comment.save()
        return redirect('gallery:detail', id)

@login_required
def delete_comment(request, question_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        if comment.user == request.user:
            comment.delete()
        return redirect('gallery:detail', question_id)

@login_required
def update_comment(request, question_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('gallery:detail', question_id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'gallery/form.html', {'form': form})