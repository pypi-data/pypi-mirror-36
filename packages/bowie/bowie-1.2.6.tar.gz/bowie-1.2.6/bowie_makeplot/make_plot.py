"""
Module turns gridded datasets into helpful plots. It is designed for LISA Signal-to-Noise (SNR) comparisons across sennsitivity curves and parameters, but is flexible to other needs. It is part of the BOWIE analysis tool. Author: Michael Katz. Please cite "Evaluating Black Hole Detectability with LISA" (arXiv:1807.02511) for usage of this code. 

	This code is licensed under the GNU public license. 
	
	The methods here can be called with an input dictionary or .json configuration file. The plotting classes are also importable for customization. See BOWIE_basic_examples.ipynb for examples on how to use this code. See paper_plots.ipynb for the plots shown in the paper. 

	The three main classes are plot types: Waterfall, Horizon, and Ratio. 

	Waterfall: 
		SNR contour plot based on plots from LISA Mission proposal.

	Ratio:
		Comparison plot of the ratio of SNRs for two different inputs. This plot also contains Loss/Gain contours, which describe when sources are gained or lost compared to one another based on a user specified SNR cut. See paper above for further explanation. 

	Horizon:
		SNR contour plots comparing multipile inputs. User can specify contour value. The default is the user specified SNR cut.
"""


import json
import sys
from collections import OrderedDict

import matplotlib.pyplot as plt

from bowie_makeplot.plotutils.makeprocess import MakePlotProcess

SNR_CUT = 5.0


def plot_main(pid, return_fig_ax=False):

	"""
	Main function for creating these plots. Reads in plot info dict from json file or dictionary in script. 

	Optional Inputs:
		:param return_fig_ax - (bool) - return figure and axes objects.

	Optional Outputs:
		fig: figure object - for customization outside of those in this program
		ax: axes object - for customization outside of those in this program
	"""

	global WORKING_DIRECTORY, SNR_CUT

	WORKING_DIRECTORY = '.'
	if 'WORKING_DIRECTORY' not in pid['general'].keys():
		pid['general']['WORKING_DIRECTORY'] = '.'

	SNR_CUT = 5.0
	if 'SNR_CUT' not in pid['general'].keys():
		pid['general']['SNR_CUT'] = SNR_CUT

	if "switch_backend" in pid['general'].keys():
		plt.switch_backend(pid['general']['switch_backend'])

	running_process = MakePlotProcess(pid)
	running_process.input_data()
	running_process.setup_figure()
	running_process.create_plots()
		

	#save or show figure
	if 'save_figure' in pid['general'].keys():
		if pid['general']['save_figure'] == True:
			dpi=200
			if 'dpi' in pid['general'].keys():
				dpi = pid['general']['dpi']
			running_process.fig.savefig(pid['general']['WORKING_DIRECTORY'] + '/' + 
				pid['general']['output_path'], dpi=dpi)
	
	if 'show_figure' in pid['general'].keys():
		if pid['general']['show_figure'] == True:
			plt.show()

	if return_fig_ax == True:
		return running_process.fig, running_process.ax

	return

if __name__ == '__main__':
	"""
	starter function to read in json and pass to plot_main function. 
	"""
	#read in json
	plot_info_dict = json.load(open(sys.argv[1], 'r'),
		object_pairs_hook=OrderedDict)
	plot_main(plot_info_dict)


