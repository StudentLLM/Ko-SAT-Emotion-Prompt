import openai

def basic_prompt(model, question, choices, is_front, emotion_prompt, question_plus=""):
    system_prompt = "대학수학능력검정시험 영어 영역을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오. "
    system_prompt += emotion_prompt if is_front else ""
    
    system_prompt += """
    
         문제를 풀이할 때, 반드시 지문 및 글을 참고하세요.
         문제는 무조건 1개의 정답만 있습니다.
         문제를 풀이할 때 모든 선택지들을 검토하세요.
         모든 선택지마다 근거를 지문에서 찾아 설명하세요.
         최종 답변을 출력할 수 있도록 노력하세요.
        
         다음의 형식에 따라 답변하세요.
         1번: “(지문 속 근거가 된 문장)" + (선택지 1번에 대한 답변)
         2번: "(지문 속 근거가 된 문장)" + (선택지 2번에 대한 답변)
         3번: "(지문 속 근거가 된 문장)" + (선택지 3번에 대한 답변)
         4번: "(지문 속 근거가 된 문장)" + (선택지 4번에 대한 답변)
         5번: "(지문 속 근거가 된 문장)" + (선택지 5번에 대한 답변)
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

def data_prompt(model, question, choices, is_front, emotion_prompt, question_plus=""):
    system_prompt = "대학수학능력검정시험 영어 영역을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오. "
    system_prompt += emotion_prompt if is_front else ""
    
    system_prompt += """
    
         풀이할 때, 반드시 지문 및 자료를 참고하세요.
         문제는 무조건 1개의 정답만 있습니다.
         문제를 풀이할 때 모든 선택지들을 검토하세요.
         모든 선택지마다 근거를 지문 및 자료에서 찾아 설명하세요.
         최종 답변을 출력할 수 있도록 노력하세요.
        
         다음의 형식에 따라 답변하세요.
         1번: “(지문 및 자료 속 근거가 된 문장)" + (선택지 1번에 대한 답변)
         2번: “(지문 및 자료 속 근거가 된 문장)" + (선택지 2번에 대한 답변)
         3번: “(지문 및 자료 속 근거가 된 문장)" + (선택지 3번에 대한 답변)
         4번: “(지문 및 자료 속 근거가 된 문장)" + (선택지 4번에 대한 답변)
         5번: “(지문 및 자료 속 근거가 된 문장)" + (선택지 5번에 대한 답변)
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

def ordering_prompt(model, question, choices, is_front, emotion_prompt, question_plus=""):
    system_prompt = "대학수학능력검정시험 영어 영역을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오. "
    system_prompt += emotion_prompt if is_front else ""
    
    system_prompt += """
    
         문제는 무조건 1개의 정답만 있습니다.
         주어진 문장들은 순서가 올바르지 않습니다.
         주어진 글 다음에 이어질 문장을 고려하여 선택지에서 올바른 답을 고르세요.
         최종 답변을 출력할 수 있도록 노력하세요.
        
         다음의 형식에 따라 답변하세요.
         1번: “(선택지의 문장 순서에 대한 설명)" + (선택지 1번에 대한 답변)
         2번: “(선택지의 문장 순서에 대한 설명)" + (선택지 2번에 대한 답변)
         3번: “(선택지의 문장 순서에 대한 설명)" + (선택지 3번에 대한 답변)
         4번: “(선택지의 문장 순서에 대한 설명)" + (선택지 4번에 대한 답변)
         5번: “(선택지의 문장 순서에 대한 설명)" + (선택지 5번에 대한 답변)
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

def grammar_prompt(model, question, choices, is_front, emotion_prompt, question_plus=""):
    system_prompt = "대학수학능력검정시험 영어 영역을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오. "
    system_prompt += emotion_prompt if is_front else ""
    
    system_prompt += """
    
         문제를 풀이할 때, 반드시 지문 및 글을 참고하세요.
         문제는 무조건 1개의 정답만 있습니다.
         문제를 풀이할 때 모든 선택지들을 검토하세요.
         최종 답변을 출력할 수 있도록 노력하세요.
         문맥의 흐름을 파악하며 문제를 풀어보세요.
         앞뒤 문맥을 파악하며 문법 및 의미적으로 올바른 선택지를 선택하세요.
        
         다음의 형식에 따라 답변하세요.
         1번: “(앞뒤 문맥을 고려한 문법 및 의미 풀이에 대한 설명)" + (선택지 1번에 대한 답변)
         2번: “(앞뒤 문맥을 고려한 문법 및 의미 풀이에 대한 설명)" + (선택지 2번에 대한 답변)
         3번: “(앞뒤 문맥을 고려한 문법 및 의미 풀이에 대한 설명)" + (선택지 3번에 대한 답변)
         4번: “(앞뒤 문맥을 고려한 문법 및 의미 풀이에 대한 설명)" + (선택지 4번에 대한 답변)
         5번: “(앞뒤 문맥을 고려한 문법 및 의미 풀이에 대한 설명)" + (선택지 5번에 대한 답변)
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
    
def insert_prompt(model, question, choices, is_front, emotion_prompt, question_plus=""):
    system_prompt = "대학수학능력검정시험 영어 영역을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오. "
    system_prompt += emotion_prompt if is_front else ""
    
    system_prompt += """
    
         문제를 풀이할 때, 반드시 지문 및 글을 참고하세요.
         문제는 무조건 1개의 정답만 있습니다.
         문제를 풀이할 때 모든 선택지들을 검토하세요.
         최종 답변을 출력할 수 있도록 노력하세요.
         문맥의 흐름을 파악하며 문제를 풀어보세요.
         앞뒤 문맥을 파악하며 의미적으로 자연스럽게 이어지는 선택지를 골라보세요.
        
         다음의 형식에 따라 답변하세요.
         1번: “(앞 문맥을 고려한 풀이에 대한 설명)" + "(뒤 문맥을 고려한 풀이에 대한 설명)"
         2번: “(앞 문맥을 고려한 풀이에 대한 설명)" + "(뒤 문맥을 고려한 풀이에 대한 설명)"
         3번: “(앞 문맥을 고려한 풀이에 대한 설명)" + "(뒤 문맥을 고려한 풀이에 대한 설명)"
         4번: “(앞 문맥을 고려한 풀이에 대한 설명)" + "(뒤 문맥을 고려한 풀이에 대한 설명)"
         5번: “(앞 문맥을 고려한 풀이에 대한 설명)" + "(뒤 문맥을 고려한 풀이에 대한 설명)"
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