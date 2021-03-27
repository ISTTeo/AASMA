package loadingdocks;

import java.awt.Color;
import java.awt.Point;

public class Box extends Entity {

	public Box(Point point, Color color) {
		super(point, color);
	}
	
	/*****************************
	 ***** AUXILIARY METHODS ***** 
	 *****************************/

	public void grabBox(Point newpoint) {
		Board.removeEntity(point);
		point = newpoint;
	}
	
	public void dropBox(Point newpoint) {
		Board.insertEntity(this,newpoint);
		point = newpoint;
	}

	public void moveBox(Point newpoint) {
		point = newpoint;
	}
}
