import gradio as gr
import openai
import os
import sys

try:
  openai.api_key = os.environ['OPENAI_API_KEY']
except KeyError:
  sys.stderr.write("""
  Hello! To get started, you will first need to enter your OpenAI API key. Please follow the instructions below:
  
  If you don't have an API key yet, visit:
  
  https://platform.openai.com/signup

  1. Make an account or sign in
  2. Click "View API Keys" from the top right menu.
  3. Click "Create new secret key"

  Then, open the Secrets Tool and add OPENAI_API_KEY into 'key' and your key into 'value'. This will save it as a Secret and you will be able to run this code and keep your API key safe.
  """)
  exit(1)

message_history = [{
  "role":
  "user",
  "content":
  f"You are a medical AI symptom intake chatbot. You will take a brief patient review of systems and then classify their symptoms as grades 1-4 according to the “Common Terminology Criteria for Adverse Events” (CTCAE) “Cancer Therapy Evaluation Protocol” (CTEP) guidelines which you have been trained on. Your tone will be conversational and you will chat with patients in a question-and-response format. You will ask one question at a time, followed by your next question. You will ask a brief review of systems. Any positive findings you will further investigate and classify based on your knowledge of the CTCAE CTEP guidelines. Here are some example symptoms and their corresponding CTCAE grades. Patient symptoms: The patient is dead. CTCAE grade: 5. Patient symptoms: Mild chest pain, intervention not indicated. CTCAE grade: 1. Patient symptoms: Anal hemorrhage with transfusion indicated, invasive intervention indicated, hospitalization. CTCAE grade: 3. Patient symptoms: Abdominal pain, moderate, limiting instrumental ADL. CTCAE grade: 2. Patient symptoms: Urinary Obstruction, life-threatening consequences, organ failure, urgent operative intervention indicated. CTCAE grade: 4. You will politely decline any requests to answer questions outside of your medical purview."
}, {
  "role": "assistant",
  "content": f"OK"
}]


def predict(input):
  # tokenize the new input sentence
  message_history.append({"role": "user", "content": f"{input}"})

  completion = openai.ChatCompletion.create(model="gpt-4",
                                            messages=message_history)
  #Just the reply:
  reply_content = completion.choices[
    0].message.content  #.replace('```python', '<pre>').replace('```', '</pre>')

  print(reply_content)
  message_history.append({"role": "assistant", "content": f"{reply_content}"})

  # get pairs of msg["content"] from message history, skipping the pre-prompt:              here.
  response = [
    (message_history[i]["content"], message_history[i + 1]["content"])
    for i in range(2,
                   len(message_history) - 1, 2)
  ]  # convert to tuples of list
  return response


# creates a new Blocks app and assigns it to the variable demo.
with gr.Blocks() as demo:
  gr.Markdown("""
    # Patient Symptom Intake and CTCAE Grader Chatbot v1.0
    Please start by typing "Hello" into the chat.
    """)
  # creates a new Chatbot instance and assigns it to the variable chatbot.
  chatbot = gr.Chatbot(label="Cancer Sx Chatbot")

  # creates a new Row component, which is a container for other components.
  with gr.Row():
    '''creates a new Textbox component, which is used to collect user input. 
        The show_label parameter is set to False to hide the label, 
        and the placeholder parameter is set'''
    txt = gr.Textbox(
      show_label=False,
      placeholder="Enter text and press enter").style(container=False)
  '''
    sets the submit action of the Textbox to the predict function, 
    which takes the input from the Textbox, the chatbot instance, 
    and the state instance as arguments. 
    This function processes the input and generates a response from the chatbot, 
    which is displayed in the output area.'''
  txt.submit(predict, txt, chatbot)  # submit(function, input, output)
  #txt.submit(lambda :"", None, txt)  #Sets submit action to lambda function that returns empty string
  '''
    sets the submit action of the Textbox to a JavaScript function that returns an empty string. 
    This line is equivalent to the commented out line above, but uses a different implementation. 
    The _js parameter is used to pass a JavaScript function to the submit method.'''
  txt.submit(
    None, None, txt, _js="() => {''}"
  )  # No function, no input to that function, submit action to textbox is a js function that returns empty string, so it clears immediately.

demo.launch(share=True)
