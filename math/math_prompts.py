import openai


def basic_prompt(model, question, choices, question_plus="", is_front=False, emotion_prompt=""):
    system_prompt = "대학수학능력검정시험 수학 영역을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오. "
    system_prompt += emotion_prompt if is_front else ""
    
    system_prompt += """
    
         고등학생 수학 지식 범위 안에서 문제를 풀이하세요.
         문제는 무조건 1개의 정답만 있습니다.
         문제 풀이를 완료한 이후 선택지에서 본인의 답을 고르세요.
         만약 문제의 조건이 있다면 풀이 시 해당 조건을 만족하는 답을 구하시오.

         다음의 형식을 따라 답변하세요.
         문제 풀이: (문제에 대한 자세한 풀이)
         최종 정답: (1~5번 중 최종 선택)
    """
    
    user_prompt = ""

    if question_plus:
        user_prompt += f"""
            이 문제는 아래와 같이 [조건]이 주어져 있습니다. ~~
            문제의 각 선택지들을 해결하기 위한 배경 지식을 설명해 주고 있는 것이 <조건>로써, 각 선택지들을 지문과 연결시키고, <조건>의 지식을 활용하면 각 선택지의 참과 거짓을 판단할 수 있습니다.
            문제를 해결할 때, 반드시 <조건>의 내용을 이용해서 문제를 해결해야 합니다.
            [조건] :
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

    # ChatGPT, GPT-4 API generation
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

def no_choice_prompt(model, question, question_plus="", is_front=False, emotion_prompt=""):
    system_prompt = "대학수학능력검정시험 수학 영역을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오. "
    system_prompt += emotion_prompt if is_front else ""
    
    system_prompt += """
    
         고등학생 수학 지식 범위 안에서 문제를 풀이하세요.
         문제는 무조건 1개의 정답만 있습니다.
         만약 문제의 조건이 있다면 풀이 시 해당 조건을 만족하는 답을 구하시오.

         다음의 형식을 따라 답변하세요.
         문제 풀이: (문제에 대한 자세한 풀이)
         최종 정답: (1~5번 중 최종 선택)
    """

    user_prompt = ""

    if question_plus:
        user_prompt += f"""
            이 문제는 아래와 같이 [조건]이 주어져 있습니다. ~~
            문제의 각 선택지들을 해결하기 위한 배경 지식을 설명해 주고 있는 것이 <조건>으로써
            문제를 해결할 때, 반드시 <조건>의 내용을 이용해서 문제를 해결해야 합니다.
            [조건] :
            {question_plus}
        """
    
    user_prompt += f"""
        질문 :
        {question}
    """
    user_prompt += emotion_prompt if not is_front else ""

    # ChatGPT, GPT-4 API generation
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
