#Import tkinter library
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import font as tkFont
from tkinter import messagebox, ttk

def listen():
    text_area.insert(END, f"Listening.....\n")
    
    if receive_inputVoice():
        user_input: str = getLatestQuestion()

        text_area.insert(END, f"You : {user_input}\n")

        text_area.insert(END, f"Processing.....\n")

        # user request to end the section 
        if checklistExistInString(user_input.lower(), end_section):
            
            # ask for confirm 
            qres = f"{currentbot}: Confirm to end this section?"
            text_area.insert(END, qres + "\n")
            process_response(qres)
            
            # receive input 
            if receive_inputVoice():
                yn = getLatestQuestion()
                if "yes" in yn.lower() or "ya" in yn.lower():
                    # say yes
                    res = "Okay, bye"
                    setResponse(res)
                    text_area.insert(END, f"{currentbot} : {res} + "\n")
                    generate_sound(res)

                elif "no" in yn.lower():
                    # say no
                    res = "Nice! Let's keep talking"


                text_area.insert(END, f"{currentbot} : {res} + "\n")
                process_response(res)


                # search best match inside json file 
        best_match: str | None = find_best_match(user_input, [q['question'] for q in knowledge_base['questions']])

                # ----------------------------------------------
        text_area.insert(END, f"You : {user_input}")
        # print(user_input)

        if best_match:
            # found best match - use knowledge based to response
            answer: str = get_answer_for_question(best_match, knowledge_base)
            
            ## display at nested screen
            process_response(answer)
            text_area.insert(END, f"{currentbot} : {answer}")

        elif isSearch(user_input):
            # request to searching
            query = getQuery(user_input)
        else:
            # let machine to make a response 
            answer = provide_response(user_input, currentbot)
            process_response(answer)
            text_area.insert(END, f"{currentbot} : {answer}")
    else:
        # got problem and come here - NOT_CLEAR, NOT_UNDERSTAND, ERROR....
        process_response(getLatestResponse())
        text_area.insert(END, f"You : {getLatestQuestion()}")
        text_area.insert(END, f"{currentbot} : {answer}")

### Main Window Setting
mainWin= Tk()

#Set the geometry of tkinter frame
mainWin.geometry("750x250")
mainWin.resizable(False, False)

# ------------------------- combo ------------------------- 
selection = MISTRAL # default selection

def selection_changed(event):
    global selection
    selection = combo.get()
    messagebox.showinfo(
        title="New Selection",
        message=f"Selected option: {selection}"
    )
     
combo = ttk.Combobox(
    state="readonly",
    values=[ MISTRAL, GPT, DIALO ]
)
combo.set(MISTRAL) # set default
combo.place(x=50, y=50)
combo.bind("<<ComboboxSelected>>", selection_changed) # event

# ------------------------- button ------------------------- 
micBtn = ttk.Button(mainWin, text="Mic", command=lambda: listen())
micBtn.place(x=10, y=20)

mainWin.bind('<Return>',lambda event:callback())
    
# ------------------------- text ------------------------- 
# Create the chatbot's text area
text_area = Text(mainWin, bg="white", width=50, height=20)
text_area.pack()
    
    ## looping start and receive input ....
    # open the file
knowledge_base: dict = load_knowledge_base(knowledge_path)
    
    # store model use into json
updateCurrentServebot(knowledge_path, knowledge_base)
currentbot = getCurrentServebot(knowledge_base)



    # Display the response in the chatbot's text area
    # if sucessful get input 




mainWin.mainloop()