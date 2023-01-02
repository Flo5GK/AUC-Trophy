import customtkinter
import pyperclip

app = customtkinter.CTk()
app.geometry(f"{600}x{500}")
app.title("CTk example")

last_scr = None

menu_frame = customtkinter.CTkFrame(app)
historique_frame = customtkinter.CTkFrame(app)
creation_frame = customtkinter.CTkFrame(app)
def init():
#création screen
    name_entry = customtkinter.CTkEntry(master=creation_frame, placeholder_text='Nom de l\'évent')
    name_entry.pack(pady=5)
    lore_entry = customtkinter.CTkEntry(master=creation_frame, placeholder_text='Lore')
    lore_entry.pack(pady=5)
    item_entry = customtkinter.CTkEntry(master=creation_frame, placeholder_text='Item')
    item_entry.pack(pady=5)
    button = customtkinter.CTkButton(master=creation_frame, text="CTkButton", command=button_function)
    button.pack(pady=5)
    command_text = customtkinter.CTkTextbox(master=creation_frame, width=500)
    command_text.pack(pady=5)
#Historique screen

def button_function():
    if search(item_entry.get()):
        commande = translate(item_entry.get(),name_entry.get(),lore_entry.get())
        create_obj()
        command_text.insert(0.0,commande)
    else:
        clear_textbox(command_text)
        command_text.insert(0.0,"Item non reconnu")

def create_obj():

    clear_textbox(command_text)

    item = item_entry.get()
    name = name_entry.get()
    lore = wrap_up(lore_entry.get())

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

def clear_textbox(textbox):
    textbox.destroy()
    global command_text
    command_text = customtkinter.CTkTextbox(master=app, width=500)
    command_text.pack(pady=5)

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

def creation():
    clean()
    creation_frame.pack()
    global last_scr
    last_scr = "creation"

def historique():
    clean()
    historique_frame.pack()
    global last_scr
    last_scr = "historique"
    pass

def clean():
    if last_scr == "menu":
        creation_frame.pack_forget()
    elif last_scr == "creation":
        creation_frame.pack_forget()
    elif last_scr == "historique":
        historique_frame.pack_forget()

init()


app.mainloop()