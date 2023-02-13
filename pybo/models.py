from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 장고에서 사용하는 속성(Field) 타입 참고 : https://docs.djangoproject.com/en/4.0/ref/models/fields/#field-types


class Question(models.Model):
    # 질문의 제목
    subject = models.CharField(max_length=200) # 글자수의 길이가 제한된 텍스트는 CharField를 사용
    # 질문의 내용
    content = models.TextField() # 글자수를 제한할 수 없는 텍스트는 TextField 사용
    # 질문을 작성한 일시
    create_date = models.DateTimeField() # 날짜와 시간에 관계된 속성은 DateTimeField 사용
    # 질문의 수정 일시
    modify_date = models.DateTimeField(null=True, blank=True) # null=True는 데이터베이스에서 modify_date 칼럼에 null을 허용한다는 의미이며, blank=True는 form.is_valid()를 통한 입력 데이터 검증 시 값이 없어도 된다는 의미이다.

    """
    Question 모델에서 사용한 author와 voter가 모두 User 모델과 연결되어 있기 때문에 User.question_set처럼 User 모델을 통해서 Question 데이터에 접근하려고 할 때 author를 기준으로 해야 할지 명확하지 않다.
    이를 해결하기 위해 related_name 인수를 추가해야 한다.
    
    author에는 related_name='author_question'라는 인수를 지정하고 voter에는 related_name='voter_question'라는 인수를 지정했다.
    이렇게 하면 이제 특정 사용자가 작성한 질문을 얻기 위해서는 some_user.author_question.all() 처럼 사용할 수 있다.
    마찬가지로 특정 사용자가 추천한 질문을 얻기 위해서는 some_user.voter_question.all() 처럼 사용할 수 있다.
    """
    # 질문의 작성자
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    # 추천인
    voter = models.ManyToManyField(User, related_name='voter_question') # 하나의 질문에 여러명이 추천할 수 있고 한 명이 여러 개의 질문에 추천할 수 있으므로 이런 경우에는 "다대다(N:N)" 관계를 의미하는 ManyToManyField를 사용해야 한다.

    """
    저장한 Question 모델의 데이터는 Question.objects를 통해서 조회할 수 있다.
    Question.objects.all()은 모든 Question 데이터를 조회하는 함수이다.
    결과값으로는 QuerySet 객체가 리턴되는데 <QuerySet [<Question: Question object (1)>, <Question: Question object (2)>]>에서 1과 2는 Question 데이터의 id 값이다.
    Question 모델에 __str__ 메서드를 추가하면 id 값 대신 제목을 표시할 수 있다.
    """
    def __str__(self):
        return self.subject


class Answer(models.Model):
    # 질문 (어떤 질문의 답변인지 알아야하므로 질문 속성이 필요하다)
    """
    Answer 모델은 질문에 대한 답변에 해당되므로 Question 모델을 속성을 가져가야 한다.
    기존 모델을 속성으로 연결하려면 ForeignKey를 사용해야 한다.
    ForeignKey는 다른 모델과 연결하기 위해 사용한다.
    on_delete=models.CASCADE의 의미는 이 답변과 연결된 질문(Question)이 삭제될 경우 답변(Answer)도 함께 삭제된다는 의미이다.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # 답변의 내용
    content = models.TextField() # 답변의 내용
    # 답변을 작성한 일시
    create_date = models.DateTimeField() # 답변을 작성한 일시
    # 답변의 작성자
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    # 답변의 수정 일시
    modify_date = models.DateTimeField(null=True, blank=True)
    # 추천인
    voter = models.ManyToManyField(User, related_name='voter_answer')