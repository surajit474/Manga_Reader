import threading
import tkinter as tk

import customtkinter as ctk
import requests
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1100x800")
        self.resizable(False, False)

        self.t1 = threading.Thread(target=self.image_genaretor, daemon=True)
        self.t1.start()
        self.layout()


    def layout(self):
        # frame=ctk.CTkFrame(self)
        # frame.pack(expand=True,fill="both")
        # self.canvas = tk.Canvas(
        #     frame,
        #     background="red",
        #     scrollregion=(0, 0, frame.winfo_width(),1500),
        # )
        # Frames
        self.frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.frame.bind_all(
            "<Button-4>",
            lambda event: self.frame._parent_canvas.yview_scroll(
                int(-event.num / 1.5), "units"
            ),
        )
        self.frame.bind_all(
            "<Button-5>",
            lambda event: self.frame._parent_canvas.yview_scroll(
                int(event.num / 1.5), "units"
            ),
        )
        #upper frame widget
        self.upper_frame = ctk.CTkFrame(self.frame,fg_color="transparent")
        entry_string=ctk.StringVar()
        ctk.CTkEntry(self.upper_frame,textvariable=entry_string)
        ctk.CTkButton(self.upper_frame,text='search').place(relx=0.7,rely=0.05)


        # scrollabl_frame=ctk.CTkScrollableFrame(self,width=200,height=700,fg_color='black')
        self.frame.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="a")
        self.frame.rowconfigure(0, weight=1, uniform="b")
        self.frame.rowconfigure((1, 2, 3, 4, 5), weight=2, uniform="b")
        for i in range(1, 6):
            for j in range(5):
                ctk.CTkLabel(self.frame, text="img").grid(
                    column=j, row=i, sticky="nesw", pady=8, padx=8
                )
            # ctk.CTkLabel(frame,text='hiiiii',fg_color='yellow').pack(expand=True,fill='both')

        self.upper_frame.grid(row=0,column=0,columnspan=5,sticky='nsew')
        self.frame.pack(expand=True, fill="both")
        # self.canvas.pack(expand=True, fill="both")

    def image_genaretor(self):
        url = "https://mangaverse-api.p.rapidapi.com/manga/latest"
        querystring = {
            "page": "1",
            "genres": "Harem,Fantasy",
            "nsfw": "true",
            "type": "all",
        }
        headers = {
            "X-RapidAPI-Key": "025bad191amsh7331ace778f51f6p1de833jsnd83c55b30d26",
            "X-RapidAPI-Host": "mangaverse-api.p.rapidapi.com",
        }
        self.r = requests.get(url, headers=headers, params=querystring)
        self.response = self.r.json()

        self.image_index = []
        self.image_i = []
        self.image_title = []
        self.image_summary = []
        self.image_genres = []
        self.image_id=[]
        # genarating image from api
        a = 0
        print("rrrrrrrrrr")
        for i in self.response["data"]:
            self.image_i.append(i["thumb"])
            self.image_title.append(i["title"])
            self.image_summary.append(i["summary"])
            self.image_genres.append(i['genres'])
            self.image_id.append(i['id'])
            # r=requests.get(url)

            # open(f"{j}.jpg", "wb").write(r.content)

        for i in range(1, 6):
            for j in range(5):

                response = requests.get(self.image_i[a])
                # response = requests.get("https://random.imagecdn.app/900/600")
                open(f"{i}{j}.jpg", "wb").write(response.content)
                im = ctk.CTkImage(
                    light_image=Image.open(f"{i}{j}.jpg"), size=(200, 250)
                )
                button = ctk.CTkButton(
                    self.frame,
                    image=im,
                    text=f"{a}",
                    text_color="white",
                    fg_color="transparent",
                    hover_color="gray",
                    compound="top",
                )
                button.configure(command=lambda button=button: threading.Thread(target=lambda:self.black_frame(button),daemon=True).start())
                button.grid(column=j, row=i, sticky="nesw", pady=8, padx=8)
                ctk.CTkLabel(
                    self.frame,
                    text=f"{self.image_title[a]}",
                    fg_color="transparent",
                    text_color="white",
                ).grid(column=j, row=i, sticky="s")

                self.image_index.append(f"{i}{j}")

                self.frame.update()
                a += 1

    def black_frame(self, button):
        frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        frame.rowconfigure((0, 1, 2, 3), weight=1, uniform="c")
        frame.columnconfigure((0, 1, 2), weight=1, uniform="c")

        frame.bind_all(
            "<Button-4>",
            lambda event: frame._parent_canvas.yview_scroll(
                int(-event.num / 1.5), "units"
            ),
        )
        frame.bind_all(
            "<Button-5>",
            lambda event: frame._parent_canvas.yview_scroll(
                int(event.num / 1.5), "units"
            ),
        )

        im = ctk.CTkImage(
            light_image=Image.open(f"{self.image_index[int(button.cget('text'))]}.jpg"),
            size=(300, 300),
        )
        self.second_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent",
        )
        ctk.CTkLabel(
            self.second_frame,
            text="",
            image=im,
        ).pack()
        ctk.CTkLabel(
            self.second_frame,
            text=f"{self.image_title[int(button.cget('text'))]}\n{self.image_genres[int(button.cget('text'))]}",
            fg_color="transparent",
        ).pack()
        self.second_frame.grid(column=1, row=0, sticky="nesw", pady=15)

        text_box=ctk.CTkTextbox(
            frame,
            fg_color="transparent",
            font=('Calibri',21)
        )
        text_box.grid(column=0, row=1, columnspan=3, sticky="nesw")
        text_box.insert('0.0', self.image_summary[int(button.cget('text'))], tags=None)


        chapter_frame=ctk.CTkFrame(frame,fg_color='transparent')
        ctk.CTkLabel(chapter_frame,text='Helooooo').pack()
        chapter_frame.grid(column=0,row=2,columnspan=3,rowspan=2,sticky='nsew')

        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        chapter_index=ctk.StringVar(value='0')
        Manga_chapter(self.image_id[int(button.cget('text'))])
        ctk.CTkOptionMenu(frame,values=chapter_num,variable=chapter_index).grid(row=1,column=1,sticky='s')
        Chapter_image(int(chapter_index.get()),chapter_frame)

        self.bind_all("<Escape>", func=lambda a: self.second_frame.grid_forget())
        self.bind_all("<Escape>", func=lambda a: frame.place_forget())





