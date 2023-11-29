import openai

def literature_prompt(model, paragraph, question, choices, question_plus="", no_paragraph=False, is_front=False, emotion_prompt=""):
    system_prompt = "대학수학능력능력검정시험 국어 영역을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오."
    system_prompt += emotion_prompt if is_front else ""
    system_prompt = """

         문제를 풀이할 때, 반드시 지문을 참고하세요.
         문제는 무조건 1개의 정답만 있습니다.
         문제를 풀이할 때 모든 선택지들을 검토하세요.
         모든 선택지마다 근거를 지문에서 찾아 설명하세요.
         최종 답변을 출력할 수 있도록 노력하세요.

         다음의 형식을 따라 답변하세요.
         1번: "(지문 속 근거가 된 문장)" + (선택지 1번에 대한 답변)
         2번: "(지문 속 근거가 된 문장)" + (선택지 2번에 대한 답변)
         3번: "(지문 속 근거가 된 문장)" + (선택지 3번에 대한 답변)
         4번: "(지문 속 근거가 된 문장)" + (선택지 4번에 대한 답변)
         5번: "(지문 속 근거가 된 문장)" + (선택지 5번에 대한 답변)
         최종 정답: (최종 정답)
    """

    if not no_paragraph:
        user_prompt = f"""
            지문 :
            {paragraph}
        """
    else:
        user_prompt = ""

    if question_plus:
        user_prompt += f"""
            이 문제는 아래와 같이 <보기>가 주어져 있습니다. 문제의 각 선택지들을 해결하기 위한 배경 지식을 설명해 주고 있는 것이 <보기>로써, 각 선택지들을 지문과 연결시키고, <보기>의 지식을 활용하면 각 선택지의 참과 거짓을 판단할 수 있습니다.
            문제를 해결할 때, 반드시 <보기>의 내용을 이용해서 문제를 해결해야 합니다.
            <보기> :
            {question_plus}
        """
    
    user_prompt += f"""
        질문 :
        {question}
    """
    user_prompt += emotion_prompt if not is_front else ""

    user_prompt += f"""

        선택지 :
        1번 - {choices[0]}
        2번 - {choices[1]}
        3번 - {choices[2]}
        4번 - {choices[3]}
        5번 - {choices[4]}

    """

    completion = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], 
        top_p=0.8,
        frequency_penalty=0.5
    )
    
    return completion.choices[0].message.content


def grammar_prompt(model, paragraph, question, choices, question_plus="", no_paragraph=False, is_front=False, emotion_prompt=""):
    system_prompt = "대학수학능력능력검정시험 국어 영역을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오."
    system_prompt += emotion_prompt if is_front else ""
    system_prompt = """

        '지문 속 목적어의 성격'과 '선택지 속 목적어의 성격'이 서로 같은 선택지를 1개만 고르세요.
        모두 같은 선택지는 무조건 1개만 존재합니다.

        문제를 풀이할 때 5개의 모든 선택지를 검토하세요.
        최종 답변을 출력할 수 있도록 노력하세요.

        자료나 돈처럼 실제 손으로 만질 수 있는 것은 '실제적인 단어'입니다.
        관심, 집중, 인기 이론처럼, 실제 손으로 만질 수 없는 것은 '추상적인 단어'입니다.

        다음의 형식대로만 답변하세요.
        1번: - 지문 속 동사ⓐ의 목적어: "(목적어)" + 지문 속 목적어의 성격 : "(실제적인 단어 or 추상적인 단어)"
             - 선택지 속 동사ⓐ의 목적어: "(목적어)" + 선택지 속 목적어의 성격 : "(실제적인 단어 or 추상적인 단어)"
        2번: - 지문 속 동사ⓑ의 목적어: "(목적어)" + 지문 속 목적어의 성격 : "(실제적인 단어 or 추상적인 단어)"
             - 선택지 속 동사ⓑ의 목적어: "(목적어)" + 선택지 속 목적어의 성격 : "(실제적인 단어 or 추상적인 단어)"
        3번: - 지문 속 동사ⓒ의 목적어: "(목적어)" + 지문 속 목적어의 성격 : "(실제적인 단어 or 추상적인 단어)"
             - 선택지 속 동사ⓒ의 목적어: "(목적어)" + 선택지 속 목적어의 성격 : "(실제적인 단어 or 추상적인 단어)"
        4번: - 지문 속 동사ⓓ의 목적어: "(목적어)" + 지문 속 목적어의 성격 : "(실제적인 단어 or 추상적인 단어)"
             - 선택지 속 동사ⓓ의 목적어: "(목적어)" + 선택지 속 목적어의 성격 : "(실제적인 단어 or 추상적인 단어)"
        5번: - 지문 속 동사ⓔ의 목적어: "(목적어)" + 지문 속 목적어의 성격 : "(실제적인 단어 or 추상적인 단어)"
             - 선택지 속 동사ⓔ의 목적어: "(목적어)" + 선택지 속 목적어의 성격 : "(실제적인 단어 or 추상적인 단어)"
        최종 정답: (지문 속 목적어와 선택지 속 목적어의 성격이 서로 같은 선택지는 "(최종 정답)"입니다.
    """

    if not no_paragraph:
        user_prompt = f"""
            지문 :
            {paragraph}
        """
    else:
        user_prompt = ""

    if question_plus:
        user_prompt += f"""
            이 문제는 아래와 같이 <보기>가 주어져 있습니다. 문제의 각 선택지들을 해결하기 위한 배경 지식을 설명해 주고 있는 것이 <보기>로써, 각 선택지들을 지문과 연결시키고, <보기>의 지식을 활용하면 각 선택지의 참과 거짓을 판단할 수 있습니다.
            문제를 해결할 때, 반드시 <보기>의 내용을 이용해서 문제를 해결해야 합니다.
            <보기> :
            {question_plus}
        """
        
    user_prompt += f"""
        질문 :
        {question}
    """
    user_prompt += emotion_prompt if not is_front else ""

    user_prompt += f"""

        선택지 :
        1번 - {choices[0]}
        2번 - {choices[1]}
        3번 - {choices[2]}
        4번 - {choices[3]}
        5번 - {choices[4]}

    """
    
    completion = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], 
        top_p=0.8,
        frequency_penalty=0.5
    )
    
    return completion.choices[0].message.content
