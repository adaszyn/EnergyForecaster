import settings
from calculator import Calculator
from utils import bcolors
if __name__ == "__main__":
	with Calculator(['PAL18600']) as calculator:
		calculator.load_data()
		print bcolors.OKGREEN + 'FINISHED' + bcolors.ENDC