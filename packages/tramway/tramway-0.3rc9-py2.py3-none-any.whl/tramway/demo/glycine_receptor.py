
import os
import sys
from tramway.helper import tesselate, find_imt, infer, map_plot, cell_plot
import warnings

short_description = 'infer and plot gwr-based diffusivity and potential maps for the glycine receptor dataset'

data_server = 'http://dl.pasteur.fr/fop/jod5vvB5/'
data_file = 'glycine_receptor.trxyt'
data_dir = ''


methods = ['grid', 'kdtree', 'kmeans', 'gwr']
default_localization_error = 0.001
default_prior_diffusivity = 0.01
default_prior_potential = 0.1


arguments = [
	('--grid',	dict(help='regular grid mesh', action='store_true')),
	('--kdtree',	dict(help='kd-tree mesh', action='store_true')),
	('--kmeans',	dict(help='k-means mesh', action='store_true')),
	('--gwr',	dict(help='growing-when-required-based mesh (default)', action='store_true', default=True)),
	('-ll',	dict(help='plot locations (low resolution image)', action='store_true')),
	('-lh',	dict(help='plot locations (high resolution image)', action='store_true')),
	('-ml',	dict(help='plot mesh (low resolution image)', action='store_true')),
	('-mh',	dict(help='plot mesh (high resolution image)', action='store_true')),
	('-d',	dict(help='D inference mode', action='store_true')),
	('-dd',	dict(help='DD inference mode', action='store_true')),
	('-df',	dict(help='DF inference mode (default)', action='store_true')),
	('-dv',	dict(help='DV inference mode', action='store_true')),
	(('--localization-error', '-le'), dict(help='localization error', type=float, default=default_localization_error)),
	(('--prior-diffusivity', '-pd'), dict(help='prior diffusivity', type=float, default=default_prior_diffusivity)),
	(('--prior-potential', '-pv'), dict(help='prior potential', type=float, default=default_prior_potential))]


def main(**kwargs):

	#warnings.simplefilter('error')

	local = os.path.join(data_dir, data_file)
	if not os.path.isfile(local):
		print("cannot find file: {}".format(local))
		sys.exit(1)

	output_basename, _ = os.path.splitext(local)

	# determine which tesselation method
	method = None
	for m in methods:
		if kwargs.get(m, False):
			method = m
			break
	if not method:
		method = methods[-1]

	def out(method, extension):
		return '{}.{}{}'.format(output_basename, method, extension)

	# tesselate
	tesselation_file = out(method, '.rwa')
	if not os.path.isfile(tesselation_file):
		mesh = tesselate(local, method, output_file=tesselation_file, \
			verbose=True, strict_min_cell_size=10)

	# plot locations and meshes
	pt_size_low, pt_size_high = 8, 6
	res_low, res_high = 200, 400
	if kwargs.get('ll', False):
		cell_plot(tesselation_file, output_file='gr_locations_low.png',
			verbose=True, voronoi=False,
			locations=dict(color=['k']*9999, size=pt_size_low), dpi=res_low)
	if kwargs.get('lh', False):
		cell_plot(tesselation_file, output_file='gr_locations_high.png',
			verbose=True, voronoi=False,
			locations=dict(color=['k']*9999, size=pt_size_high), dpi=res_high)
	if kwargs.get('ml', False):
		cell_plot(tesselation_file, output_file='gr_{}_low.png'.format(method),
			verbose=True, voronoi=False,
			delaunay=dict(color='kkk', linewidth=2, centroid_style=None),
			locations=dict(color='light', size=pt_size_low), dpi=res_low)
	if kwargs.get('mh', False):
		cell_plot(tesselation_file, output_file='gr_{}_high.png'.format(method),
			verbose=True,
			delaunay=dict(color='kkk', linewidth=1, centroid_style=None),
			voronoi=dict(color='yyyy', linewidth=.5, centroid_style=None,
				negative=True),
			locations=dict(color='light', size=pt_size_high), dpi=res_high)

	# determine which inference modes
	_d  = kwargs.get('d',  False)
	_dd = kwargs.get('dd', False)
	_df = kwargs.get('df', False)
	_dv = kwargs.get('dv', False)
	if not any((_d, _dd, _df, _dv)):
		_df = True

	localization_error = kwargs.get('locatization_error', default_localization_error)
	priorD = kwargs.get('prior_diffusivity', default_prior_diffusivity)
	priorV = kwargs.get('prior_potential', default_prior_potential)

	# infer and plot maps
	if _d:
		D = infer(tesselation_file, mode='D', localization_error=localization_error)
		map_plot(D, output_file=out(method, '.d.png'), show=True)

	if _df:
		DF = infer(tesselation_file, mode='DF', localization_error=localization_error)
		map_plot(DF, output_file=out(method, '.df.png'), show=True, clip=.99) 

	if _dd:
		DD = infer(tesselation_file, mode='DD', localization_error=localization_error, \
			priorD=priorD)
		map_plot(DD, output_file=out(method, '.dd.png'), show=True)

	if _dv:
		DV = infer(tesselation_file, mode='DV', localization_error=localization_error, \
			priorD=priorD, priorV=priorV)
		map_plot(DV, output_file=out(method, '.dv.png'), show=True)

	sys.exit(0)


if __name__ == '__main__':
	main()

