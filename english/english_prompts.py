import openai

def basic_prompt(model, question, choices, is_front, emotion_prompt, question_plus=""):
    system_prompt = "대학수학능력검정시험 영어 영역을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오. "
    system_prompt += emotion_prompt if is_front else ""
    
    system_prompt += """
    
         문제를 풀이할 때, 반드시 지문을 참고하세요.
         문제는 무조건 1개의 정답만 있습니다.
         문제를 풀이할 때 모든 선택지들을 검토하세요.
         모든 선택지마다 근거를 지문에서 찾아 설명하세요.

         다음의 형식을 따라 답변하세요.

         1번: "(지문 속 근거가 된 문장)" + (자세한 풀이) + (선택지 1번에 대한 답변)
         2번: "(지문 속 근거가 된 문장)" + (자세한 풀이) + (선택지 2번에 대한 답변)
         3번: "(지문 속 근거가 된 문장)" + (자세한 풀이) + (선택지 3번에 대한 답변)
         4번: "(지문 속 근거가 된 문장)" + (자세한 풀이) + (선택지 4번에 대한 답변)
         5번: "(지문 속 근거가 된 문장)" + (자세한 풀이) + (선택지 5번에 대한 답변)
         최종 정답: (최종 정답)
    """
    
    user_prompt = ""

    if question_plus:
        user_prompt += f"""
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

    # for test
    # return system_prompt + user_prompt
    
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

def data_prompt(model, question, choices, is_front, emotion_prompt, question_plus=""):
    system_prompt = "대학수학능력검정시험 영어 영역을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오. "
    system_prompt += emotion_prompt if is_front else ""
    
    system_prompt += """
    
         문제를 풀이할 때, 반드시 지문을 참고하세요.
         문제는 무조건 1개의 정답만 있습니다.
         문제를 풀이할 때 모든 선택지들을 검토하세요.
         모든 선택지마다 근거를 지문에서 찾아 설명하세요.

         다음의 형식을 따라 답변하세요.

         1번: "(지문과 자료 속 근거가 된 문장)" + (자세한 풀이) + (선택지 1번에 대한 답변)
         2번: "(지문과 자료 속 근거가 된 문장)" + (자세한 풀이) + (선택지 2번에 대한 답변)
         3번: "(지문과 자료 속 근거가 된 문장)" + (자세한 풀이) + (선택지 3번에 대한 답변)
         4번: "(지문과 자료 속 근거가 된 문장)" + (자세한 풀이) + (선택지 4번에 대한 답변)
         5번: "(지문과 자료 속 근거가 된 문장)" + (자세한 풀이) + (선택지 5번에 대한 답변)
         최종 정답: (최종 정답)
    """
    
    user_prompt = ""

    if question_plus:
        user_prompt += f"""
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

    # for test
    # return system_prompt + user_prompt
    
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

def ordering_prompt(model, question, choices, is_front, emotion_prompt, question_plus=""):
    system_prompt = "대학수학능력검정시험 영어 영역을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오. "
    system_prompt += emotion_prompt if is_front else ""
    
    system_prompt += """
    
         문제를 풀이할 때, 반드시 지문을 참고하세요.
         문제는 무조건 1개의 정답만 있습니다.
         문제를 풀이할 때 모든 선택지들을 검토하세요.
         모든 선택지마다 근거를 지문에서 찾아 설명하세요.

         다음의 형식을 따라 답변하세요.
         
         1번: "(문장 순서에 대한 설명)" + (자세한 풀이) + (선택지 1번에 대한 답변)
         2번: "(문장 순서에 대한 설명)" + (자세한 풀이) + (선택지 2번에 대한 답변)
         3번: "(문장 순서에 대한 설명)" + (자세한 풀이) + (선택지 3번에 대한 답변)
         4번: "(문장 순서에 대한 설명)" + (자세한 풀이) + (선택지 4번에 대한 답변)
         5번: "(문장 순서에 대한 설명)" + (자세한 풀이) + (선택지 5번에 대한 답변)
         최종 정답: (최종 정답)
    """
    
    user_prompt = ""

    if question_plus:
        user_prompt += f"""
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

    # for test
    # return system_prompt + user_prompt
    
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
