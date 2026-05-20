from tkinter import *
import customtkinter
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
from PIL import Image, ImageTk
import tkinter
import os

#Init root and info
root = customtkinter.CTk()
root.title('Music Player')
root.geometry('920x450')
root.resizable(width=FALSE, height=FALSE)
#setting the appearance to system
customtkinter.set_appearance_mode('system')
#setting default color theme for whole app
customtkinter.set_default_color_theme('blue')

#Init pygame mixer
pygame.mixer.init()

#-------Add and Delete Song Function-------

#add song function
def add_song():
    song = filedialog.askopenfilename(initialdir='music/', title='Chose A Song', filetypes=(("mp3 Files", "*.mp3"), ))
    #strip out directory and extension from song name
    song = song.replace("/Users/manit/Documents2/musicplayer-main/music/", "")
    song = song.replace(".mp3", "")

    #adding song to listbox
    song_box.insert(END, song)

#add many songs to playlist
def add_many_song():
    songs = filedialog.askopenfilenames(initialdir='music/', title='Chose A Song', filetypes=(("mp3 Files", "*.mp3"), ))
    #loop through the songs to strip names
    for song in songs:
        #strip each song in the playlist
        song = song.replace("/Users/manit/Documents2/musicplayer-main/music/", "")
        song = song.replace(".mp3", "")
        #adding song to listbox
        song_box.insert(END, song)

#delete a song
def delete_song():
    stop()
    #delete selected song
    song_box.delete(ANCHOR)
    #stop playing song deleted
    pygame.mixer.music.stop()

    #clear album image
    remove_album_cover()

#delete all song
def delete_all_songs():
    stop()
    #delete all songs
    song_box.delete(0,END)
    #stop music if song deleted
    pygame.mixer.music.stop()
    #clear album image
    remove_album_cover()

#------------------------------------------

#------Save and Load Song Functions--------

#save and delete songs 
def sd_songs_to_file():
    if save_switch.get()==1:
        songs = song_box.get(0, END)
        with open('selected_songs.txt', 'w') as file:
            for song in songs:
                file.write(song + '\n')
    else:
        with open('selected_songs.txt', 'w') as file:
            pass

#load songs if save switch on when closing app
def load_songs_from_file():
    try:
        with open('selected_songs.txt', 'r') as file:
            songs = file.readlines()
            for song in songs:
                song = song.strip()  # Remove newline characters
                song_box.insert(END, song)
                save_switch.select()
    except FileNotFoundError:
        pass  # If the file doesn't exist yet, continue without loading songs

#if pressed shift esc when save switch true delete all song and delete song which are saved
root.bind('<Shift-Escape>', lambda event: delete_all_songs_saved() if save_switch.get() == 1 else sd_songs_to_file())

#delete all song and set save switch to false
def delete_all_songs_saved():
    stop()
    #delete all songs
    song_box.delete(0,END)
    #stop music if song deleted
    pygame.mixer.music.stop()
    #clear album image
    remove_album_cover()
    #switch the song save swicth to false
    save_switch.toggle()

#------------------------------------------

#------Function to calculate the time song at and song length--------
#song length time info
def play_time():
    #check for 2 loop for play_time
    global stopped
    if stopped:
        return
    #curent song time
    current_time = pygame.mixer.music.get_pos()/1000
    #conver to time format using time
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    #get the current song tuple number
    song = song_box.get(ACTIVE)
    #song title
    song = f'/Users/manit/Documents2/musicplayer-main/music/{song}.mp3'
    #load song with mutagen
    song_mut = MP3(song)
    #get song length with mutagen
    global song_length
    song_length = song_mut.info.length
    #convert to time format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    #increase current time by 1s
    current_time+=1
    if int(my_slider.get()) == int(song_length):
        statu_bar.config(text=f'{converted_song_length}/{converted_song_length}')
        if switch.get()==1:
            next_song()
    elif paused:
        pass
    elif(int(my_slider.get()) == int(current_time)):
        #update slider to position
        slider_position = int(song_length)
        my_slider.configure(to=slider_position)
        my_slider.set(int(current_time))
    else:
        #update slider to position
        slider_position = int(song_length)
        my_slider.configure(to=slider_position)
        my_slider.set(int(my_slider.get()))
        #conver to time format using time
        converted_current_time = time.strftime('%M:%S', time.gmtime(my_slider.get()))
        #output time to status bar
        statu_bar.config(text=f'{converted_current_time}/{converted_song_length}')

        #move sldier along by 1s
        next_time = int(my_slider.get())+1
        my_slider.set(next_time)
    #update time
    statu_bar.after(1000, play_time)

