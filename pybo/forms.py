from django import forms
from .models import Question, Answer

"""
장고의 폼은 일반 폼(forms.Form)과 모델 폼(forms.ModelForm)이 있는데 모델 폼은 모델(Model)과 연결된 폼으로 폼을 저장하면 연결된 모델의 데이터를 저장할 수 있는 폼이다.
모델 폼은 이너 클래스인 Meta 클래스가 반드시 필요하다.
Meta 클래스에는 사용할 모델과 모델의 속성을 적어야 한다.
"""
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question # 사용할 모델
        fields = ['subject', 'content'] # QuestionForm에서 사용할 Question 모델의 속성
        # widgets = { # {{ form.as_p }}로 HTML 코드를 자동으로 생성할 때 스타일, 라벨 커스터마이징
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        # }
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }