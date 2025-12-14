
from langchain_groq import ChatGroq
from langchain.chains.llm import LLMChain
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from flask import Flask,request,jsonify
import os
import ast

app = Flask(__name__)

@app.route("/form_generation", methods = ["POST"])
def form_generation():

  data = request.json

  role = data["role"]
  experience=data["experience"]
  section= data["sections"]
  load_dotenv()
  a=os.getenv("API_KEY")
  
  llm = ChatGroq(
      model="llama-3.1-8b-instant",  
      api_key=a,
      temperature=1
  )

  feedback_prompt = ChatPromptTemplate.from_template("""
  You are an expert HR system helping to generate structured 360-degree performance feedback forms.
  
  Generate a performance feedback form as a **strict JSON object** using the following inputs:
  - Role: {role}
  - Experience: {experience}
  - Sections: A list of default section keys in snake_case format
    (e.g., "core_performance_areas","team_collaboration","behavioral_cultural_fit")
  
  ### INSTRUCTIONS ###
  
  1. Output **only** a JSON object with this exact structure:
  {{{{  
    "employee_information": {{{{  
      "role": string,
      "experience": string
    }}}},
    "feedback_sections": {{{{  
      "section_key_1": {{{{  
        "questions": [
          {{{{ "question_1": string }}}},
          {{{{ "question_2": string }}}},
          {{{{ "question_3": string }}}},
          {{{{ "question_4": string }}}},
          {{{{ "question_5": string }}}}
        ]
      }}}},
      ...
    }}}},
    "open_ended_feedback": {{{{  
      "areas_for_improvement": "",
      "strengths": "",
      "suggestions_for_growth": ""
    }}}}
  }}}}
  
  2. For each section:
    - Generate 5 specific, observable, rateable questions with numbered keys.
  
  3. Add exactly 2 relevant extra sections for the role.
  
  ### STRICT RULES ###
  - Return ONLY valid parsable JSON.
  - NO markdown, NO comments, NO extra text.
  - Use only double quotes.
  - Use colons for key-value pairs and commas for separation.
  
  ### BEGIN ###76 A;L'
  Role: {role}
  Experience: {experience}
  Sections: {default_sections}
  """)

  
  chain = LLMChain(llm=llm, prompt=feedback_prompt)
  
  response = chain.invoke({"role":role,"experience":experience,"default_sections":section})


  return jsonify(response)



if __name__ == '__main__':
  app.run(debug=True)