#------------------------------------------

#---Function to get and remove album cover---
def get_album_cover():
    image_current_path=song_box.get(ACTIVE)
    image_current_path=f'/Users/manit/Documents2/musicplayer-main/img/{image_current_path}.jpg'
    image1 = Image.open(image_current_path)
    image2=image1.resize((170, 170))
    global load
    load = ImageTk.PhotoImage(image2)
    label1.configure(image=load)
    label1.grid(row=0, column=0)

def remove_album_cover():
    image_current_path=f'/Users/manit/Documents2/musicplayer-main/img/Transparent.png'
    image1 = Image.open(image_current_path)
    image2=image1.resize((170, 170))
    load = ImageTk.PhotoImage(image2)
    label1.configure(image=load)
    label1.image=load

#------------------------------------------

#-----------Playing Control Start-----------
#play select song
def play():
    #set stop var to false
    global stopped
    stopped = False
    statu_bar.config(text='')
    my_slider.set(0)
    song = song_box.get(ACTIVE)
    song = f'/Users/manit/Documents2/musicplayer-main/music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #call the paly_time fn to get current time
    play_time()
    get_album_cover()

#stop playing current song
global stopped
stopped = False
def stop():
    #reset slider and status bar
    statu_bar.config(text='')
    my_slider.set(0)
    #stop song from playing
    pygame.mixer.music.stop()
    song_box.select_clear(ACTIVE)

    #clear ststus bar
    statu_bar.config(text='')

    #set stop variable to true
    global stopped
    stopped = True

    remove_album_cover()

#play next song in playlist
def next_song():
    #reset slider and status bar
    statu_bar.config(text='')
    my_slider.set(0)
    #get the current song tuple number
    next_one = song_box.curselection()
    #add one to next song no
    next_one = next_one[0]+1
    
    #check if auto play is set to true
    if (switch.get()==1 and next_one == song_box.size()):
        next_one = 0
        song = song_box.get(next_one)
        #song title
        song = f'/Users/manit/Documents2/musicplayer-main/music/{song}.mp3'
        #load and play song
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        #clear active song in frame
        song_box.selection_clear(0,END)

        #activate next song in frame
        song_box.activate(next_one)

        #set active bar to next song
        song_box.selection_set(next_one, last=None)

        get_album_cover()
    else:
        song = song_box.get(next_one)
        #song title
        song = f'/Users/manit/Documents2/musicplayer-main/music/{song}.mp3'
        #load and play song
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        #clear active song in frame
        song_box.selection_clear(0,END)

        #activate next song in frame
        song_box.activate(next_one)

        #set active bar to next song
        song_box.selection_set(next_one, last=None)
        get_album_cover()

#play previous song in playlist
def previous_song():
    #reset slider and status bar
    statu_bar.config(text='')
    my_slider.set(0)
    #get the current song tuple number
    next_one = song_box.curselection()
    
    #add one to next song no
    next_one = next_one[0]-1

    song = song_box.get(next_one)
    #song title
    song = f'/Users/manit/Documents2/musicplayer-main/music/{song}.mp3'
    #load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #clear active song in frame
    song_box.selection_clear(0,END)

    #activate next song in frame
    song_box.activate(next_one)

    #set active bar to next song
    song_box.selection_set(next_one, last=None)
    get_album_cover()

#global var to check wethere song paused or not
global paused
paused = False

#pause and iunpauase current song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        #unpause
        pygame.mixer.music.unpause()
        paused=False
    else: 
        #pause
        pygame.mixer.music.pause()
        paused=True
    
#slider function
def slide(x):
    song = song_box.get(ACTIVE)
    song = f'/Users/manit/Documents2/musicplayer-main/music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

#create volume function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

#----------End of Playing Control------------

#----------Defining the Widgets--------------

#create master frame
master_frame = customtkinter.CTkFrame(master=root)
master_frame.pack(pady=20)

#creating playlistbox
song_box = Listbox(master_frame, bg='#aab0b5', fg='black', width=60)
song_box.grid(row=0, column=0, pady=20,padx=20)

#create palyer control frames
controls_frame = customtkinter.CTkFrame(master=master_frame,width=350, height=200, fg_color='transparent')
controls_frame.grid(row=1, column=0, pady=20, padx=10)

