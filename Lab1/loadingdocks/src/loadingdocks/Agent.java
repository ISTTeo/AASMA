package loadingdocks;

import java.awt.Color;
import java.awt.Point;
import loadingdocks.Block.Shape;

/**
 * Agent behavior
 * @author Rui Henriques
 */
public class Agent extends Entity {

	public int direction = 90;
	public Box cargo;

	public Agent(Point point, Color color){ 
		super(point, color);
	} 
	
	
	/**********************
	 **** A: decision ***** 
	 **********************/
	
	public void agentDecision() {
	  if(this.cargo == null && this.direction == 180 && this.point.x == 0 && this.point.y == 0) {
		  this.direction = 90;
		  //TODO chill > I cant make it stop unless I can memorize what I did
	  } else if(isWall()) {
		  this.direction = 0;
	  } 
	  else if(isFreeCell()) {
		  moveAhead();
	  } else if(isRamp()) {
		  //TPDP pickup
		  Entity isItABox = Board.getEntity(aheadPosition());
		  Box okayItsABox = (Box) isItABox; 
		  this.cargo = okayItsABox;
		  //this.cargo.getPicked();
		  this.direction = 270;
	  } else if(isShelf()) {
		  //TODO place
		  if(this.cargo != null) {
			  
			  this.cargo.getDropped(aheadPosition());
			  
			  this.cargo = null;
		  }
		  this.direction = 180;
	  }
	}
	
	/********************/
	/**** B: sensors ****/
	/********************/
	
	/* Check if the cell ahead is floor (which means not a wall, not a shelf nor a ramp) and there are any robot there */
	protected boolean isFreeCell() {
	  Point ahead = aheadPosition();
	  return Board.getBlock(ahead).shape.equals(Shape.free);
	}

	/* Check if the cell ahead is a wall */
	protected boolean isWall() {
		Point ahead = aheadPosition();
		return ahead.x<0 || ahead.y<0 || ahead.x>=Board.nX || ahead.y>=Board.nY;
	}
	
	protected boolean isRamp() {
	  Point ahead = aheadPosition();
	  return Board.getBlock(ahead).shape.equals(Shape.ramp);
	}
	
	protected boolean isShelf() {
	  Point ahead = aheadPosition();
	  return Board.getBlock(ahead).shape.equals(Shape.shelf);
	}

	/**********************/
	/**** C: actuators ****/
	/**********************/
	/* Move agent forward */
	public void moveAhead() {
		Point oldPos = this.point;
		Point ahead = aheadPosition();
		Board.updateEntityPosition(point,ahead);
		point = ahead;
		
		if(this.cargo != null) {
			//TODO should the agent bring the box after him? Cant be in same pos right?
			this.cargo.getMoved(oldPos);
		}
	}
	
	/**********************/
	/**** D: auxiliary ****/
	/**********************/

	/* Position ahead */
	private Point aheadPosition() {
		Point newpoint = new Point(point.x,point.y);
		switch(direction) {
			case 0: newpoint.y++; break;
			case 90: newpoint.x++; break;
			case 180: newpoint.y--; break;
			default: newpoint.x--; 
		}
		return newpoint;
	}
}
