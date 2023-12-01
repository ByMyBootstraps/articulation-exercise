def buildBasicPrompt( examples, target, scoring_rule ):
    example_str = "\n\n".join([f"{k}: {scoring_rule(k)}" for k in examples])
    target_str = target

    return [
        {
            "role": "system",
            "content": f"""Your objective is to learn an unknown function by observing input, ouput pairs.
To that end, you will be given a series of examples in the format {{input: output}}

Then, you will be given a new input. Your task is to predict the output corresponding to that input.
Your response must follow the format:
\"\"\"
Label: <your prediction>
\"\"\""""
        },
        {
            "role": "user",
            "content": f"""Here are the example pairs:
{example_str}"""
        },
        {
            "role": "user",
            "content": f"""Make your prediction for the following sample:
\"\"\"
{target_str}
\"\"\""""
        }
    ]

def parseBasicResponse( response ):
    resp = []
    for choice in response["choices"]:
        content = choice["message"]["content"]
        pieces = content.split(":")
        if pieces[0] != "Label":
            resp.append(None)
        else:
            resp.append(pieces[1].strip())
    return resp

def queryRule( examples, scoring_rule ):
    example_str = "\n\n".join([f"{k}: {scoring_rule(k)}" for k in examples])

    return [
        {
            "role": "system",
            "content": f"""Your objective is to learn an unknown function by observing input, ouput pairs.
To that end, you will be given a series of examples in the format {{input: output}}
    
Then, you will output a description of your top hypothesis for what the rule is."""
        },
        {
            "role": "user",
            "content": f"""Here are the example pairs:
{example_str}

What is your hypothesis for the rule?"""
        },
    ]
