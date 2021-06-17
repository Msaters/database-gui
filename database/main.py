from tkinter import *
from tkinter import filedialog, messagebox

from PIL import ImageTk, Image
import sqlite3
import base64
import io

root = Tk()
root.iconphoto(TRUE, PhotoImage(file = "db.png"))
root.title("Adresy")
root.geometry("400x400")

#create a database or connect to one
conn = sqlite3.connect('address_book.db')

#create cursor
c = conn.cursor()

#create Table
c.execute("""CREATE TABLE IF NOT EXISTS adresy (
    Imie text,
    Nazwisko text,
    Miasto text,
    Adres text,
    Wojewodztwo text,
    Kod_Pocztowy text,
    Zdjecie BLOB 
    )
""")

#Databases

#SUBMITING METHOD
def submit():
    # create a database or connect to one
    conn = sqlite3.connect('address_book.db')

    # create cursor
    c = conn.cursor()

    try:
        c.execute("INSERT INTO adresy VALUES (:Imie, :Nazwisko, :Miasto, :Adres, :Wojewodztwo, :kod_pocztowy, :Zdjecie)",
                  (
                      str(Imie_Entry.get()),
                      str(Nazwisko_Entry.get()),
                      str(Miasto_Entry.get()),
                      str(Adres_Entry.get()),
                      str(Wojewodztwo_Entry.get()),
                      str(kod_pocztowy_Entry.get()),
                      imageBlob
                  )
                  )
    except:
        c.execute(
            "INSERT INTO adresy VALUES (:Imie, :Nazwisko, :Miasto, :Adres, :Wojewodztwo, :kod_pocztowy, :Zdjecie)",
            (
                str(Imie_Entry.get()),
                str(Nazwisko_Entry.get()),
                str(Miasto_Entry.get()),
                str(Adres_Entry.get()),
                str(Wojewodztwo_Entry.get()),
                str(kod_pocztowy_Entry.get()),
                None
            )
            )

    #Clearing
    Imie_Entry.delete(0 , END)
    Nazwisko_Entry.delete(0 , END)
    Miasto_Entry.delete(0 , END)
    Adres_Entry.delete(0 , END)
    Wojewodztwo_Entry.delete(0 , END)
    kod_pocztowy_Entry.delete(0 , END)
    image = None

    # submit changes
    conn.commit()
    # close connection
    conn.close()

#QUERY METHOD
def query():
    # create a database or connect to one
    conn = sqlite3.connect('address_book.db')

    # create cursor
    c = conn.cursor()

    c.execute("SELECT *, oid FROM adresy")
    adresy = c.fetchall()

    #try to destroy (restart) window if opened
    global query
    try:
        query.destroy()
    except:
        pass

    query = Toplevel()
    query.title("Baza Danych")
    query.geometry("300x600")

    #Go Thru every adres
    print_adresy = ''
    i = 0
    global image2
    for adres in adresy:
        print_adresy = str(adres[0]) + " " + str(adres[1]) + " " + str(adres[7]) + "\n"
        query_label = Label(query, text = print_adresy, font="Arial 12 italic", anchor = "center", width = 30)
        query_button = Button(query,image = image2, width = 12, height = 12, command = lambda blob = adres[6]: showImage(blob))
        query_label.grid(row = i, columnspan = 2, column = 0, sticky  = W + E)
        query_button.grid(row = i, column = 2, pady= (0, 17))
        i = i + 1

    # submit changes
    conn.commit()
    # close connection
    conn.close()

#SHOWING IMAGE FROM BLOB
def showImage(blob):
    try:
        binaryData = base64.b64decode(blob)

        # Convert the bytes into a PIL image
        image = Image.open(io.BytesIO(binaryData))
        image.show()
    except:
        messagebox.showwarning(title = "ta kolumna nie ma zdjecia", message = "do tej kolumny nie zostalo zalaczone zdjecie")


#DELETING METHOD
def delete():
    # create a database or connect to one
    conn = sqlite3.connect('address_book.db')

    # create cursor
    c = conn.cursor()

    c.execute("DELETE FROM adresy WHERE oid = :PLACEHOLDER", Delete_Entry.get())
    messagebox.showinfo(title = "Usunieto podany element", message="Element o numerze %s został usunięty z bazydanych" % Delete_Entry.get())
    #try to make here query restart

    # submit changes
    conn.commit()

    # close connection
    conn.close()

