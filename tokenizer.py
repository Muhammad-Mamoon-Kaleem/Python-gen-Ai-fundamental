import tiktoken

text = 'i love pakistan'
encoding = tiktoken.encoding_for_model("gpt-4")
tokenIds=encoding.encode(text)
print(tokenIds)

