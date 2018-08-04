class Grid_generator:
	def __init__(self):
		self.Init_constants()

	def Init_constants(self):
		"""Set all member variables which may have changes after __init__ is called"""

		self.constants = op('select_output_info')
		self.grid_data = op('table_grid_data')
		self.destination_grid = op('table_points')
		self.c2p = op('null_c2p')
		self.grid_geometry = op('grid1')		
		self.bits_not_used_x = self.constants['bits_x'].eval() - self.constants['bits_to_use'].eval()
		self.bits_not_used_y = self.constants['bits_y'].eval() - self.constants['bits_to_use'].eval()
		self.grid_spacing_x = 2**self.bits_not_used_x
		self.grid_spacing_y = 2**self.bits_not_used_y
		self.num_rows = math.floor(self.constants['height'] / self.grid_spacing_y)
		self.num_cols = math.floor(self.constants['width'] / self.grid_spacing_x)
		self.placeholder_points_grid = op('sopto_points_placeholder')

	def Init_grid(self):
		"""Initialize the grid with the correct number of rows and columns"""

		print('Initializing grid with {}x{} pixel blocks'.format(self.grid_spacing_x, self.grid_spacing_y))
		
		# Setup the SOP
		self.grid_geometry.par.rows = self.num_rows
		self.grid_geometry.par.cols = self.num_cols
		self.grid_data.clear(keepFirstRow=True)

		# Set the center (i.e. the position which will store the UV coordinate)
		for y in range(self.num_rows):
			for x in range(self.num_cols):
				center_x = self.grid_spacing_x * x + self.grid_spacing_x // 2
				center_y = self.grid_spacing_y * y + self.grid_spacing_y // 2
				self.grid_data.appendRow([center_x, center_y, 0, 0, 0])

	def Process_grid(self, verbose=False):
		"""Loop through every pixel in the c2p and build the correspondence between projector and camera pixels"""

		for cpx in range(self.c2p.width):
			for cpy in range(self.c2p.height):
				# cpx and cpy are camera image pixel (from lower left) the projector pixels are encoded in the r and g channels
				ppx, ppy, _, _ = self.c2p.sample(x=cpx, y=cpy)

				# Many camera pixels do not store projector pixels - skip these
				if not ppx or not ppy:
					continue

				# Figure out which grid cell this corresponds to
				cell_x = int(ppx // self.grid_spacing_x)
				cell_y = int(ppy // self.grid_spacing_y)
				
				if verbose:
					print('projector pixel ({},{}) corresponds to grid cell ({}, {})'.format(ppx, ppy, cell_x, cell_y))
				
				# Skip the table header
				table_row = cell_x + cell_y * self.num_cols + 1
				
				self.grid_data[table_row, 'cpx'] = int(self.grid_data[table_row, 'cpx'].val) + cpx	
				self.grid_data[table_row, 'cpy'] = int(self.grid_data[table_row, 'cpy'].val) + cpy
				self.grid_data[table_row, 'count'] = int(self.grid_data[table_row, 'count'].val) + 1		

	def Compute_averages(self):
		"""Compute the average of every cell, which should give an approximation of the average"""

		minimum_centroid_size = 4

		# TODO: check to see if at least 4 camera pixels correspond 
		# to this projector pixel, i.e. that the 'count' column is
		# 4 or greater

		for row_index in range(1, self.grid_data.numRows):
			count = int(self.grid_data[row_index, 'count'].val)

			if count:
				self.grid_data[row_index, 'cpx'] = float(self.grid_data[row_index, 'cpx'].val) / count
				self.grid_data[row_index, 'cpy'] = float(self.grid_data[row_index, 'cpy'].val) / count

	def Copy_points(self):
		"""Replace the placeholder grid with one made from this data"""

		self.destination_grid.text = self.placeholder_points_grid.text

	def Setup_grid_uvs(self):
		"""Get the UV coordinate for each point on the grid"""

		for row_index in range(1, self.grid_data.numRows):
			uv_x = float(self.grid_data[row_index, 'cpx'].val) / self.c2p.width
			uv_y = float(self.grid_data[row_index, 'cpy'].val) / self.c2p.height
			
			# Cells that do not have values are set to -1 (this creates holes)			
			if uv_x == 0.0 and uv_y == 0.0:
				uv_x = -1.0
				uv_y = -1.0
				
			self.destination_grid[row_index, 'uv(0)'] = uv_x
			self.destination_grid[row_index, 'uv(1)'] = uv_y

	def Execute_all(self):
		"""Convenience method that calls all steps"""

		self.Init_constants()
		self.Init_grid()
		self.Process_grid()
		self.Compute_averages()
		self.Copy_points()
		self.Setup_grid_uvs()