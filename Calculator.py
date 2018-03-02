import parser
import tkinter
from tkinter import ttk
from tkinter import font

class ScrollFrame(tkinter.Frame):

	def __init__(self, master):
		tkinter.Frame.__init__(self, master)
		self.master = master
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		self.canvas = tkinter.Canvas(self, bg="white")
		self.canvas.grid(row=0, column=0, sticky=tkinter.NSEW)
		self.canvas.bind("<Configure>", self.on_resize)
		
		self.scrollbar = tkinter.Scrollbar(self, orient="vertical", command=self.canvas.yview)
		self.scrollbar.grid(row=0, column=1, sticky=tkinter.NS)
		self.canvas.configure(yscrollcommand=self.scrollbar.set)

		self.inner_frame = tkinter.Frame(self.canvas)
		self.inner_frame.grid(row=0, column=0)
		self.canvas.columnconfigure(0, weight=1)

		self.canvas.create_window(0, 0, window=self.inner_frame, anchor='nw')
		self.update_scroll_region()
		
	def update_scroll_region(self):
		#this mess is because the inner_frame refused to expand to fill the canvas
		max_pixel_width = self.canvas.winfo_width() // 2
		char_count = 1
		while default_font.measure("A"*char_count) < max_pixel_width: #convert pixel unit to char unit
			char_count += 1
		char_count -= 3
		for widget in self.inner_frame.children.values():
			if widget.grid_info()["column"] == 1: #skip the separator widget
				continue
			if widget.grid_info()["column"] == 2: #skip the var widget
				continue
			if widget.grid_info()["column"] == 3: #skip the other separator widget
				continue
			widget.configure(width=char_count)
		#this part should stay
		self.master.update()
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
		
	def on_resize(self, event):	
		self.update_scroll_region()
		
	def scroll_to_bottom(self):
		self.canvas.yview_moveto(1)

class Window(tkinter.Frame):
	
	def __init__(self, master=None):
		tkinter.Frame.__init__(self, master)
		self.master = master
		self.master.geometry("800x600")
		self.master.title("Python Calculator")
		self.pack(fill=tkinter.BOTH, expand=1, padx=5, pady=5)
		self.init_data()
		self.init_layout()
	
	def init_data(self):
		self.list_equations = []
		self.list_results = []
		self.index_history = None
		
	def init_layout(self):
		self.columnconfigure(0, weight=1)
		self.columnconfigure(2, weight=1)
		self.rowconfigure(1, weight=1)

		tkinter.Label(self, text="Input", anchor=tkinter.W, font=default_font).grid(row=0, column=0, sticky=tkinter.EW)
		tkinter.Label(self, text=" X  ", anchor=tkinter.W, font=default_font).grid(row=0, column=1, sticky=tkinter.EW)
		tkinter.Label(self, text="Output", anchor=tkinter.W, font=default_font).grid(row=0, column=2, sticky=tkinter.EW)

		self.frame_history = ScrollFrame(self)
		self.frame_history.grid(row=1, column=0, columnspan=3, sticky=tkinter.NSEW)
		
		self.input_equation = tkinter.Text(self, height=3, width=30, relief=tkinter.FLAT, font=default_font)
		self.input_equation.grid(row=2, column=0, columnspan=3, sticky=tkinter.EW)
		self.input_equation.bind("<Return>", self.submit_equation)
		self.input_equation.bind("<Up>", self.history_up)
		self.input_equation.bind("<Down>", self.history_down)
		self.input_equation.focus_set()
		
	def append_output(self, equation, result):
		self.list_equations.append(equation)
		self.list_results.append(result)
		row = len(self.list_equations)

		output_equation = tkinter.Text(self.frame_history.inner_frame, height=1, width=30, relief=tkinter.FLAT, font=default_font)
		output_equation.insert(tkinter.END, equation)
		output_equation.config(state=tkinter.DISABLED)
		output_equation.grid(row=row, column=0, sticky=tkinter.EW)

		ttk.Separator(self.frame_history.inner_frame, orient=tkinter.VERTICAL).grid(row=row, column=1, stick=tkinter.NS)

		x = tkinter.Text(self.frame_history.inner_frame, height=1, width=4, relief=tkinter.FLAT, font=default_font)
		x.insert(tkinter.END, "X"+str(row)+"=")
		x.config(state=tkinter.DISABLED)
		x.grid(row=row, column=2, sticky=tkinter.EW)

		ttk.Separator(self.frame_history.inner_frame, orient=tkinter.VERTICAL).grid(row=row, column=3, stick=tkinter.NS)

		output_result = tkinter.Text(self.frame_history.inner_frame, height=1, width=30, relief=tkinter.FLAT, font=default_font)
		output_result.insert(tkinter.END, result)
		output_result.config(state=tkinter.DISABLED)
		output_result.grid(row=row, column=4, sticky=tkinter.EW)

		self.frame_history.update_scroll_region()
		self.frame_history.scroll_to_bottom()

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
		equation = self.convert_x_variables(equation)
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
		
	def convert_x_variables(self, equation):
		for i in range(len(self.list_results)-1, -1, -1):
			equation = equation.replace("X"+str(i+1), str(self.list_results[i]))
		return equation
	
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
default_font = font.Font(family="Courier", size=10, weight="normal")
app = Window(root)
root.mainloop()
