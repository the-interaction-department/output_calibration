def onValueChange(channel, sampleIndex, val, prev):
	# Make sim show the patterns
	op.Projector_outputs.op('switch_projection_map').par.index = 0

	# Capture first image
	op('tex3d_captures').par.resetpulse.pulse()
	op('tex3d_captures').par.replaceindex = 0
	op('tex3d_captures').par.resetsinglepulse.pulse()