#create volume label frame
volume_frame= customtkinter.CTkFrame(master=master_frame, fg_color='transparent')
volume_frame.grid(row=0, column=1,padx=(0,10),pady=10)

#create volume label frame
album_frame= customtkinter.CTkFrame(master=master_frame, width=175, height=170, bg_color='#aab0b5', fg_color='#aab0b5')
album_frame.grid(row=0, column=2,padx=(0,10),pady=10)

# Define Player Control Button Images using Pillow
back_btn_img = customtkinter.CTkImage(light_image=Image.open('images/back50.png'),dark_image=Image.open('images/back50.png'),size=(50,50))
forward_btn_img =  customtkinter.CTkImage(light_image=Image.open('images/forward50.png'),dark_image=Image.open('images/forward50.png'),size=(50,50))
play_btn_img = customtkinter.CTkImage(light_image=Image.open('images/play50.png'),dark_image=Image.open('images/play50.png'),size=(50,50))
pause_btn_img =  customtkinter.CTkImage(light_image=Image.open('images/pause50.png'),dark_image=Image.open('images/pause50.png'),size=(50,50))
stop_btn_img =  customtkinter.CTkImage(light_image=Image.open('images/stop50.png'),dark_image=Image.open('images/stop50.png'),size=(50,50))

#create Player control buttons
back_button =  customtkinter.CTkButton(controls_frame, text='',border_width=0,width=70, command=previous_song,image=back_btn_img,fg_color='transparent')
back_button.grid(row=0, column=0)

forward_button = customtkinter.CTkButton(controls_frame, text='', border_width=0, width=70, command=next_song,image=forward_btn_img,fg_color='transparent')
forward_button.grid(row=0, column=1, padx=10)

play_button = customtkinter.CTkButton(controls_frame, text='',border_width=0,width=70,command=play,image=play_btn_img,fg_color='transparent')
play_button.grid(row=0, column=2,padx=10)

pause_buttton = customtkinter.CTkButton(controls_frame, text='',border_width=0,width=70, command=lambda:pause(paused),image=pause_btn_img,fg_color='transparent')
pause_buttton.grid(row=0, column=3,padx=10)

stop_button = customtkinter.CTkButton(controls_frame, text='',border_width=0, width=70, command=stop,image=stop_btn_img,fg_color='transparent')
stop_button.grid(row=0, column=4)

#switch for autoplay
switch = customtkinter.CTkSwitch(master_frame, text="Autoplay", onvalue=True, offvalue=False)
switch.grid(row=1, column=1)

#switch to save the songs in song box
save_switch = customtkinter.CTkSwitch(master_frame, text="Save Playlist", onvalue=True, offvalue=False, command=sd_songs_to_file)
save_switch.grid(row=2, column=1, pady=(0,20))

#create menu
my_menu = Menu(root, background='#1f6aa5', fg='#ffffff') 
root.config(menu=my_menu)

#add Sond menu
add_song_menu = Menu(my_menu,bg="#1f6aa5", fg="#ffffff")
my_menu.add_cascade(label='Add Songs', menu=add_song_menu)
add_song_menu.add_command(label='Add one song to playlist', command=add_song)

#add many songs
add_song_menu.add_command(label='Add Many song to playlist', command=add_many_song)

#crete delete song menu
remove_song_menu = Menu(my_menu,bg="#1f6aa5", fg="#ffffff")
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song from playlist", command=delete_song)
remove_song_menu.add_command(label="Delete all song from playlist", command=delete_all_songs)

#create status bar
statu_bar = Label(root, text='', anchor=E, bg='#1f6aa5', fg="#ffffff")
statu_bar.pack(fill=X, side=BOTTOM, ipady=2)

#create music slider
my_slider = customtkinter.CTkSlider(master_frame, from_=0, to=100, orientation=HORIZONTAL, command=slide, width=360,fg_color='#4c4c4c')
my_slider.set(0)
my_slider.grid(row=2, column=0, pady=10)

#create volume slider
volume_slider = customtkinter.CTkSlider(volume_frame, from_=0, to=1, orientation=VERTICAL, command=volume, height=120,fg_color='#4c4c4c')
volume_slider.set(1)
volume_slider.pack()

#label for album frame
label1 = tkinter.Label(album_frame)

#------------------------------------------


#call to load file if the save was true when the app closed
load_songs_from_file()

root.mainloop()