import openai


def basic_prompt(model, question, choices, question_plus="", is_front=False, emotion_prompt=""):
    system_prompt = "대학수학능력검정시험 수학 영역을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오. "
    system_prompt += emotion_prompt if is_front else ""
    
    system_prompt += """
    
         고등학생 수학 지식 범위 안에서 문제를 풀이하세요.
         문제는 무조건 1개의 정답만 있습니다.
         문제 풀이를 완료한 이후 선택지에서 본인의 답을 고르세요.
         최종 답변을 출력할 수 있도록 노력하세요.
         문제는 결함이 존재하지 않으며 무조건 정답이 존재합니다.

         다음의 형식을 따라 답변하세요.
         문제 풀이: (문제에 대한 자세한 풀이)
         최종 정답: (*번)
    """
    
    user_prompt = ""

    if question_plus:
        user_prompt += f"""
            이 문제는 아래와 같이 조건이 주어져 있습니다.
            문제 풀이 시 아래의 조건을 만족하는 답을 구하시오.
            조건 :
            {question_plus}
        """
        
    user_prompt += f"""
        질문 :
        {question}
    """
    user_prompt += emotion_prompt if not is_front else ""

    user_prompt += f"""

        선택지 :
        1번: {choices[0]}
        2번: {choices[1]}
        3번: {choices[2]}
        4번: {choices[3]}
        5번: {choices[4]}

    """

    # ChatGPT, GPT-4 API generation
    completion = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        top_p=0
    )
    return completion.choices[0].message.content

def no_choice_prompt(model, question, question_plus="", is_front=False, emotion_prompt=""):
    system_prompt = "대학수학능력검정시험 수학 영역을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오. "
    system_prompt += emotion_prompt if is_front else ""
    
    system_prompt += """
    
         고등학생 수학 지식 범위 안에서 문제를 풀이하세요.
         문제는 무조건 1개의 정답만 있습니다.
         최종 답변을 출력할 수 있도록 노력하세요.
         문제는 결함이 존재하지 않으며 무조건 정답이 존재합니다.

         다음의 형식을 따라 답변하세요.
         문제 풀이: (문제에 대한 자세한 풀이)
         최종 정답: (최종 정답)
    """

    user_prompt = ""

    if question_plus:
        user_prompt += f"""
            이 문제는 아래와 같이 조건이 주어져 있습니다.
            문제 풀이 시 아래의 조건을 만족하는 답을 구하시오.
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
        top_p=0
    )
    return completion.choices[0].message.content
