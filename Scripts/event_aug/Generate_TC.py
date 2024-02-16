import openai
import json
import re
import time

openai.api_key = YOUR_OPENAI_KEY

def Request_GPT_generate(request):
    request = [{"role": "user",
                "content": request}]

    '''make the call,'''
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', max_tokens=2048, temperature=0.3, messages = request)
    response = response['choices'][0]['message']['content']
    def return_with_patten(pattern,response):
        return re.findall(pattern, response)[0].strip()
    results = return_with_patten(r'Text Completion:(.*)',response).split('|')
    return results

def concat_json(json_file_path,new_list):
    with open(json_file_path, 'r+') as file:
        data = json.load(file)
        data.extend(new_list)
        file.seek(0)  # 移动文件指针到文件开头
        json.dump(data, file, indent=4)  # 将数据写回文件并格式化
        file.truncate()
        file.close()
               
def Generate_TC(qa_list,template):
    #import ipdb;ipdb.set_trace()
    # 18391 piece of data
    for i in range(150,len(qa_list)):
        temp_dict = {}
        for j in ['QA1','QA2','QA3','QA4','QA5']:
            #import ipdb;ipdb.set_trace()
            question = qa_list[i][j][0]
            answer = qa_list[i][j][1]
            prompt = template.format(question,answer)
            result = Request_GPT_generate(prompt)
            temp_dict[j] = result
        
        print(f"adding into TC list {i}")    
        concat_json('EvEdit/EvEdit_benchmark/Completion.json',[temp_dict])
        
    
                 
def main():
    with open('EvEdit/EvEdit_benchmark/QA.json','r') as f1:
        qa_list = json.load(f1)   
    with open('EvEdit/EvEdit_benchmark/Text_Completion.txt','r') as f2:
        template = f2.read()
    Generate_TC(qa_list,template)
    
if __name__ == "__main__":
    main()