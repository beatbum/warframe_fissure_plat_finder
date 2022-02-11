import tkinter as tk
import screenshot_and_parse as sp


class Gui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self["borderwidth"] = 10
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.create_input_button()
        self.create_output_frame()

    def create_output_frame(self):
        self.output_frame = tk.Frame(self, padx=10, pady=10, borderwidth=3, relief="sunken")
        self.output = [*range(4)]
        print(self.output)
        for y in range(4):
            self.output[y] = tk.Label(self.output_frame, text="Output will go here", relief="raised", borderwidth=2, )
            self.output[y].grid(row=0, column=y)
            self.output_frame.grid(row=0, column=0)
        print(self.output)

    def create_input_button(self):
        self.scan = tk.Button(self)
        self.scan["text"] = "Scan screen for items"
        self.scan["command"] = self.get_data
        self.scan.grid(row=1, column=0)

    def get_data(self):
        place_in_list = 0
        prices = sp.main_logic()
        for item in prices.keys():
            result = prices[item].result()
            if result is not None:
                print("{item}: Price {price}".format(item=item, price=result))
                self.output[place_in_list]["text"] = "{item}\n{price}P".format(item=item, price=result)
                place_in_list += 1


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Plat Finder")
    app = Gui(master=root)
    app.mainloop()