#SAVING UPDATED DATA METHOD
def save():
    # create a database or connect to one
    conn = sqlite3.connect('address_book.db')

    # create cursor
    c = conn.cursor()
    try:
        c.execute("""  
            UPDATE adresy SET 
            Imie = :Imie, 
            Nazwisko = :Nazwisko,
            Miasto = :Miasto, 
            Adres = :Adres, 
            Wojewodztwo = :Wojewodztwo,
            kod_pocztowy = :kod_pocztowy,
            Zdjecie = :Zdjecie
            WHERE oid = :number""",
            {
                'Imie' : Imie_Entry_update.get(),
                'Nazwisko' : Nazwisko_Entry_update.get(),
                'Miasto' : Miasto_Entry_update.get(),
                'Adres' : Adres_Entry_update.get(),
                'Wojewodztwo' : Wojewodztwo_Entry_update.get(),
                'kod_pocztowy' : kod_pocztowy_Entry_update.get(),
                'Zdjecie' : imageBlob,
                'number' : Delete_Entry.get()
            })
    except:
        c.execute("""  
                    UPDATE adresy SET 
                    Imie = :Imie, 
                    Nazwisko = :Nazwisko,
                    Miasto = :Miasto, 
                    Adres = :Adres, 
                    Wojewodztwo = :Wojewodztwo,
                    kod_pocztowy = :kod_pocztowy,
                    Zdjecie = :Zdjecie
                    WHERE oid = :number""",
                  {
                      'Imie': Imie_Entry_update.get(),
                      'Nazwisko': Nazwisko_Entry_update.get(),
                      'Miasto': Miasto_Entry_update.get(),
                      'Adres': Adres_Entry_update.get(),
                      'Wojewodztwo': Wojewodztwo_Entry_update.get(),
                      'kod_pocztowy': kod_pocztowy_Entry_update.get(),
                      'Zdjecie': None,
                      'number': Delete_Entry.get()
                  })

    # submit changes
    conn.commit()
    # close connection
    conn.close()

    update.destroy()

#UPDATING METHOD
def update():
    # create a database or connect to one
    conn = sqlite3.connect('address_book.db')

    # create cursor
    c = conn.cursor()

    # try to destroy (restart) window if opened
    global update
    try:
        update.destroy()
    except:
        pass

    c.execute("SELECT * FROM adresy WHERE oid = :number", Delete_Entry.get())
    update_data = c.fetchone()
    if(update_data is not None):
        update = Toplevel()
        update.title("Update Window")
        update.geometry("315x300")

        #Create globals for updating tables
        global Imie_Entry_update
        global Nazwisko_Entry_update
        global Miasto_Entry_update
        global Adres_Entry_update
        global Wojewodztwo_Entry_update
        global kod_pocztowy_Entry_update
        global imageBlob_update

        #Entries in save window to change their value
        Imie_Entry_update = Entry(update, width=30)
        Nazwisko_Entry_update = Entry(update, width=30)
        Miasto_Entry_update = Entry(update, width=30)
        Adres_Entry_update = Entry(update, width=30)
        Wojewodztwo_Entry_update = Entry(update, width=30)
        kod_pocztowy_Entry_update = Entry(update, width=30)

        # Create Image Upload Button update
        global image
        upload_Button_update = Button(update, image = image, command=upload1, width=35, height=35)

        #inserting values to boxes from table
        Imie_Entry_update.insert(0, update_data[0])
        Nazwisko_Entry_update.insert(0, update_data[1])
        Miasto_Entry_update.insert(0, update_data[2])
        Adres_Entry_update.insert(0, update_data[3])
        Wojewodztwo_Entry_update.insert(0, update_data[4])
        kod_pocztowy_Entry_update.insert(0, update_data[5])
        imageBlob_update = update_data[6]

        Imie_Entry_update.grid(row=0, column=1, pady=(10, 0))
        Nazwisko_Entry_update.grid(row=1, column=1)
        Miasto_Entry_update.grid(row=2, column=1)
        Adres_Entry_update.grid(row=3, column=1)
        Wojewodztwo_Entry_update.grid(row=4, column=1)
        kod_pocztowy_Entry_update.grid(row=5, column=1)
        upload_Button_update.grid(row=6, column=1, pady=5)

        # labels
        Imie_Label_update = Label(update, text="Imie : ", anchor=W)
        Nazwisko_Label_update = Label(update, text="Nazwisko : ", anchor=W)
        Miasto_Label_update = Label(update, text="Miasto : ", anchor=W)
        Adres_Label_update = Label(update, text="Adres : ", anchor=W)
        Wojewodztwo_Label_update = Label(update, text="Wojewodztwo : ", anchor=W)
        kod_pocztowy_Label_update = Label(update, text="kod_pocztowy : ", anchor=W)
        zdjecie_Label = Label(update, text="Zdjecie : ", anchor=W)

        Imie_Label_update.grid(row=0, column=0, pady=(10, 0), sticky=W + E)
        Nazwisko_Label_update.grid(row=1, column=0, sticky=W + E)
        Miasto_Label_update.grid(row=2, column=0, sticky=W + E)
        Adres_Label_update.grid(row=3, column=0, sticky=W + E)
        Wojewodztwo_Label_update.grid(row=4, column=0, sticky=W + E)
        kod_pocztowy_Label_update.grid(row=5, column=0, sticky=W + E)
        zdjecie_Label.grid(row=6, column=0, sticky=W + E)

        # Create Update Button
        Update_Rec = Button(update, text="Save", command=save)
        Update_Rec.grid(row=7, column=0, columnspan=2, ipadx=142, pady = 10)
    else:
        messagebox.showwarning(title="zly numer kolumny", message="kolumna o takim numerze nie istnieje")

    # submit changes
    conn.commit()

    # close connection
    conn.close()

