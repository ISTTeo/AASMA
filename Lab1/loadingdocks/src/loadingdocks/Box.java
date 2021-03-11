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
	
	public void getDropped(Point newPoint) {
		//TODO we dont need this unless I can set point to null and remove entity from board
		//TODO but doing so appear to give a nullptr at DisplayObjects in board / GUI 
		getMoved(newPoint);
	}
	
	public void getMoved(Point newPoint) {
		Board.updateEntityPosition(this.point, newPoint);
		this.point = newPoint;
	}
}
