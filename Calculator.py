import parser
import tkinter
from tkinter import ttk

class Window(tkinter.Frame):
	
	def __init__(self, master=None):
		tkinter.Frame.__init__(self, master)
		self.master = master
		self.master.geometry("800x600")
		self.master.title("Calculator")
		self.pack(fill=tkinter.BOTH, expand=1, padx=5, pady=5)
		self.init_data()
		self.init_layout()
	
	def init_data(self):
		self.list_equations = []
		self.list_results = []
		self.index_history = None
		
	def init_layout(self):
		self.frame_history = tkinter.Frame(self)
		self.frame_history.grid(row=0, column=0, stick=tkinter.EW)
		self.columnconfigure(0, weight=1)
		tkinter.Label(self.frame_history, text="Input", anchor=tkinter.W).grid(row=0, column=0, sticky=tkinter.EW)
		ttk.Separator(self.frame_history, orient=tkinter.VERTICAL).grid(row=0, column=1, stick=tkinter.NS)
		tkinter.Label(self.frame_history, text="Output", anchor=tkinter.W).grid(row=0, column=2, sticky=tkinter.EW)
		self.frame_history.columnconfigure(0, weight=1)
		self.frame_history.columnconfigure(2, weight=1)
		self.input_equation = tkinter.Text(self, height=20, width=30, relief=tkinter.FLAT)
		self.input_equation.grid(row=1, column=0, sticky=tkinter.EW)
		self.input_equation.bind("<Return>", self.submit_equation)
		self.input_equation.bind("<Up>", self.history_up)
		self.input_equation.bind("<Down>", self.history_down)
		self.input_equation.focus_set()
		
	def append_output(self, equation, result):
		self.list_equations.append(equation)
		self.list_results.append(result)
		row = len(self.list_equations) + 1
		output_equation = tkinter.Text(self.frame_history, height=1, width=30, relief=tkinter.FLAT)
		output_equation.insert(tkinter.END, equation)
		output_equation.config(state=tkinter.DISABLED)
		output_equation.grid(row=row, column=0, sticky=tkinter.EW)
		ttk.Separator(self.frame_history, orient=tkinter.VERTICAL).grid(row=row, column=1, stick=tkinter.NS)
		output_result = tkinter.Text(self.frame_history, height=1, width=30, relief=tkinter.FLAT)
		output_result.insert(tkinter.END, result)
		output_result.config(state=tkinter.DISABLED)
		output_result.grid(row=row, column=2, sticky=tkinter.EW)

	def clear_input(self):
		self.input_equation.delete("1.0", tkinter.END)
		
	def set_input(self, text):
		self.clear_input()
		self.input_equation.insert("1.0", text)
		
	def history_up(self, event):
		max = len(self.list_equations) - 1
		if max < 0:
			return
		if self.index_history == None:
			self.index_history = max
		else:
			self.index_history -= 1
			if self.index_history < 0:
				self.clear_input()
				self.index_history = None
				return
		self.set_input(self.list_equations[self.index_history])
		
	def history_down(self, event):
		max = len(self.list_equations) - 1
		if max < 0:
			return
		if self.index_history == None:
			self.index_history = 0
		else:
			self.index_history += 1
			if self.index_history > max:
				self.clear_input()
				self.index_history = None
				return
		self.set_input(self.list_equations[self.index_history])
		
	def submit_equation(self, event):
		equation = self.text_last_line(event.widget)
		equation = equation.strip()
		result = self.calculate(equation)
		self.append_output(equation, str(result))
		self.clear_input()
		self.index_history = None
		return "break" #otherwise, the enter is still added to input after this
	
	@staticmethod
	def text_last_line(text_widget):
		some_text = text_widget.get("1.0", tkinter.END) #get full text
		lines = some_text.split("\n")
		return lines[-2] #actual last line is expected empty
	
	@staticmethod
	def calculate(equation):
		"""
		Evaluates the expression
		ref : http://stackoverflow.com/questions/594266/equation-parsing-in-python
		"""
		try:
			formulae = parser.expr(equation).compile()
			return eval(formulae)
		except Exception as e:
			return "Error: " + str(e)

root = tkinter.Tk()
app = Window(root)
root.mainloop()
