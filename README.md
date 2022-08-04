# korean-similarity 📊

: To score apparent similarity between korean texts

: 한국어 문자열 유사도를 측정하기 위한 코드입니다.

----

<br>

## 필요성 🔥

<br>

- 두 문자열이 정확히 일치하진 않더라도 유사도를 비교하고 싶을 때

- 의미적인 유사도가 아닌 <u>외형적 유사도</u> 를 구하고 싶을 때

<br>

### 영어

- 사실 이런 문제를 [difflib](https://docs.python.org/ko/3/library/difflib.html) 에서 제공하는 SequenceMatcher 를 통해 어느 정도 해소할 수 있습니다.

<br>

~~~python
from difflib import SequenceMatcher

str1 = 'Insure' # 보험에 들다
str2 = 'Ensure' # 보장하다
str3 = 'Instance' # 예시

# similarity between 'Insure' and 'Ensure'
ratio_12 = SequenceMatcher(None, str1, str2).ratio()

# similarity between 'Insure' and 'Instance'
ratio_13 = SequenceMatcher(None, str1, str3).ratio()

# 0.8333... , 0.5714...
print(ratio_12, ratio_13)
~~~

<br>

### 한국어

- 하지만 한국어는 좀 다릅니다. 왜냐하면, 한글은 자음과 모음을 이용하여 '초성 + 중성 + 종성'이 합쳐지거든요.

- 아래 예시를 보시죠. 유치원생이 실수로 '자존심'을 '자존싱'이라고 썼어요. 그래도 '자존력'보다는 외형적으로 더 높은 점수를 받아 마땅합니다.

- 하지만 점수는 동일합니다. 왜냐하면, 유니코드상 '심' 이나 '싱'이나 '력'이나 다른 글자면 다른 글자거든요. '심' 과 '싱'이 유사한 걸 알 수 없습니다.

<br>

~~~python
from difflib import SequenceMatcher

str1 = '자존심'
str2 = '자존싱'
str3 = '자존력'

# similarity between '자존심' and '자존싱'
ratio_12 = SequenceMatcher(None, str1, str2).ratio()

# similarity between '자존심' and '자존싱'
ratio_13 = SequenceMatcher(None, str1, str3).ratio()

# 0.6666..., 0.6666...
print(ratio_12, ratio_13)
~~~

----

<br>

## 초성 중성 종성 분리 🌞

<br>

- 한글이 유니코드로 인해 갖는 문제점을 어느 정도 해소하고자, 초성 중성 종성을 분리합니다. 분리하는 코드는 아래에 작성된 [neotune](https://github.com/neotune)의 도움을 받았습니다.

- 'get_ko_sim1' 함수를 통해 더 정확한 유사도를 측정하실 수 있습니다.

<br>

~~~python
str1 = '초절정 스위스 여신과 가슴이 두근거리는 데이트'
str2 = '초절정 스미스 머신과 가슴 이두근 고립 웨이트'

score = get_ko_sim1(str1, str2)
quick_score = get_ko_sim1(str1, str2, speed=1)
real_quick_score = get_ko_sim1(str1, str2, speed=2)

print(f'str1: {str1}\n'
        + f'str2: {str2}\n'
        + f'score: {score}\n'
        + f'quick_score: {quick_score}\n'
        + f'real_quick_score: {real_quick_score}\n')
~~~

<br>

다음과 같이 외형 유사도가 더 높게 측정되는 것을 알 수 있습니다.

<br>

~~~
str1: 초절정 스위스 여신과 가슴이 두근거리는 데이트
str2: 초절정 스미스 머신과 가슴 이두근 고립 웨이트

vanilla_score: 0.72  # 일반 점수
score: 0.7920792079207921  # 초성 중성 종성 분리 후 점수
~~~

<br>

참고로, 다음 2개의 점수는 quick_ratio, real_quick_ratio 함수의 값도 함께 출력해본 것입니다. 더 빠르게 값을 구할 수 있다고 하니, 참고하시길 바랍니다. 정확도는 떨어지니, 저는 사용을 권하진 않습니다.

<br>

~~~
quick_score: 0.8514851485148515
real_quick_score: 0.9900990099009901
~~~

<br>

## 이중 자음/모음 분리 추가 ⭐

<br>

- '자장면'과 '짜장면'이 외형적으로도 유사도가 높아야 합니다. 하지만, 지금 코드 상으로는 '자장면'과 '가장면'의 유사도와 똑같겠죠. 유니코드 상, 'ㅈ' 와 'ㅉ' 이 유사하는 걸 모르니까요.

- 그래서 'get_ko_sim2' 를 통해 분리 후 점수를 측정할 수 있습니다.

<br>

~~~python
str1 = '자장면'
str2 = '짜장면'

score1 = get_ko_sim1(str1, str2)
score2 = get_ko_sim2(str1, str2)

print(f'str1: {str1}\n'
        + f'str2: {str2}\n'
        + f'score1: {score1}\n'
        + f'score2: {score2}\n')
~~~

~~~
str1: 자장면
str2: 짜장면
score1: 0.875  # 이중 자음/모음 분리 전
score2: 0.9411764705882353  # 이중 자음/모음 분리 후
~~~

## 의견 🌙

<br>

- 사실 외형적 유사도를 정의할 부분은 많습니다. 'ㅈ' 과 'ㅊ' 도 유사하고, 'ㅋ' 과 'ㄱ'도 유사하죠.

- 하지만 그걸 모두 다루긴 어렵고, 오히려 분리하면서 길이도 달라지고 순서에 따라 점수가 달라질 수도 있습니다.

- 지금 제 코드 역시 완벽한 게 아니며, 편리하게 이용하시라고 만들었습니다. 더 좋은 의견이 있으시면, 언제든지 개선해주신다면 감사드리겠습니다.


----

<br>

## 출처

[neotune](https://github.com/neotune)님의 [python-korean-handler](https://github.com/neotune/python-korean-handler)를 적극 활용하였음을 밝히며, 다시 한번 감사를 전합니다.

----