class Manga_chapter():
    def __init__(self,id):
        global chapter_id,chapter_num
        url='https://mangaverse-api.p.rapidapi.com/manga/chapter'
        querystring ={"id":id}
        headers = {
            "X-RapidAPI-Key": "025bad191amsh7331ace778f51f6p1de833jsnd83c55b30d26",
            "X-RapidAPI-Host": "mangaverse-api.p.rapidapi.com",
        }
        self.r = requests.get(url, headers=headers, params=querystring)
        response = self.r.json()
        chapter_id=[]
        chapter_num=[]
        for j,i in enumerate(response["data"]):
            chapter_id.append(i['id'])
            chapter_num.append(f"{j}")

class Chapter_image:
    def __init__(self,index,frame):
        global chapter_image
        url = "https://mangaverse-api.p.rapidapi.com/manga/image"

        querystring = {"id":chapter_id[index]}
        headers = {
            "X-RapidAPI-Key": "025bad191amsh7331ace778f51f6p1de833jsnd83c55b30d26",
            "X-RapidAPI-Host": "mangaverse-api.p.rapidapi.com"
        }
        r = requests.get(url, headers=headers, params=querystring)
        response=r.json()
        chapter_image=[]

        for i in response['data']:
            chapter_image.append(i['link'])
        for i,link in enumerate(chapter_image):
                response_1 = requests.get(link)
                
                open(f"chapter/image/{i}.jpg", "wb").write(response_1.content)
                image=Image.open(f"chapter/image/{i}.jpg")
                size=image.size
                im = ctk.CTkImage(
                    light_image=image, size=size
                )
               
                ctk.CTkLabel(frame,text='',image=im).pack()


             
        

ctk.set_appearance_mode("dark")
app = App()
app.mainloop()
