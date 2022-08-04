# -*- coding: utf-8 -*-
import re
from difflib import SequenceMatcher

"""
해당 코드는 다음 github 의 도움을 받았음을 밝힙니다.
: https://github.com/neotune/python-korean-handler
"""

"""
    초성 중성 종성 분리 하기
	유니코드 한글은 0xAC00 으로부터
	초성 19개, 중성21개, 종성28개로 이루어지고
	이들을 조합한 11,172개의 문자를 갖는다.

	한글코드의 값 = ((초성 * 21) + 중성) * 28 + 종성 + 0xAC00
	(0xAC00은 'ㄱ'의 코드값)

	따라서 다음과 같은 계산 식이 구해진다.
	유니코드 한글 문자 코드 값이 X일 때,

	초성 = ((X - 0xAC00) / 28) / 21
	중성 = ((X - 0xAC00) / 28) % 21
	종성 = (X - 0xAC00) % 28

	이 때 초성, 중성, 종성의 값은 각 소리 글자의 코드값이 아니라
	이들이 각각 몇 번째 문자인가를 나타내기 때문에 다음과 같이 다시 처리한다.

	초성문자코드 = 초성 + 0x1100 //('ㄱ')
	중성문자코드 = 중성 + 0x1161 // ('ㅏ')
	종성문자코드 = 종성 + 0x11A8 - 1 // (종성이 없는 경우가 있으므로 1을 뺌)
"""
# 유니코드 한글 시작 : 44032, 끝 : 55199
BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

DOUBLE_KOREAN_DICT = {
    # 이중자음
    'ㄲ': 'ㄱㄱ',
    'ㄸ': 'ㄷㄷ',
    'ㅃ': 'ㅂㅂ',
    'ㅆ': 'ㅅㅅ',
    'ㅉ': 'ㅈㅈ',
    'ㄳ': 'ㄱㅅ',
    'ㄵ': 'ㄴㅈ',
    'ㄶ': 'ㄴㅎ',
    'ㄺ': 'ㄹㄱ',
    'ㄻ': 'ㄹㅁ',
    'ㄼ': 'ㄹㅂ',
    'ㄽ': 'ㄹㅅ',
    'ㄾ': 'ㄹㅌ',
    'ㄿ': 'ㄹㅍ',
    'ㅀ': 'ㄹㅎ',
    'ㅄ': 'ㅂㅅ',
    # 이중모음
    'ㅐ': 'ㅏㅣ',
    'ㅒ': 'ㅑㅣ',
    'ㅔ': 'ㅓㅣ',
    'ㅖ': 'ㅕㅣ',
    'ㅘ': 'ㅗㅏ',
    'ㅙ': 'ㅗㅐ',
    'ㅚ': 'ㅗㅣ',
    'ㅝ': 'ㅜㅓ',
    'ㅞ': 'ㅜㅔ',
    'ㅟ': 'ㅜㅣ',
    'ㅢ': 'ㅡㅣ'
}

def convert(test_keyword):
    split_keyword_list = list(test_keyword)
    result = list()

    for keyword in split_keyword_list:
        # 한글인지 확인 후 진행합니다.
        if re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', keyword) is not None:
            char_code = ord(keyword) - BASE_CODE

            # char1: 초성
            char1 = int(char_code / CHOSUNG)
            result.append(CHOSUNG_LIST[char1])

            # char2: 중성
            char2 = int((char_code - (CHOSUNG * char1)) / JUNGSUNG)
            result.append(JUNGSUNG_LIST[char2])

            # char3: 종성
            char3 = int((char_code - (CHOSUNG * char1) - (JUNGSUNG * char2)))
            if char3==0:
                pass

            else:
                result.append(JONGSUNG_LIST[char3])

        else:
            result.append(keyword)

    return ''.join(result)

def divide_more(s: str):
    """
    '짜장면' 과 '자장면'이 더 가까워질 수 있도록 하는 함수입니다.
    
    'ㅑ' 와 'ㅏ' 는 유사합니다.
    하지만 이것까지는 다루는 것은 상당히 어렵다고 판단해서 제외하였습니다.
    """
    for k, v in DOUBLE_KOREAN_DICT.items():
        s = s.replace(k, v)

    return s

def get_ko_sim1(str1: str, str2: str, speed: int = 0):
    str1, str2 = convert(str1), convert(str2)
    
    if speed == 0:
        score = SequenceMatcher(None, str1, str2).ratio()
    
    elif speed == 1:
        score = SequenceMatcher(None, str1, str2).quick_ratio()
    
    else:
        score = SequenceMatcher(None, str1, str2).real_quick_ratio()
    
    return score

def get_ko_sim2(str1: str, str2: str, speed: int = 0):
    print(str1, str2)

    str1, str2 = convert(str1), convert(str2)
    print(str1, str2)

    str1, str2 = divide_more(str1), divide_more(str2)
    
    print(str1, str2)
    
    if speed == 0:
        score = SequenceMatcher(None, str1, str2).ratio()
    
    elif speed == 1:
        score = SequenceMatcher(None, str1, str2).quick_ratio()
    
    else:
        score = SequenceMatcher(None, str1, str2).real_quick_ratio()
    
    return score

    
if __name__ == '__main__':
    str1 = '초절정 스위스 여신과 가슴이 두근거리는 데이트'
    str2 = '초절정 스미스 머신과 가슴 이두근 고립 웨이트'
    
    vanilla_score = SequenceMatcher(None, str1, str2).ratio()
    score = get_ko_sim1(str1, str2)
    quick_score = get_ko_sim1(str1, str2, speed=1)
    real_quick_score = get_ko_sim1(str1, str2, speed=2)
    
    print(f'str1: {str1}\n'
          + f'str2: {str2}\n'
          + f'vanilla_score: {vanilla_score}\n'
          + f'score: {score}\n'
          + f'quick_score: {quick_score}\n'
          + f'real_quick_score: {real_quick_score}\n')

    str1 = '자장면'
    str2 = '짜장면'

    score1 = get_ko_sim1(str1, str2)
    score2 = get_ko_sim2(str1, str2)
    
    print(f'str1: {str1}\n'
          + f'str2: {str2}\n'
          + f'score1: {score1}\n'
          + f'score2: {score2}\n')