#return image as a large binary object (blob)
def readToBinary(image):
    with open(image, 'rb') as f:
        blobImage = f.read()
    blobImage = base64.b64encode(blobImage)
    return blobImage

#UPLODING IMG METHOD
def upload():
    global imageBlob
    img = filedialog.askopenfilename(initialdir="/", title="Select File",
                                         filetypes=(("zdjecia", ("*JPG", "*PNG")), ("gify", "*GIF")))
    imageBlob = readToBinary(img)

#TAK DALO BY SIE TO ZROBIc OPTYMALnIEJ NAPRZYKLAD NA LAMBDZIE ALE JUZ ZMECZONY JESTEM A TO MALO ZMIENIA
def upload1():
    global imageBlob_update
    img = filedialog.askopenfilename(initialdir="/", title="Select File",
                                         filetypes=(("zdjecia", ("*JPG", "*PNG")), ("gify", "*GIF")))
    imageBlob_update = readToBinary(img)

#Entries
Imie_Entry = Entry(root, width = 30)
Nazwisko_Entry = Entry(root, width = 30)
Miasto_Entry = Entry(root, width = 30)
Adres_Entry = Entry(root, width = 30)
Wojewodztwo_Entry = Entry(root, width = 30)
kod_pocztowy_Entry = Entry(root, width = 30)

Imie_Entry.grid(row = 0,column = 1, pady = (10,0))
Nazwisko_Entry.grid(row = 1,column = 1)
Miasto_Entry.grid(row = 2,column = 1)
Adres_Entry.grid(row = 3,column = 1)
Wojewodztwo_Entry.grid(row = 4,column = 1)
kod_pocztowy_Entry.grid(row = 5,column = 1)

#labels
Imie_Label = Label(root, text = "Imie : ", anchor = W)
Nazwisko_Label = Label(root, text = "Nazwisko : ", anchor = W)
Miasto_Label = Label(root, text = "Miasto : ", anchor = W)
Adres_Label = Label(root, text = "Adres : ", anchor = W)
Wojewodztwo_Label = Label(root, text = "Wojewodztwo : ", anchor = W)
kod_pocztowy_Label = Label(root, text = "kod_pocztowy : ", anchor = W)
zdjecie_Label = Label(root, text = "Zdjecie : ", anchor = W)

padx = 10
Imie_Label.grid(row = 0,column = 0, pady = (10,0), sticky=W+E, padx = (padx,0))
Nazwisko_Label.grid(row = 1,column = 0, sticky=W+E, padx = (padx,0))
Miasto_Label.grid(row = 2,column = 0, sticky=W+E, padx = (padx,0))
Adres_Label.grid(row = 3,column = 0, sticky=W+E, padx = (padx,0))
Wojewodztwo_Label.grid(row = 4,column = 0, sticky=W+E, padx = (padx,0))
kod_pocztowy_Label.grid(row = 5,column = 0, sticky=W+E, padx = (padx,0))
zdjecie_Label.grid(row = 6,column = 0, sticky=W+E, padx = (padx,0))

#DELETE ID GUI
Delete_Label = Label(root, text= "wiersz do usuniecia (ID)", anchor = W)
Delete_Entry = Entry(root, width = 30)
Delete_Label.grid(row = 9, column = 0, sticky = W+E, padx = (10,0), pady = 5)
Delete_Entry.grid(row = 9, column = 1)

#Buttons

#Create Image Upload Button
image2 = PhotoImage(file = "image_icon.png")
image = PhotoImage(file = "upload.png")
upload_Button = Button(root ,image = image, command = upload, width = 35, height = 35)
upload_Button.grid(row = 6, column = 1, pady = 5)

#Create Submit Button
Add_Rec = Button(root,text = "Dodaj Rekord do Databazy" , command = submit)
Add_Rec.grid(row = 7, column = 0, columnspan = 2, ipadx = 119, pady = (10,0), padx = (5,0))

#Create Query Button
Query_Rec = Button(root,text = "Pokaz Rekordy" , command = query)
Query_Rec.grid(row = 8, column = 0, columnspan = 2, ipadx = 150, padx = (5,0))

#Create Delete Button
Delete_Rec = Button(root,text = "Usun Rekord" , command = delete)
Delete_Rec.grid(row = 10, column = 0, columnspan = 2, ipadx = 154, padx = (5,0))

#Create Update Button
Update_Rec = Button(root,text = "Aktualizuj Rekord" , command = update)
Update_Rec.grid(row = 11, column = 0, columnspan = 2, ipadx = 142, padx = (5,0))

#submit changes
conn.commit()

#close connection
conn.close()

root.mainloop()