import customtkinter
import pyperclip

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()
        self.title("AUC Trophy")
        self.geometry(f"{self.WIDTH}X{self.HEIGHT}")

    #Création des 2 frames
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
    #Frame gauche (historique)
        self.hist_lab = customtkinter.CTkLabel(master=self.frame_left, text="Historique des trophées créés:", text_font=("Roboto Medium", -16))
        self.hist_lab.grid(row=1, column=0, pady=10, padx=10)

        self.hist_lab_1 = customtkinter.CTkLabel(master=self.frame_left, text=f"- {get_historique()[0][0]}")
        self.hist_lab_1.grid(row=2, column=0,pady=10,padx=10)
        self.hist_lab_2 = customtkinter.CTkLabel(master=self.frame_left, text=f"- {get_historique()[0][1]}")
        self.hist_lab_2.grid(row=3, column=0,pady=10,padx=10)
        self.hist_lab_3 = customtkinter.CTkLabel(master=self.frame_left, text=f"- {get_historique()[0][2]}")
        self.hist_lab_3.grid(row=4, column=0,pady=10,padx=10)
        self.hist_lab_4 = customtkinter.CTkLabel(master=self.frame_left, text=f"- {get_historique()[0][3]}")
        self.hist_lab_4.grid(row=5, column=0,pady=10,padx=10)
        self.hist_lab_5 = customtkinter.CTkLabel(master=self.frame_left, text=f"- {get_historique()[0][4]}")
        self.hist_lab_5.grid(row=6, column=0,pady=10,padx=10)
    #Frame droite (creation)
        self.name_entry = customtkinter.CTkEntry(master=self.frame_right, placeholder_text='Nom de l\'évent')
        self.name_entry.pack(pady=5)
        self.lore_entry = customtkinter.CTkEntry(master=self.frame_right, placeholder_text='Lore')
        self.lore_entry.pack(pady=5)
        self.item_entry = customtkinter.CTkEntry(master=self.frame_right, placeholder_text='Item')
        self.item_entry.pack(pady=5)
        self.command_text = customtkinter.CTkTextbox(master=self.frame_right, width=500)
        self.command_text.pack(pady=5)
        self.button = customtkinter.CTkButton(master=self.frame_right, text="CTkButton", command=gen_commande)
        self.button.pack(pady=5)
        self.notif = customtkinter.CTkLabel(master=self.frame_right, text="", text_font=("Roboto Medium", -16), text_color=("green"))
        self.notif.pack(pady=5)
    def clear(self):
        self.command_text.destroy()
        self.command_text = customtkinter.CTkTextbox(master=self.frame_right, width=500)
        self.command_text.pack(pady=5,before=self.button)
    def update_historique(self):
        self.hist_lab_1.configure(text=f"- {get_historique()[0][0]}")
        self.hist_lab_2.configure(text=f"- {get_historique()[0][1]}")
        self.hist_lab_3.configure(text=f"- {get_historique()[0][2]}")
        self.hist_lab_4.configure(text=f"- {get_historique()[0][3]}")
        self.hist_lab_5.configure(text=f"- {get_historique()[0][4]}")
    def update_notif(self, text: str, color: str):
        self.notif.configure(text=text,text_color=(color))

def gen_commande():
    if search(app.item_entry.get()):
        commande = translate(app.item_entry.get(),app.name_entry.get(),app.lore_entry.get())
        create_obj()
        app.command_text.insert(0.0,commande)
        app.update_historique()
        app.update_notif("Commande copiée !","green")
    else:
        app.clear()
        app.update_notif("Item non reconnu ...","red")

def create_obj():

    app.clear()

    item = app.item_entry.get()
    name = app.name_entry.get()
    print(app.lore_entry.get())
    lore = wrap_up(app.lore_entry.get())
    print(lore)

    commande = translate(item, name, lore)
    pyperclip.copy(commande)

    with open("historique.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

        if len(lines) == 5:
            lines.pop()


        lines.insert(0,name + " | " + commande + "\n")
    with open("historique.txt", "w", encoding="utf-8") as w_file:
        for i in lines:
            w_file.write(i)

def wrap_up(text: str, n: int = 35):
    wraped = [""]

    if len(text) < n:
        wraped.append(text)
        return wraped
    else:
        text = text.split()

        l = 0
        for word in text:
            if len(word) + len(wraped[l]) +1 < n:
                if not wraped == [""]:
                    wraped[l] += " "
                wraped[l] += word
            elif len(word) + len(wraped[l]) +1 > n:
                wraped.append(word)
                l += 1
    return wraped

def translate(item:str, name:str, lore:list):
    commande = f"give @p " + item + "{display:{Name:'[{\"text\":\"" + name +"\",\"italic\":false,\"color\":\"gold\",\"underlined\":true}]',Lore:['[{\"text\":\"\",\"italic\":false,\"color\":\"dark_purple\"}]','[{\"text\":\"" + name +"\",\"italic\":false,\"color\":\"gray\"},{\"text\":\"\",\"italic\":false,\"color\":\"dark_purple\"}]','[{\"text\":\"Récompense d\\'événement :\",\"italic\":false,\"color\":\"gold\"}]',"
    
    for i in lore:
        if "\\" in i :
            i = i.replace('\\','\\\\\\\\')
        if '"' in i:
            i = i.replace('"','\\\\"')
        if "'" in i:
            i = i.replace("'","\\'")
        commande += "'[{\"text\":\"" +i+"\",\"italic\":true,\"color\":\"dark_purple\"}]',"
    commande += "'[{\"text\":\"\",\"italic\":false,\"color\":\"dark_purple\"}]','[{\"text\":\"Objet Importable\",\"italic\":false,\"color\":\"gold\"},{\"text\":\"\",\"italic\":false,\"color\":\"dark_purple\"}]','[{\"text\":\"⚠ Ne pas utiliser ⚠ \",\"italic\":false,\"color\":\"red\"},{\"text\":\"\",\"italic\":false,\"color\":\"dark_purple\"}]']},Enchantments:[{id:infinity,lvl:1}],HideFlags:1} 1"

    return commande

def search(item: str):
    if "minecraft:" not in item:
        item = "minecraft:" + item

    with open("items.txt", "r") as file:
        temp = file.read().split()

        if item in temp:
            return True
        else:
            return False

def get_historique():
    list_commande = []
    with open("historique.txt", "r", encoding="utf-8") as file:
        for i in file:
            list_commande.append(i.split(" | "))
    
    list_command_nom = []
    for index, value in enumerate(list_commande):
        list_command_nom.append(value[0])
    list_commande = [list_command_nom,list_commande]
    return list_commande


app = App()
app.iconbitmap('AUC.ico')
app.mainloop()
