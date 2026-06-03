import random
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Question, Choice

WRONG_BOOK_KEY = 'wrong_question_ids'


def index(request):
    wrong_ids = request.session.get(WRONG_BOOK_KEY, [])
    total_questions = Question.objects.count()
    return render(request, 'quiz/index.html', {
        'wrong_count': len(wrong_ids),
        'total_questions': total_questions,
    })


def start_quiz(request):
    if request.method != 'POST':
        return redirect('quiz:index')

    nickname = request.POST.get('nickname', '').strip()
    question_count = int(request.POST.get('question_count', 5))
    mode = request.POST.get('mode', 'normal')

    if not nickname:
        messages.error(request, '請先輸入暱稱。')
        return redirect('quiz:index')

    if mode == 'wrong':
        wrong_ids = request.session.get(WRONG_BOOK_KEY, [])
        questions = list(Question.objects.filter(id__in=wrong_ids).prefetch_related('choices'))
        if not questions:
            messages.error(request, '目前沒有錯題紀錄，請先完成一次一般測驗。')
            return redirect('quiz:index')
    else:
        questions = list(Question.objects.all().prefetch_related('choices'))

    random.shuffle(questions)
    questions = questions[:min(question_count, len(questions))]

    quiz_data = []
    for question in questions:
        choices = list(question.choices.all())
        random.shuffle(choices)
        quiz_data.append({
            'question': question,
            'choices': choices,
        })

    request.session['nickname'] = nickname
    request.session['quiz_mode'] = mode
    request.session['current_question_ids'] = [q.id for q in questions]

    return render(request, 'quiz/quiz.html', {
        'nickname': nickname,
        'quiz_mode': mode,
        'quiz_data': quiz_data,
    })


def submit_quiz(request):
    if request.method != 'POST':
        return redirect('quiz:index')

    question_ids = request.session.get('current_question_ids', [])
    nickname = request.session.get('nickname', '匿名')
    quiz_mode = request.session.get('quiz_mode', 'normal')

    questions = Question.objects.filter(id__in=question_ids).prefetch_related('choices')
    question_map = {q.id: q for q in questions}

    results = []
    correct_count = 0
    wrong_question_ids = []

    for question_id in question_ids:
        question = question_map.get(question_id)
        if not question:
            continue

        selected_choice_id = request.POST.get(f'question_{question_id}')
        correct_choice = question.choices.filter(is_correct=True).first()
        selected_choice = None
        is_correct = False

        if selected_choice_id:
            try:
                selected_choice = question.choices.get(id=int(selected_choice_id))
                is_correct = bool(selected_choice.is_correct)
            except (Choice.DoesNotExist, ValueError):
                selected_choice = None

        if is_correct:
            correct_count += 1
        else:
            wrong_question_ids.append(question.id)

        results.append({
            'question': question,
            'selected_choice': selected_choice,
            'correct_choice': correct_choice,
            'is_correct': is_correct,
            'is_unanswered': selected_choice is None,
        })

    old_wrong_ids = request.session.get(WRONG_BOOK_KEY, [])

    if quiz_mode == 'wrong':
        # 錯題複習模式中，答對的題目會從錯題本移除，仍答錯的保留。
        answered_correct_ids = [
            item['question'].id for item in results if item['is_correct']
        ]
        new_wrong_ids = [
            qid for qid in old_wrong_ids if qid not in answered_correct_ids
        ]
        new_wrong_ids = list(set(new_wrong_ids + wrong_question_ids))
    else:
        new_wrong_ids = list(set(old_wrong_ids + wrong_question_ids))

    request.session[WRONG_BOOK_KEY] = new_wrong_ids
    request.session.modified = True

    total_questions = len(results)
    wrong_count = total_questions - correct_count
    accuracy = round((correct_count / total_questions) * 100) if total_questions else 0

    return render(request, 'quiz/result.html', {
        'nickname': nickname,
        'quiz_mode': quiz_mode,
        'results': results,
        'total_questions': total_questions,
        'correct_count': correct_count,
        'wrong_count': wrong_count,
        'accuracy': accuracy,
    })


def clear_wrong_book(request):
    request.session[WRONG_BOOK_KEY] = []
    request.session.modified = True
    messages.success(request, '錯題紀錄已清除。')
    return redirect('quiz:index')
