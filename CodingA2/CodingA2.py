#Import relevant modules
import tkinter as tk
import random
from itertools import count
#External library Pillow for image handling: Python Software Foundation. (2025). Pillow (Version 11.3.0) [Computer software]. https://python-pillow.github.io/ 
from PIL import Image, ImageTk


#GIF animation setup from: PythonProgramming. (2021, February 19). Animate gif in tkinter [Code tutorial]. https://pythonprogramming.altervista.org/animate-gif-in-tkinter/
#Create class for Gif animation
class ImageLabel(tk.Label):
    def load(self, im): #Define function to load the Gif
        if isinstance(im, str): #Check if the input is a file path string
            im = Image.open(im) #Open the image file

        frames = [] #Create a list to store the frames of the Gif
        try:
            for i in count(0): #Loop through each frame of the Gif
                frames.append(ImageTk.PhotoImage(im.copy())) #Convert each frame to a PhotoImage and add it to the frames list
                im.seek(i) #Move to the next frame
        except EOFError:
            pass #Stop when there are no more frames

        self.frames = frames #Store frames in the object
        self.delay = im.info.get('duration', 100) #Set delay time between frames 
        self.next_frame(0) #Start playing the GIF from the first frame

    #Define function to display frames in sequence
    def next_frame(self, frame_index=0):
        current_image = self.frames[frame_index] #Get the current frame
        self.config(image=current_image) #Set the label to display the current frame
        frame_index += 1 #Move to the next frame
        if frame_index < len(self.frames): #If there are more frames
            self.after(self.delay, self.next_frame, frame_index) #Schedule the next frame to be displayed after the delay

    #Define function to stop and clear the Gif
    def unload(self):
        self.config(image=None) #Clear the image from the label
        self.frames = None #Clear the frames


#Create interface
interface = tk.Tk()
#Set the title of the interface
interface.title("Motivational To-Do List")
#Set the size for the interface
interface.geometry("400x575")
#Set the background colour for the interface
interface.config(bg="white")

#Add title to the interface
title_label = tk.Label(
    interface,
    text="Today's To-Do List!",
    font=("Balham", 28),
    bg="white",
    fg="#FF6991"
)
#Set title at the top centre of the interface
title_label.pack(pady=20)

#Add text box for user entry for checklist
task_entry = tk.Entry(interface, font=("Gravity-Book", 14), bg="white", highlightbackground="white")
task_entry.pack(pady=5)

#Create button to add task
add_button = tk.Button(
    interface,
    text="ADD TASK",
    font=("Helvetica", 14),
    bg="white",
    fg="#FF6991",
    highlightbackground="white",
    activebackground="white"
)
add_button.pack(pady=5)


#Scrollable frame setup from: GeeksforGeeks. (2025, July 23). How to add a scrollbar to a group of widgets in Tkinter [Code tutorial]. https://www.geeksforgeeks.org/python/how-to-add-a-scrollbar-to-a-group-of-widgets-in-tkinter/
#Create a canvas widget within main interface
canvas = tk.Canvas(interface, bg="white", highlightthickness=0)
#Create a vertical scrollbar linked to the interface
scrollbar = tk.Scrollbar(interface, orient="vertical", command=canvas.yview)
#Create a frame to contain the scrollable list
scrollable_frame = tk.Frame(canvas, bg="white")

#Bind the function to update the scrollregion of the canvas when the size of the scrollable frame changes
scrollable_frame.bind(
    "<Configure>", 
    lambda e: canvas.configure(scrollregion=canvas.bbox("all")) #Update scrollregion
)

#Add the scrollable frame to the canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#Configure the canvas to use the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

#Pack the canvas to the left side of the interface and allow it to expand
canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
#Pack the scrollbar to the right side of the interface and fill vertically
scrollbar.pack(side="right", fill="y")


#Create list to store all checkboxes
checkboxes = []
#Create global variable to track if first task completed
first_task_done = False
#Create global variable to store reference to Finish All button
finish_button = None

#Create list of motivational quotes for the completion of the first task
first_quote = [
    "First one done, you've got this!",
    "Great start, keep going!",
    "First one done, the hardest part is over!",
    "First step done, keep it up!",
    "Amazing work, keep the momentum going!",
    "Starting strong sets the pace for today!",
    "You've begun and that's half the battle!",
    "Your day is off to a fantastic start!"
]

