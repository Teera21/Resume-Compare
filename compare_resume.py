from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
import os 
from translation import str_range_to_eng,str_range_to_th
import pickle


openai_api_key = os.getenv('OPENAI_API_KEY', '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')
llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name='gpt-3.5-turbo')

def get_result(jd,pickle_name,results_list,directory):

    template = """
                Write an analysis about the information in the RESUME whether it is consistent or suitable for How many job qualifications in the JOBDESCRIPTION? And try to evaluate the suitability for the job between RESUME and JOBDESCRIPTION by scoring from 1-10. 

                % START OF JOBDESCRIPTION
                {jobdescription}
                % END OF JOBDESCRIPTION

                % START OF RESUME
                {resume}
                % END OF RESUME

                % RESPONSE FORMAT:
                - Respond in under 700 characters
                - if the RESUME does not match the JOBDESCRIPTION, reply that it does not match.


                YOUR ANALYZE: """
    prompt = PromptTemplate(
    input_variables=["jobdescription","resume"],
    template=template)

    jd = str_range_to_eng(jd)
    result_txt = ''   
    with open("./data_cach/"+ pickle_name, "rb") as fp: 
        data = pickle.load(fp)
    resume_select = []
    for i in results_list[1][0]:
        resume_select.append(data[i])
    for i,j in enumerate(resume_select):
        ref = data[results_list[1][0][i]].split('\*/')[-1].split('/')[-1].split(directory)[1]
        final_prompt = prompt.format(jobdescription=jd,resume=j)
        output = llm.predict(final_prompt)
        result_txt += ''"\n\n"+ref+"\n"
        result_txt +=output
    return str_range_to_th(result_txt)