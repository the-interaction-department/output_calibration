def onValueChange(channel, sampleIndex, val, prev):
	op.Decoder.op('tex3d_captures1').par.replaceindex = val
	op.Decoder.op('tex3d_captures1').par.resetsinglepulse.pulse()
	
	
	