import curses
from curses import wrapper
import pyperclip

"""
NOTE: permettre de quitter en appuyant sur échap et pas en écrivant ex
        supporter les caractères problématique : (/ etc)
"""

item = None
name = None
lore = None

class Menu:
    def __init__(self, options):
        self.options = options
        self.state = 1

        max_op_len = 0
        for i in self.options:
            if len(i) > max_op_len: max_op_len = len(i)

        self.width = round(max_op_len * 1.5)
        self.height = len(options) + 2

    def construct(self, stdscr):
        try:
            stdscr.clear()

            if self.state > len(self.options): self.state = len(self.options)
            elif self.state < 1: self.state = 1

            stdscr.addstr(u'\u250C' + u'\u2500'*(self.width-2) + u'\u2510' + '\n')

            for index, option in enumerate(self.options):
                
                if index + 1 == self.state:
                    stdscr.addstr(u'\u2502')
                    stdscr.addstr(option, curses.color_pair(1))
                    stdscr.addstr(" "*(self.width - len(option) - 2) + u'\u2502' + '\n')
                else:
                    stdscr.addstr(u'\u2502' + option)
                    stdscr.addstr(" "*(self.width - len(option) - 2) + u'\u2502' + '\n')

            stdscr.addstr(u'\u2514' + u'\u2500'*(self.width-2) + u'\u2518' + '\n')
        except:
            raise Exception("\u001b[31mVous avez écraser mon joli menu ! :(((\033[0m")
