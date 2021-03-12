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
	
	public void getPicked(Point newPoint) {
		//TODO useless the way I did it
		Board.removeEntity(this.point);
		this.point = newPoint;
	}
	
	public void getDropped(Point newPoint) {
		//TODO we dont need this unless I can set point to null and remove entity from board
		//TODO but doing so appear to give a nullptr at DisplayObjects in board / GUI 
		Board.insertEntity(this, newPoint);
		this.point = newPoint;
	}
	
	public void getMoved(Point newPoint) {
		//Board.updateEntityPosition(this.point, newPoint);
		this.point = newPoint;
	}
}
