package loadingdocks;

import java.awt.Color;
import java.awt.Point;
import java.util.ArrayList;
import java.util.List;
import loadingdocks.Block.Shape;

/**
 * Environment
 * @author Rui Henriques
 */
public class Board {

	/** The environment */

	public static int nX = 10, nY = 10;
	private static Block[][] board;
	private static Entity[][] objects;
	private static List<Agent> robots;
	private static List<Box> boxes;
	
	
	/****************************
	 ***** A: SETTING BOARD *****
	 ****************************/
	
	public static void initialize() {
		
		/** A: create board */
		board = new Block[nX][nY];
		for(int i=0; i<nX; i++) 
			for(int j=0; j<nY; j++) 
				board[i][j] = new Block(Shape.free, Color.lightGray);
				
		/** B: create ramp, boxes and shelves */
		int rampX = 4, rampY = 3;
		Color[] colors = new Color[] {Color.red, Color.blue, Color.green, Color.yellow};
		boxes = new ArrayList<Box>();
		for(int i=rampX, k=0; i<2*rampX; i++) {
			for(int j=0; j<rampY; j++) {
				board[i][j] = new Block(Shape.ramp, Color.gray);
				if((j==0||j==1) && (i==(rampX+1)||i==(rampX+2))) continue;
				else boxes.add(new Box(new Point(i,j), colors[k++%4]));
			}
		}
		Point[] pshelves = new Point[] {new Point(0,6), new Point(0,8), new Point(8,6), new Point(8,8)};
		for(int k=0; k<pshelves.length; k++) 
			for(int i=0; i<2; i++) 
				board[pshelves[k].x+i][pshelves[k].y] = new Block(Shape.shelf, colors[k]);
		
		/** C: create agents */
		int nrobots = 3;
		robots = new ArrayList<Agent>();
		for(int j=0; j<nrobots; j++) robots.add(new Agent(new Point(0,j), Color.pink));
		
		objects = new Entity[nX][nY];
		for(Box box : boxes) objects[box.point.x][box.point.y]=box;
		for(Agent agent : robots) objects[agent.point.x][agent.point.y]=agent;
	}
	
	/****************************
	 ***** B: BOARD METHODS *****
	 ****************************/
	
	public static Entity getEntity(Point point) {
		return objects[point.x][point.y];
	}
	public static Block getBlock(Point point) {
		return board[point.x][point.y];
	}
	public static void updateEntityPosition(Point point, Point newpoint) {
		objects[newpoint.x][newpoint.y] = objects[point.x][point.y];
		objects[point.x][point.y] = null;
	}	
	public static void removeEntity(Point point) {
		objects[point.x][point.y] = null;
	}
	public static void insertEntity(Entity entity, Point point) {
		objects[point.x][point.y] = entity;
	}

	/***********************************
	 ***** C: ELICIT AGENT ACTIONS *****
	 ***********************************/
	
	private static RunThread runThread;
	private static GUI GUI;

	public static class RunThread extends Thread {
		
		int time;
		
		public RunThread(int time){
			this.time = time*time;
		}
		
	    public void run() {
	    	while(true){
	    		step();
				try {
					sleep(time);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
	    	}
	    }
	}
	
	public static void run(int time) {
		Board.runThread = new RunThread(time);
		Board.runThread.start();
	}

	public static void reset() {
		removeObjects();
		initialize();
		GUI.displayBoard();
		displayObjects();	
		GUI.update();
	}

	public static void step() {
		removeObjects();
		for(Agent a : robots) a.agentDecision();
		displayObjects();
		GUI.update();
	}

	public static void stop() {
		runThread.interrupt();
		runThread.stop();
	}

	public static void displayObjects(){
		for(Agent agent : robots) GUI.displayObject(agent);
		for(Box box : boxes) GUI.displayObject(box);
	}
	
	public static void removeObjects(){
		for(Agent agent : robots) GUI.removeObject(agent);
		for(Box box : boxes) GUI.removeObject(box);
	}
	
	public static void associateGUI(GUI graphicalInterface) {
		GUI = graphicalInterface;
	}
}