#Create list of motivational quotes for the completion of subsequent tasks
other_quotes = [
    "Another task down, you're unstoppable!",
    "Another one done, you're on fire!",
    "You're making amazing progress!",
    "Keep it up, you're doing fantastic!",
    "Another step closer to your goals!",
    "You're crushing it, keep going!",
    "Keep smashing those tasks!",
    "You're unstoppable, keep it up!"
]

#Create list of motivational quotes for finishing all tasks
finish_all_quotes = [
    "Great work, all tasks cleared!",
    "All tasks done, time to relax!",
    "You've cleared everything, well done!",
    "All tasks completed, fantastic job!",
    "All done, you should feel proud!",
    "What a productive day, good job!",
    "You crushed it today, well done!",
    "Amazing work, see you next time!"
]


#Define function to show confetti overlay
def show_confetti_overlay(quote_text):
    overlay = tk.Frame(interface, bg='white') #Create overlay frame
    overlay.place(x=0, y=0, relwidth=1, relheight=1) #Make overlay cover entire interface

    gif_label = ImageLabel(overlay) #Create label to display Gif
    gif_label.pack(expand=True) #Let GIF label expand to fill overlay
    gif_label.load("confetti6.gif") #Load and play the confetti Gif

    #Create and place motivational quote label
    quote_label = tk.Label(
        overlay,
        text=quote_text,
        font=("Balham", 20, "bold"),
        bg='white',
        fg="#FF6991"
    )
    quote_label.place(relx=0.5, rely=0.1, anchor='n')

    #Define function to remove overlay 
    def remove_overlay():
        gif_label.unload() #Stop and clear the Gif
        overlay.destroy() #Remove the overlay frame

    #Remove overlay after 3 seconds
    interface.after(3000, remove_overlay)

#Define function to show confetti and quote when a task is completed
def show_confetti():
    global first_task_done #Access global variable to track if first task completed

    if not first_task_done: #If this is the first task completed
        quote = random.choice(first_quote) #Randomly select a quote from the first task quotes
        first_task_done = True #Set first task completed to True
    else:
        quote = random.choice(other_quotes) #Randomly select a quote from the other task quotes
    show_confetti_overlay(quote) #Show confetti overlay with the selected quote


#Define function to clear all tasks
def finish_all():
    global finish_button, first_task_done #Access global variables

    for cb in checkboxes:
        cb.destroy() #Destroy each checkbox
    checkboxes.clear() #Clear the list of checkboxes
    first_task_done = False #Reset first task completed to False

    if finish_button:
        finish_button.destroy() #Remove the Finish All button
        finish_button = None #Reset Finish All button reference

    quote = random.choice(finish_all_quotes) #Choose a random quote from the finish all quotes
    show_confetti_overlay(quote) #Show confetti overlay with a finish all quotes quote

#Define function to add task to checklist
def add_task(event=None):
    global finish_button, checkboxes #Access global variables

    task_text = task_entry.get() #Get text from the entry box
    if not task_text: 
        return #Ignore empty task entries

    #Create variable to check if checkbox is checked
    var = tk.IntVar()

    #Define function that runs when checkbox is checked
    def checkbox_command():
        if var.get(): #If checkbox is checked
            show_confetti() 

    #Create the checkbox
    cb = tk.Checkbutton(
        scrollable_frame,
        text=task_text,
        font=("Gravity-Book", 18),
        variable=var,
        command=checkbox_command,
        bg="white",
        activebackground="white"
    )
    cb.pack(anchor="w", pady=2)

    #Add checkbox to the list of checkboxes
    checkboxes.append(cb)
    #Clear the entry box
    task_entry.delete(0, tk.END)

    #If the clear button is not already displayed, create and display it
    if finish_button is None:
        finish_button = tk.Button(
            interface,
            text="FINISH ALL",
            font=("Gravity-Book", 10),
            bg="white",
            fg="#FF6991",
            highlightbackground="white",
            activebackground="white",
            command=finish_all
        )
        finish_button.pack(side="bottom", pady=10)


#Link the add task function to the button and Enter key
add_button.config(command=add_task)
interface.bind("<Return>", add_task)

#Run
interface.mainloop()