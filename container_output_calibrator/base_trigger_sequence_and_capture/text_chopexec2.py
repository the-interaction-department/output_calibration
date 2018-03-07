def onValueChange(channel, sampleIndex, val, prev):
	# Make sim show the patterns
	op.Scene.op('switch_projection_map').par.index = 0

	# Capture first image
	op('tex3d_captures1').par.resetpulse.pulse()
	op('tex3d_captures1').par.replaceindex = 0
	op('tex3d_captures1').par.resetsinglepulse.pulse()
