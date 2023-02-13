from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

"""
로그인 상태가 아닐 때, request.user에는 User 객체가 아닌 AnonymousUser 객체가 들어있다.
질문 생성(question_create), 답변 생성(answer_create) 시 author 속성을 정의할 때 User를 이용하도록 했으므로 로그인 상태가 아닐 때 오류가 발생한다.

이 문제를 해결하기 위해 request.user를 사용하는 함수에 @login_required 애너테이션을 사용해야 한다.
@login_required 애너테이션이 붙은 함수는 로그인이 필요한 함수를 의미한다.
"""


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        """
        POST 방식에서는 request.POST를 인수로 생성
        -> request.POST를 인수로 QuestionForm을 생성할 경우에는 request.POST에 담긴 subject, content 값이 QuestionForm의 subject, content 속성에 자동으로 저장되어 객체가 생성된다.

        request.POST에넌 화면에서 사용자가 입력한 내용들이 담겨있다.
        """
        form = QuestionForm(request.POST)
        if form.is_valid():  # 폼이 유효하다면 -> form에 저장된 subject, content의 값이 올바른지 확인 -> 올바르지 않다면 form에 오류 메시지가 저장되므로 화면에 오류 표시 가능
            question = form.save(commit=False)  # 임시 저장(commit=False)하여 question 객체를 리턴받는다.
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()  # 실제 저장을 위해 작성일시를 설정한다.
            question.save()  # 데이터를 실제로 저장한다.
            return redirect('pybo:index')
    else:
        form = QuestionForm()  # GET 방식에서는 QuestionForm을 인수 없이 생성
    context = {'form': form}
    # return render(request, 'pybo/question_form.html', {'form': form}) # {'form': form}은 템플릿에서 질문 등록 시 사용할 폼 엘리먼트를 생성할 때 쓰인다.
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        """
        로그인한 사용자와 질문의 글쓴이가 다를 경우 '수정권한이 없습니다'라는 오류를 발생시킨다.
        이 오류를 발생시키기 위해 messages 모듈을 이용하였다.
        messages는 장고가 제공하는 모듈로 넌필드 오류(non-field error)를 발생시킬 경우에 사용한다.
        """
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == 'POST':
        # POST 요청인 경우 수정된 내용을 반영해야 하는 케이스이므로 다음처럼 폼을 생성해야 한다.
        form = QuestionForm(request.POST, instance=question) # instance를 기준으로 QuestionForm을 생성하지만 request.POST의 값으로 덮어쓰라는 의미이다.
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now() # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        # GET 요청인 경우 질문수정 화면에 조회된 질문의 제목과 내용이 반영될 수 있도록 해야 한다.
        form = QuestionForm(instance=question) # 폼 생성시 이처럼 instance 값을 지정하면 폼의 속성 값이 instance의 값으로 채워진다.
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')


@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        """
        Question 모델의 voter는 여러사람을 추가할 수 있는 ManyToManyField이므로 question.voter.add(request.user)처럼 add 함수를 사용하여 추천인을 추가한다.
        
        동일한 사용자가 동일한 질문을 여러번 추천하더라도 추천수가 증가하지는 않는다.
        동일한 사용자를 add 할 경우에 오류가 발생할것 같지만 오류는 발생하지 않는다.
        오류도 발생하지 않고 추가되지도 않는다.
        이는 ManyToManyField 내부에서 자체적으로 처리된다.
        """
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)