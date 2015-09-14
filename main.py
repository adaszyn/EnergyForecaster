import settings
from calculator import Calculator
from utils import bcolors
if __name__ == "__main__":
	with Calculator(['CTP01600']) as calculator:
		calculator.load_data()
		print bcolors.OKGREEN + 'FINISHED' + bcolors.ENDC