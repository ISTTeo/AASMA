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
	private Point ahead;

	public Agent(Point point, Color color){ 
		super(point, color);
	} 
	
	
	/**********************
	 **** A: decision ***** 
	 **********************/
	
	public void agentDecision() {
	  ahead = aheadPosition();
	  
	  if (isWall()) {
		  rotateRandomly();
	  } else if(isFreeCell()) {
		  if(Math.random() > .95) 
			  rotateRandomly();
		  else
			  moveAhead(); //Introduce a little anarchy
	  }
	  else if(isRamp()) {
		  if(isBoxAhead()) {
			  grabBox();
			  rotateRandomly();
		  } else {
			  rotateRandomly();
		  }
	  } else if(isShelf()) {
		  if(cargo != null && shelfColor().equals(cargoColor())) {
			  dropBox();
		  } else {
			  rotateRandomly();
		  }
	  } else {
		  //Agent ahead
		  rotateRandomly();
	  }	
	 }
	
	/********************/
	/**** B: sensors ****/
	/********************/
	
	/* Check if agent is carrying box */
	public boolean cargo() {
		return cargo != null;
	}
	
	/* Return the color of the box */
	public Color cargoColor() {
		return cargo.color;
	}

	/* Return the color of the shelf ahead or 0 otherwise */
	public Color shelfColor(){
		if(isShelf())
			return Board.getBlock(ahead).color;
		return null;
		//TODO returns Color NULL is to be returned right?
	}

	/* Check if the cell ahead is floor (which means not a wall, not a shelf nor a ramp) and there are any robot there */
	public boolean isFreeCell() {
	  if(Board.getBlock(ahead).shape.equals(Shape.free))
		  if(Board.getEntity(ahead)==null) return true;
	  return false;
	}

	/* Check if the cell ahead contains a box */
	public boolean isBoxAhead(){
		Entity entity = Board.getEntity(ahead);
		return entity!=null && entity instanceof Box;
	}

	/* Check if the cell ahead is a shelf */
	public boolean isShelf() {
	  Block block = Board.getBlock(ahead);
	  return block.shape.equals(Shape.shelf);
	}

	/* Check if the cell ahead is a ramp */
	public boolean isRamp(){
	  Block block = Board.getBlock(ahead);
	  return block.shape.equals(Shape.ramp);
	}

	/* Check if the cell ahead is a wall */
	private boolean isWall() {
		return ahead.x<0 || ahead.y<0 || ahead.x>=Board.nX || ahead.y>=Board.nY;
	}

	/**********************/
	/**** C: actuators ****/
	/**********************/

	/* Rotate agent randomly */
	public void rotateRandomly() {
		double rnd = Math.random();
		if(rnd > .75)
			rotateRight();
		else if(rnd > .5) {
			rotateRight();
			rotateRight();
		} else if (rnd > .25) {
			rotateLeft();
		}
	}
	
	/* Rotate agent to right */
	public void rotateRight() {
		direction = (direction+90)%360;
	}
	
	/* Rotate agent to left */
	public void rotateLeft() {
		direction = (direction-90)%360;
	}
	
	/* Move agent forward */
	public void moveAhead() {
		Board.updateEntityPosition(point,ahead);
		if(cargo()) cargo.moveBox(ahead);
		point = ahead;
	}

	/* Cargo box */
	public void grabBox() {
	  cargo = (Box) Board.getEntity(ahead);
	  cargo.grabBox(point);
	}

	/* Drop box */
	public void dropBox() {
		cargo.dropBox(ahead);
	    cargo = null;
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