def create_obj(stdscr):

    if not get_info(stdscr):
        return False

    commande = translate(item, name, lore)
    pyperclip.copy(commande)

    stdscr.clear()
    stdscr.addstr(commande + "\nCommande copiée")
    stdscr.getch()

    with open("historique.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

        if len(lines) == 5:
            lines.pop()


        lines.insert(0,name + " | " + commande + "\n")
    with open("historique.txt", "w", encoding="utf-8") as w_file:
        for i in lines:
            w_file.write(i)

def get_info(stdscr):
    curses.echo(True)
    while True:
        stdscr.clear()
        stdscr.addstr("Quel item utiliser ?\n")

        global item
        item = get_str_utf8(stdscr,"Quel item utiliser ?\n")

        if item.lower() == "ex":
            return False
        elif search(item):
            break
    while True:
        stdscr.clear()
        stdscr.addstr("Quel est le nom de l'évent ?\n")


        global name
        name = get_str_utf8(stdscr,"Quel est le nom de l'évent ?\n")

        if name.lower() == "ex":
            return False
        elif '"' in name or '\'' in name:
            if '"' in name:
                name = name.replace('"','\\\\"')
            if '\'' in name:
                name = name.replace("'","\\'")
            break
        break
    while True:
        stdscr.clear()
        stdscr.addstr("Quel sera sa description ?\n")

        global lore
        lore = get_str_utf8(stdscr,"Quel sera sa description ?\n")
        if lore.lower() == "ex":
            return False
        elif '"' in name or '\'' in name:
            if '"' in name:
                name = name.replace('"','\\\\"')
            if '\'' in name:
                name = name.replace("'","\\'")

        lore = wrap_up(lore)
        break

    curses.echo(False)
    return True

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

def search(item: str):
    if "minecraft:" not in item:
        item = "minecraft:" + item

    with open("items.txt", "r") as file:
        temp = file.read().split()

        if item in temp:
            return True
        else:
            return False

def translate(item:str, name:str, lore:list):
    commande = f"give @p " + item + "{display:{Name:'[{\"text\":\"" + name +"\",\"italic\":false,\"color\":\"gold\",\"underlined\":true}]',Lore:['[{\"text\":\"\",\"italic\":false,\"color\":\"dark_purple\"}]','[{\"text\":\"" + name +"\",\"italic\":false,\"color\":\"gray\"},{\"text\":\"\",\"italic\":false,\"color\":\"dark_purple\"}]','[{\"text\":\"Récompense d\\'événement :\",\"italic\":false,\"color\":\"gold\"}]',"
    
    for i in lore:
        commande += "'[{\"text\":\"" +i+"\",\"italic\":true,\"color\":\"dark_purple\"}]',"
    commande += "'[{\"text\":\"\",\"italic\":false,\"color\":\"dark_purple\"}]','[{\"text\":\"Objet Importable\",\"italic\":false,\"color\":\"gold\"},{\"text\":\"\",\"italic\":false,\"color\":\"dark_purple\"}]','[{\"text\":\"⚠ Ne pas utiliser ⚠ \",\"italic\":false,\"color\":\"red\"},{\"text\":\"\",\"italic\":false,\"color\":\"dark_purple\"}]']},Enchantments:[{id:infinity,lvl:1}],HideFlags:1} 1"

    return commande
def historique(stdscr):
    list_commande = []
    with open("historique.txt", "r", encoding="utf-8") as file:
        for i in file:
            list_commande.append(i.split(" | "))
    
    list_command_menu = []
    for index, value in enumerate(list_commande):
        list_command_menu.append(value[0])
    menu_historique = Menu(list_command_menu)
    while True:
        menu_historique.construct(stdscr)

        key = stdscr.getch()
        if key == curses.KEY_UP:
            menu_historique.state -= 1
        elif key == curses.KEY_DOWN:
            menu_historique.state += 1
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            if menu_historique.state == 1:
                pyperclip.copy(list_commande[0][1])
                stdscr.addstr("Commande copiée")
                stdscr.getch()
                break
            if menu_historique.state == 2:
                pyperclip.copy(list_commande[1][1])
                stdscr.addstr("Commande copiée")
                stdscr.getch()
                break
            if menu_historique.state == 3:
                pyperclip.copy(list_commande[2][1])
                stdscr.addstr("Commande copiée")
                stdscr.getch()
                break
            if menu_historique.state == 4:
                pyperclip.copy(list_commande[3][1])
                stdscr.addstr("Commande copiée")
                stdscr.getch()
                break
            if menu_historique.state == 5:
                pyperclip.copy(list_commande[4][1])
                stdscr.addstr("Commande copiée")
                stdscr.getch()
                break
            if menu_historique.state == 6:
                pyperclip.copy(list_commande[5][1])
                stdscr.addstr("Commande copiée")
                stdscr.getch()
                break
            if menu_historique.state == 7:
                pyperclip.copy(list_commande[6][1])
                stdscr.addstr("Commande copiée")
                stdscr.getch()
                break
            if menu_historique.state == 8:
                pyperclip.copy(list_commande[7][1])
                stdscr.addstr("Commande copiée")
                stdscr.getch()
                break
            if menu_historique.state == 9:
                pyperclip.copy(list_commande[8][1])
                stdscr.addstr("Commande copiée")
                stdscr.getch()
                break
            if menu_historique.state == 10:
                pyperclip.copy(list_commande[9][1])
                stdscr.addstr("Commande copiée")
                stdscr.getch()
                break
        
def menu_scr(stdscr):

    start_menu = Menu(["Créer un objet","Historique des objets créés","Quitter"])
    while True:
        start_menu.construct(stdscr)
        key = stdscr.getch()
        if key == curses.KEY_UP:
            start_menu.state -= 1
        elif key == curses.KEY_DOWN:
            start_menu.state += 1
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            if start_menu.state == 1:
                create_obj(stdscr)
            if start_menu.state == 2:
                historique(stdscr)
            if start_menu.state == 3:
                break

def get_str_utf8(stdscr, before: str = None):
    string = ""
    while True:
        key = chr(stdscr.getch())
        if key == '\n':
            return string
        elif key == '\x08' and not string == "":
            string = string[:-1]
            stdscr.clear()
            if not before == None: stdscr.addstr(before)
            stdscr.addstr(string)
            
        else:
            string += key

            stdscr.clear()
            if not before == None: stdscr.addstr(before)
            stdscr.addstr(string)

def main(stdscr):
    
    stdscr.keypad(True)
    curses.curs_set(0)

    if curses.is_term_resized(0,0) == True:
        curses.resize_term(*stdscr.getmaxyx())
        stdscr.clear()
        stdscr.refresh()
    

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)


    menu_scr(stdscr)


wrapper(main)