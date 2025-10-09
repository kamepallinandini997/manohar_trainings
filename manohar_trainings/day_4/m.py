from langchain_google_genai import ChatGoogleGenerativeAI
 
from langchain_core.messages import HumanMessage
 
from langchain_community.document_loaders import PyPDFLoader
 
pdf_path=PyPDFLoader("BajiBabu_Resume.pdf")=
 
load_pdf=pdf_path.load()
 
pdf_text="\n".join([page.page_content for page in load_pdf])
 
llm=ChatGoogleGenerativeAI(model="gemini-2.5-pro",api_key="AIzaSyA-SsBef1O30YyaHmG6jigNjnTX2raliqA")
 
res=HumanMessage(
    content={f"give me the summarization for the given pdf {pdf_text}"}
)
ans=llm.invoke([res])
print(ans.content)