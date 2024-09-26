![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

<hr/>

# Prompt flow AI For Business
Đây là phần Prompt flow AI cho dự án AI For Business của ATS. README này bao gồm yêu cầu dự án, và cách execute và chạy test.
## Yêu cầu phần mềm
### Python 3
Phiên bản tối thiểu: 3.12.5 (Có thể sử dụng phiên bản mới nhất).
https://www.python.org/downloads/
Phải link .venv trước mới xài được pip
```
cho windows
> python -m .\.venv
```
### Visual Studio Code
Chắc ai cũng có rồi =))
https://code.visualstudio.com/
### Prompt flow for Visual Studio Code
Cái này cung cấp giao diện cho các file Promptflow, cụ thể `flow.dag.yaml`
(Có thể vào tab Extensions của Visual Studio Code, search promptflow và tải về kết quả đầu tiên)
https://marketplace.visualstudio.com/items?itemName=prompt-flow.prompt-flow
### Pycharm (Optional)
Mạnh hơn Visual Code nhưng phải nôn tiền ra cho JetBrains
https://www.jetbrains.com/pycharm/download/

## Chuẩn bị debug
### 0. Link .venv
Phải link .venv trước mới xài được pip
```
cho windows
> python -m .\.venv
```
### 1. Cài đặt các dependencies
Terminal > New Terminal
```
> pip install -r requrements.txt
```
### 2. Chuẩn bị prompt flow
1. Thanh bên > Logo Promptflow
2. Đợi hơi lâu với lại máy nào RAM <16gb sẽ lag
3. Khi promotflow load xong thì ở khung FLOWS, chọn thư mục ".."
Sau đó chọn AI_for_Business và ấn nút "Open"
![alt text](image.png)
Nó sẽ ra giao diện như thế này:
![alt text](image-1.png)
4. Nếu nó kêu install dependencies thì chạy lệnh
```
> pip install promptflow promptflow-tools
```
5. Sau đó quay lại flow
### 3. Chạy promptflow
1. Vẫn là ở Logo Promptflow
2. Ấn nút "Test"
3. Chọn "Run in Interactive Mode (Text Only)"

## Tạo và chạy Docker Image (Nếu có thay đổi code)
### Tạo Dockerfile
1. Thanh bên > Logo Promptflow
2. Khi promotflow load xong thì ở khung FLOWS, chọn thư mục ".."
3. Sau đó chọn AI_for_Business và ấn nút "Build"
4. Chọn Build As Docker
5. Chọn folder docker (k có thì tạo)
6. Ấn nút "Create Dockerfile"
### Build docker image
1. Terminal > New Terminal
2. Chạy lệnh
```
cd docker
docker build . -t promptflow
docker run -p 8080:8080 -e OPENAI_API_KEY="<tự lên azure mà lấy API key>" promptflow
```
<hr/>

(Docs của MS)
# Use Functions with Chat Models

This flow covers how to use the LLM tool chat API in combination with external functions to extend the 
capabilities of GPT models. 

`functions` is an optional parameter in the <a href='https://platform.openai.com/docs/api-reference/chat/create' target='_blank'>Chat Completion API</a> which can be used to provide function 
specifications. The purpose of this is to enable models to generate function arguments which adhere to the provided 
specifications. Note that the API will not actually execute any function calls. It is up to developers to execute 
function calls using model outputs. 

If the `functions` parameter is provided then by default the model will decide when it is appropriate to use one of the 
functions. The API can be forced to use a specific function by setting the `function_call` parameter to 
`{"name": "<insert-function-name>"}`. The API can also be forced to not use any function by setting the `function_call` 
parameter to `"none"`. If a function is used, the output will contain `"finish_reason": "function_call"` in the 
response, as well as a `function_call` object that has the name of the function and the generated function arguments. 
You can refer to <a href='https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb' target='_blank'>openai sample</a> for more details.


## What you will learn

In this flow, you will learn how to use functions with LLM chat models and how to compose function role message in prompt template.

## Tools used in this flow
- LLM tool
- Python tool

## References
- <a href='https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb' target='_blank'>OpenAI cookbook example</a>
- <a href='https://openai.com/blog/function-calling-and-other-api-updates?ref=upstract.com' target='_blank'>OpenAI function calling announcement</a> 
- <a href='https://platform.openai.com/docs/guides/gpt/function-calling' target='_blank'>OpenAI function calling doc</a>
- <a href='https://platform.openai.com/docs/api-reference/chat/create' target='_blank'>OpenAI function calling API</a>
