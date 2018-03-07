def onValueChange(channel, sampleIndex, val, prev):
	op('tex3d_captures').par.replaceindex = val
	op('tex3d_captures').par.resetsinglepulse.pulse()
	
	
	