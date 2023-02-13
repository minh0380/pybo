from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q

from ..models import Question


def index(request):
    """
    page = request.GET.get('page', '1')은 http://localhost:8000/pybo/?page=1 처럼 GET 방식으로 호출된 URL에서 page값을 가져올 때 사용한다.
    만약 http://localhost:8000/pybo/ 처럼 page값 없이 호출된 경우에는 디폴트로 1이라는 값을 설정한다.
    """
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '') # 검색어
    question_list = Question.objects.order_by('-create_date')  # - 기호가 붙어있으면 역방향, 없으면 순방향 정렬
    if kw:
        """
            Q함수는 OR조건으로 데이터를 조회하기 위해 사용하는 함수이다.
            그리고 filter 함수 뒤에 사용된 distinct는 조회 결과에 중복이 있을 경우 중복을 제거하여 리턴하는 함수이다.
            하나의 질문에는 여러 개의 답변이 있을 수 있다. 이 때 여러 개의 답변이 검색 조건에 해당될 때 동일한 질문이 중복으로 조회될 수 있다. 이런 이유로 중복된 질문을 제거하기 위해 distinct를 사용했다.
        """
        question_list = question_list.filter(
            Q(subject__icontains=kw) | # 제목 검색
            Q(content__icontains=kw) | # 내용 검색
            Q(answer__content__icontains=kw) | # 답변 내용 검색
            Q(author__username__icontains=kw) | # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw) # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기

    """
    paginator를 이용하여 요청된 페이지(page)에 해당되는 페이징 객체(page_obj)를 생성했다.
    이렇게 하면 장고 내부적으로는 데이터 전체를 조회하지 않고 해당 페이지의 데이터만 조회하도록 쿼리가 변경된다.
    """
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw}

    # render 함수는 파이썬 데이터를 템플릿에 적용하여 HTML로 반환하는 함수
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)