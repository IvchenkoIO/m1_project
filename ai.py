import openai

def req():
    openai.api_key="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"
    model_engine = "text-davinci-003"
    prompt = "describe the ip"

    
    # set max number of words
    max_tokens = 128

    # generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(completion.choices[0].text)
    # display the answer
    return completion.choices[0].text

req()