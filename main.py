import settings
from calculator import Calculator
from fancyprinter import FancyPrinter
if __name__ == "__main__":
	with Calculator(['PAL18600']) as calculator:
		calculator.load_data()
		FancyPrinter.print_green('FINISHED')
