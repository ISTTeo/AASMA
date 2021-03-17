package loadingdocks;

import java.awt.Color;

public class Block {

	public enum Shape { shelf, ramp, free }
	public Shape shape;
	public Color color;
	
	public Block(Shape shape, Color color) {
		this.shape = shape;
		this.color = color;
	}

}
