import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# 함수에 @register.filter 애너테이션을 적용하면 템플릿에서 해당 함수를 필터로 사용할 수 있게 된다.
@register.filter
def sub(value, arg):
    return value - arg


# mark 함수는 markdown 모듈과 mark_safe 함수를 이용하여 입력 문자열을 HTML로 변환하는 필터 함수이다.
@register.filter
def mark(value):
    """
    마크다운에는 몇 가지 확장 기능이 있는데,
    nl2br은 줄바꿈 문자를 <br>로 바꾸어 준다. (nl2br을 사용하지 않을 경우 줄바꿈을 하기 위해서는 줄 끝에 스페이스를 두개 연속으로 입력해야 한다.)
    fenced_code는 위에서 살펴본 마크다운의 소스코드 표현을 위해 필요하다.
    """
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))