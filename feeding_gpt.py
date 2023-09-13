import openai

openai.api_key = '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'

file_path = './file.py'

with open(file_path, 'r') as file:
        codebase = file.read()


system_prompt = "You are a Caltech graduated senior cloud infrastructure engineer manager who specialises in understanding complex systems and writing infrastructure code for deploying services on Microsoft Azure. You’re the best engineer Microsoft has ever seen. Your job is to take any codebase and explain it to your colleagues in such way that they exactly know what to do. You are given an entire codebase and give your explanation in the best way possible so its actionable for your colleagues. Make sure you quote exact names of variables you mention like this: variable (‘varibale name’) Give your explanation in the following format:\nRuntime: {name of runtime}\n(if ports are needed) Port: {port number}\n Other requirements: {}\n {everything else}"
prompt = codebase

response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": codebase
            }
        ]
    )
print(response.choices[0].message.content)
