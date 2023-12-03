from tkinter.ttk import Combobox
from tkinter import Tk, Button, filedialog, messagebox, Label, Menu
from PIL import ImageGrab
from cv2 import VideoWriter, VideoWriter_fourcc, cvtColor, resize, COLOR_BGR2RGB
from ctypes import windll
import time
import numpy as np




''' Application version '''
__version__='1.0'

''' Application Name '''
app_name = 'RHS_Recorder'

''' About Information '''
about_msg='''
    App name: '''+app_name+'''
    
'''

''' Contact Details '''
contact_us='''
    Email: jainrocky1008@gmail.com
    github: jainrocky
'''

''' Waiting time for Tk.after function '''
call_record_after = 2

''' Application Window Size(Constant or non resizable) '''
app_window_size='640x240'

''' Video resolution '''
video_res = (1280, 720)

''' stop text '''
btn_close_txt='Stop'

''' exit text '''
btn_exit_txt='Exit'

''' close button width '''
btn_close_width=20

''' start text '''
btn_start_txt='Record'

''' start button width '''
btn_start_width=20

''' opencv codec '''
codec='mp4v'



class WindowRecorder:
    def __init__(self):
        self.__app = Tk()
        self.__app.title(app_name)
        self.__app.geometry(app_window_size)
        self.__app.resizable(0, 0)
        self.__is_recording=False

    '''
        CREATING CONTEXT OR FORM  with two buttons one menu having three
        items one label for timer and one combobox for fps selection
    '''
    def create_context(self):
        self.__btn_start_stop = Button(self.__app, text=btn_start_txt, width=btn_start_width, command=self.start_recording, bg='green', fg='white', bd=0)
        self.__btn_start_stop.pack(pady=10)
        
        self.__btn_exit=Button(self.__app, text=btn_exit_txt, width=btn_close_width, command=self.destroy, fg='white', bg='blue', bd=0)
        self.__btn_exit.pack()

        ''' Timer label '''
        self.__timer=Label(text='00:00:00')
        self.__timer.pack(side='left', padx=5)

        self.__saving_label=Label(text='')
        self.__saving_label.pack(side='right', padx=5)
        
        ''' Root Menu '''
        self.__root_menu = Menu(master=self.__app)
        self.__app.config(menu=self.__root_menu)

        ''' File Menu '''
        self.__file_menu = Menu(self.__root_menu, tearoff=0)
        self.__file_menu.add_command(label='About', command=self.about)
        self.__file_menu.add_command(label='Contact us', command=self.contact_us)
        self.__file_menu.add_separator()
        self.__file_menu.add_command(label='Exit', command=self.destroy)

        self.__root_menu.add_cascade(label='Menu', menu=self.__file_menu)


    ''' Start application '''        
    def start(self):
        self.__app.mainloop()

    ''' Start recording '''
    def start_recording(self):
        self.time=time.time()
        self.__is_recording=True
        self.__temp_video_frames = list()
        self.__btn_start_stop.configure(text=btn_close_txt, command=self.stop, bg='red')
        self.__saving_label['text']=''
        self.__timer['text']='00:00:00'
        self.__app.iconify()
        self.record_frames()
        
    ''' Stop screen recording '''
    def stop(self):
        if self.__job is not None:
            self.__app.after_cancel(self.__job)
            self.__job=None
            
        self.time =int(time.time()-self.time)
        total_frame=len(self.__temp_video_frames)
        self.__timer['text']=time.strftime('%H:%M:%S', time.gmtime(self.time))
        self.__app.update()
        print('total time: {}'.format(self.time))
        print('total frame: {}'.format(total_frame))
        self.__is_recording=False
        file = filedialog.asksaveasfile(defaultextension="*.*", filetypes=[('mp4', '.mp4'),])
        if file:
            if file.name:
                fourcc = VideoWriter_fourcc(*codec)
                video_writer = VideoWriter(file.name, fourcc, total_frame//self.time, video_res, True)
                if self.__temp_video_frames:
                    for i, frame in enumerate(self.__temp_video_frames):
                        frame=np.array(frame)
                        frame = cvtColor(frame, COLOR_BGR2RGB)
                        frame = resize(frame, video_res)
                        video_writer.write(frame)
                        self.__saving_label['text']='{:.2f}% Complete'.format( ((i+1)/total_frame)*100 )
                        self.__app.update()
                    print('writing frame complete...')
                    del self.__temp_video_frames
                video_writer.release()
        self.__btn_start_stop.configure(text=btn_start_txt, command=self.start_recording, bg='green')


    ''' Close application '''
    def destroy(self):
        self.__app.destroy()

    ''' Extracting list of frames '''
    def record_frames(self):
        self.__temp_video_frames.append(ImageGrab.grab())
        self.__timer['text']=time.strftime('%H:%M:%S', time.gmtime(time.time()-self.time))
        if self.__is_recording:
            self.__job=self.__app.after(call_record_after, self.record_frames)

    ''' Contact us information '''
    def contact_us(self):
        messagebox.showinfo('Contact us', contact_us)

    ''' About details'''
    def about(self):
        messagebox.showinfo('About', about_msg)
        

if __name__=='__main__':
    ''' Fixing ImageGarb bug(i.e, not cropping full screen) '''
    user_32=windll.user32
    user_32.SetProcessDPIAware()

    ''' App Call '''
    app=WindowRecorder()
    app.create_context()
    app.start()
