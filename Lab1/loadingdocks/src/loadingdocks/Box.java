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
	
	public void getPicked() {
		//TODO
	}
	
	public void getDropped() {
		//TODO
	}
	
	public void getMoved(Point newPoint) {
		Board.updateEntityPosition(this.point, newPoint);
		this.point = newPoint;
	}
}
