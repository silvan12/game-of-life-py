from ctypes import sizeof
import tkinter as tk
import time

class gameOptions:
    def __init__(self):
        # Titel
        root.title("Opties - Game of Py")

        # Parents
        self.container = tk.Frame(root)
        self.button_group = tk.Frame(self.container)        

        # Grootte
        self.size_label = tk.Label(self.container, text="Grootte:")
        self.size_label.grid(column=0, row=0, sticky="sw")
        self.size_input = tk.Scale(self.container, from_=1, to=25, orient=tk.HORIZONTAL)
        self.size_input.grid(column=1, row=0)

        # Minimum aantal buren om te overleven
        self.cel_min_label = tk.Label(self.container, text="Minimum buren om levend te blijven:")
        self.cel_min_label.grid(column=0, row=1, sticky="sw")
        self.cel_min_input = tk.Scale(self.container, from_=1, to=8, orient=tk.HORIZONTAL)
        self.cel_min_input.grid(column=1, row=1)

        # Maximum aantal buren om te overleven
        self.cel_max_label = tk.Label(self.container, text="Maximum buren om levend te blijven:")
        self.cel_max_label.grid(column=0, row=2, sticky="sw")
        self.cel_max_input = tk.Scale(self.container, from_=1, to=8, orient=tk.HORIZONTAL)
        self.cel_max_input.grid(column=1, row=2)

        # Aantal buren om levend te worden
        self.cel_revive_label = tk.Label(self.container, text="Aantal buren om levend te worden:")
        self.cel_revive_label.grid(column=0, row=3, sticky="sw")
        self.cel_revive_input = tk.Scale(self.container, from_=1, to=8, orient=tk.HORIZONTAL)
        self.cel_revive_input.grid(column=1, row=3)
        
        # Aantal generaties
        self.generations_label = tk.Label(self.container, text="Aantal generaties")
        self.generations_label.grid(column=0, row=4, sticky="sw")
        self.generations_input = tk.Scale(self.container, from_=1, to=200, orient=tk.HORIZONTAL)
        self.generations_input.grid(column=1, row=4)

        self.button_group.grid(row=5,sticky="w")

        self.submit_button = tk.Button(self.button_group, width=10, text="Toepassen", command=self.submit)
        self.submit_button.grid(column=0, row=0)
        self.reset_button = tk.Button(self.button_group, width=10, text="Reset", command=self.reset)
        self.reset_button.grid(column=1, row=0)

        # Standaard waarden
        self.reset()

        self.container.pack()


    def reset(self):
        self.size_input.set(7)
        self.cel_min_input.set(2)
        self.cel_max_input.set(3)
        self.cel_revive_input.set(3)
        self.generations_input.set(5)


    def submit(self):

        # Zet de opties in een dictionary
        self.options = {
            "size": self.size_input.get(),
            "cel_min": self.cel_min_input.get(),
            "cel_max": self.cel_max_input.get(),
            "cel_revive": self.cel_revive_input.get(),
            "generations": self.generations_input.get()
        }
                          
        self.container.forget()

        # Pass de opties naar het volgende scherm
        gameInput(self.options)
    
class gameInput:
    def __init__(self, options):
        # Titel
        root.title("Invoer - Game of Py")

        self.options = options

        self.container = tk.Frame(root)
        self.bord = tk.Frame(self.container)
        self.button_group = tk.Frame(self.container)

        # Lege lijst
        self.bord_list = []

        i = 0
        for x in range(self.options["size"]):
            for y in range(self.options["size"]):

                # Append lijst met een boolean var
                self.bord_list.append(tk.IntVar())

                # Koppel de checkbox aan de boolean var in de lijst met dezelfde index
                # Om later de state te checken
                tk.Checkbutton(self.bord, highlightbackground="white",
                activebackground="gray", indicatoron=0, bg="black",
                bd=0, width=2,variable=self.bord_list[i]).grid(row=x, column=y)

                i += 1

        self.bord.pack()

        self.submit_button = tk.Button(self.button_group, width=10, text="Start", command=self.submit)
        self.submit_button.grid(column=0, row=0)
        self.reset_button = tk.Button(self.button_group, width=10, text="Reset", command=self.reset)
        self.reset_button.grid(column=1, row=0)
        
        self.button_group.pack()

        self.container.pack()

    def reset(self):
        for cel in self.bord.winfo_children():
            cel.deselect()

    def submit(self):  
        # Haal de state op van checkboxes door lijst van intvars
        self.bord_list = [i.get() for i in self.bord_list]

        # Append rij i tot en met i + lengte van een rij
        # Om list te splitten in evengrote rijen
        self.bord = []
        for i in range(0, len(self.bord_list), self.options["size"]):
            self.bord.append(self.bord_list[i:i + self.options["size"]])
            
        self.container.forget()

        gameOfLife(self.options, self.bord)


class gameOfLife:
    def __init__(self, options, bord):
        # Titel
        root.title("Simulatie - Game of Py")
        self.options = options
        self.bord = bord

        self.size = self.options["size"]
        self.cel_min = self.options["cel_min"]
        self.cel_max = self.options["cel_max"]
        self.cel_revive = self.options["cel_revive"]
        self.generations = self.options["generations"]

        window_size = self.size * 20
        self.container = tk.Canvas(root, width=window_size, height=window_size)
        self.container.pack()

        for i in range(self.generations):
            self.show()
            time.sleep(0.1)
            self.update()


    def update(self):
        # Nieuw leeg bord
        bord_update = [[0] * self.size for i in range(self.size)]
        # Binnen het raster
        for x in range(1, self.size - 1):
            for y in range(1, self.size - 1):
                # Huidige cel
                cel = self.bord[x][y]
                # Tel aantal buren
                aantal_buren = self.check(x,y)
                # Pas regels toe
                if cel and (aantal_buren < self.cel_min or aantal_buren > self.cel_max):
                    # Cel blijft dood
                    bord_update[x][y] = 0
                elif not cel and aantal_buren == self.cel_revive:
                    # Cel komt tot leven
                    bord_update[x][y] = 1
                else:
                    # Cel veranderd niet
                    bord_update[x][y] = cel

        self.bord = bord_update

    def check(self, x, y):
        buren = 0
        # Check rond een cel
        for i in range(-1,2):
            for j in range(-1,2):
                # Tel de inhoud van de cel op
                buren += self.bord[i + x][j + y]

        # Haal de cel zelf er van af
        buren -= self.bord[x][y]
        return buren

    def show(self):
        # Verwijder alle cellen
        self.container.delete("all")

        # Loop door het bord met i en j
        for i in range(self.size):
            for j in range(self.size):
                # Lengte cel
                cel_size = 20

                # Coördinaten cel
                x1 = cel_size * j
                y1 = cel_size * i
                x2 = x1 + cel_size
                y2 = y1 + cel_size

                # Check status van cel
                if self.bord[i][j]:
                    # Cel is dood
                    self.container.create_rectangle(x1, y1, x2, y2, fill='#FFFFFF')
                else:
                    # Cel is levend
                    self.container.create_rectangle(x1, y1, x2, y2, fill="#000000")
                    
        # Update 
        root.update_idletasks()



root = tk.Tk()
gameOptions()

root.mainloop()