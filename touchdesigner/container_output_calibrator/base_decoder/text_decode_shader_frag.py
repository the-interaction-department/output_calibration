uniform vec2 u_total_bits;
uniform int u_usable_bits;
uniform vec2 u_projector_res;
uniform float u_threshold = 0.5;
out vec4 o_color;

// Reconstructs the gray code for the current pixel (MSB to LSB).
// Performs thresholding
//
// Parameters:
// `number_of_bits`: the number of bits used along the current axis
// `offset`: an integer slice offset into the texture 3D containing captures
uint get_gray(int number_of_bits, int offset)
{
	uint gray = 0;
	int valid_patterns = u_usable_bits * 2;
	
	for (int i = 0; i < valid_patterns; i += 2)
	{
		int array_slice = offset + i;
		float pixel_org = texture(sTD2DArrayInputs[0], vec3(vUV.st, array_slice)).r;
		float pixel_inv = texture(sTD2DArrayInputs[0], vec3(vUV.st, array_slice + 1)).r;

		float diff = pixel_org - pixel_inv;

		if (diff > u_threshold) 
		{
			gray ^= 1;
		}
		// TODO: Implement inverses
		// else if (pixel > -threshold)
		// {
		// 	pixel is REJECTED: set it to -1.0
		// }

		if (i < number_of_bits - 2) 
		{
			gray <<= 1;
		}
	} 

	return gray;
}

uint gray_to_binary(uint num)
{
    uint mask = num;
    while (mask != 0)
    {
        mask >>= 1;
        num ^= mask;
    }
    return num;
}

void main()
{
	vec4 color = vec4(-1.0);

	// The number of patterns per axis times 2 (for the inverse)
	// These are the same and would only differ in extreme
	int col_res = int(u_usable_bits) * 2;
	int row_res = int(u_usable_bits) * 2; 

	// Get the value as calculated from the patterns and convert to binary
	uint gray_col = get_gray(col_res, 0);
	uint gray_row = get_gray(row_res, col_res);
	uint val_col = gray_to_binary(gray_col);
	uint val_row = gray_to_binary(gray_row);

	// Scale color from 0->1 then scale to native projector resolution
	color = vec4(val_col, val_row, 0.0, 1.0);
	color.xy /= max(u_projector_res.x, u_projector_res.y);
	color.xy *= u_projector_res;

	o_color = color;
}