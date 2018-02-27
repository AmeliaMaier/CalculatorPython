import parser
import tkinter

class Window(tkinter.Frame):
	
	def __init__(self, master=None):
		tkinter.Frame.__init__(self, master)
		self.master = master
		self.master.geometry("800x600")
		self.master.title("Calculator")
		self.pack(fill=tkinter.BOTH, expand=1, padx=5, pady=5)
		self.init_layout()
		
	def init_layout(self):
		tkinter.Label(self, text="Input").grid(row=0, column=0, sticky=tkinter.W)
		tkinter.Label(self, text="Output").grid(row=0, column=1, sticky=tkinter.W)
		self.inputControl = tkinter.Text(self, height=20, width=30)
		self.inputControl.grid(row=1, column=0)
		self.inputControl.bind("<Return>", submit_equation)
		self.inputControl.bind("<Up>", lambda event: "break")
		self.inputControl.bind("<Down>", lambda event: "break")
		self.outputControl = tkinter.Text(self, height=20, width=30, state=tkinter.DISABLED)
		self.outputControl.grid(row=1, column=1)
		self.inputControl.focus_set()
		
	def append_output(self, text):
		self.outputControl.config(state=tkinter.NORMAL)
		self.outputControl.insert(tkinter.END, text + "\n")
		self.outputControl.config(state=tkinter.DISABLED)
		
def submit_equation(event):
	equation = text_last_line(event.widget)
	equation = equation.strip()
	calculate(equation)
	
def text_last_line(text_widget):
	some_text = text_widget.get("0.0", tkinter.END) #get full text
	lines = some_text.split("\n")
	return lines[-2] #actual last line is expected empty
	
def calculate(equation):
	"""
	Evaluates the expression
	ref : http://stackoverflow.com/questions/594266/equation-parsing-in-python
	"""
	try:
		formulae = parser.expr(equation).compile()
		result = eval(formulae)
		app.append_output(str(result))
	except Exception as e:
		app.append_output("Error: " + str(e))

root = tkinter.Tk()
app = Window(root)
root.mainloop()
