/* 
 * stoplight.c
 *
 * 31-1-2003 : GWA : Stub functions created for CS161 Asst1.
 *
 * NB: You can use any synchronization primitives available to solve
 * the stoplight problem in this file.
 */


/*
 * 
 * Includes
 *
 */

#include <types.h>
#include <lib.h>
#include <test.h>
#include <thread.h>
#include <synch.h>

/*
 *
 * Constants
 *
 */

/*
 * Number of cars created.
 */

#define NCARS 20


/*
 *
 * Function Definitions
 *
 */

// Locks for each part of the intersection
struct lock* NE;     // Lock for North East Corner 
struct lock* NW;     // Lock for North West Corner 
struct lock* SE;     // Lock for South East Corner 
struct lock* SW;     // Lock for South West Corner 

struct semaphore* intersectionSem;      //Allows only 3 cars to be in the intersection

static const char *directions[] = { "N", "E", "S", "W" };

static const char *msgs[] = {
        "approaching:",
        "region1:    ",
        "region2:    ",
        "region3:    ",
        "leaving:    "
};

/* use these constants for the first parameter of message */
enum { APPROACHING, REGION1, REGION2, REGION3, LEAVING };

static void
message(int msg_nr, int carnumber, int cardirection, int destdirection)
{
        kprintf("%s car = %2d, direction = %s, destination = %s\n",
                msgs[msg_nr], carnumber,
                directions[cardirection], directions[destdirection]);
}
 
/*
 * gostraight()
 *
 * Arguments:
 *      unsigned long cardirection: the direction from which the car
 *              approaches the intersection.
 *      unsigned long carnumber: the car id number for printing purposes.
 *
 * Returns:
 *      nothing.
 *
 * Notes:
 *      This function should implement passing straight through the
 *      intersection from any direction.
 *      Write and comment this function.
 */

static
void
gostraight(unsigned long cardirection,
           unsigned long carnumber,
           unsigned long destdirection )
{
    if( cardirection == 0 ) {   //North
        P(intersectionSem);
        lock_acquire(NW);
        message( APPROACHING, carnumber, cardirection, destdirection);
        message( REGION1, carnumber, cardirection, destdirection );
        
        lock_acquire(SW);
        message( REGION2, carnumber, cardirection, destdirection );
        message( LEAVING, carnumber, cardirection, destdirection );
        lock_release(NW);
        lock_release(SW); 
        V(intersectionSem);
    }
    if( cardirection == 1 ) {   //East
        P(intersectionSem);
        lock_acquire(NE);
        message( APPROACHING, carnumber, cardirection, destdirection);
        message( REGION1, carnumber, cardirection, destdirection );
        
        lock_acquire(NW);
        message( REGION2, carnumber, cardirection, destdirection );
        message( LEAVING, carnumber, cardirection, destdirection );
        lock_release(NE);
        lock_release(NW);
        V(intersectionSem);
    }
    if( cardirection == 2 ) {   //South
        P(intersectionSem);
        lock_acquire(SE);
        message( APPROACHING, carnumber, cardirection, destdirection);
        message( REGION1, carnumber, cardirection, destdirection );
        
        lock_acquire(NE);
        message( REGION2, carnumber, cardirection, destdirection );
        message( LEAVING, carnumber, cardirection, destdirection );
        lock_release(SE);
        lock_release(NE);
        V(intersectionSem);
    }
    if( cardirection == 3 ) {   //West
        P(intersectionSem);
        lock_acquire(SW);
        message( APPROACHING, carnumber, cardirection, destdirection);
        message( REGION1, carnumber, cardirection, destdirection );
        
        lock_acquire(SE);
        message( REGION2, carnumber, cardirection, destdirection );
        message( LEAVING, carnumber, cardirection, destdirection );
        lock_release(SW);
        lock_release(SE);
        V(intersectionSem);
    }
}

/*
 * turnleft()
 *
 * Arguments:
 *      unsigned long cardirection: the direction from which the car
 *              approaches the intersection.
 *      unsigned long carnumber: the car id number for printing purposes.
 *
 * Returns:
 *      nothing.
 *
 * Notes:
 *      This function should implement making a left turn through the 
 *      intersection from any direction.
 *      Write and comment this function.
 */

static
void
turnleft(unsigned long cardirection,
         unsigned long carnumber,
         unsigned long destdirection)
{
    if( cardirection == 0 ) {   //North
        P(intersectionSem);
        lock_acquire(NW);
        message( APPROACHING, carnumber, cardirection, destdirection);
        message( REGION1, carnumber, cardirection, destdirection );
        
        lock_acquire(SW);
        message( REGION2, carnumber, cardirection, destdirection );
        lock_release(NW);
        
        lock_acquire(SE);
        message( REGION3, carnumber, cardirection, destdirection );
        message( LEAVING, carnumber, cardirection, destdirection );
        lock_release(SW); 
        lock_release(SE); 
        V(intersectionSem);
    }
    if( cardirection == 1 ) {   //East
        P(intersectionSem);
        lock_acquire(NE);
        message( APPROACHING, carnumber, cardirection, destdirection);
        message( REGION1, carnumber, cardirection, destdirection );
        
        lock_acquire(NW);
        message( REGION2, carnumber, cardirection, destdirection );
        lock_release(NE);
        
        lock_acquire(SW);
        message( REGION3, carnumber, cardirection, destdirection );
        message( LEAVING, carnumber, cardirection, destdirection );
        lock_release(NW);
        lock_release(SW);
        V(intersectionSem);
    }
    if( cardirection == 2 ) {   //South
        P(intersectionSem);
        lock_acquire(SE);
        message( APPROACHING, carnumber, cardirection, destdirection);
        message( REGION1, carnumber, cardirection, destdirection );
        
        lock_acquire(NE);
        message( REGION2, carnumber, cardirection, destdirection );
        lock_release(SE);
        
        lock_acquire(NW);
        message( REGION3, carnumber, cardirection, destdirection );
        message( LEAVING, carnumber, cardirection, destdirection );
        lock_release(NE);
        lock_release(NW);
        V(intersectionSem);
    }
    if( cardirection == 3 ) {   //West
        P(intersectionSem);
        lock_acquire(SW);
        message( APPROACHING, carnumber, cardirection, destdirection);
        message( REGION1, carnumber, cardirection, destdirection );
        
        lock_acquire(SE);
        message( REGION2, carnumber, cardirection, destdirection );
        lock_release(SW);
        
        lock_acquire(NE);
        message( REGION3, carnumber, cardirection, destdirection );
        message( LEAVING, carnumber, cardirection, destdirection );
        lock_release(SE);
        lock_release(NE);
        V(intersectionSem);
    }
}


/*
 * turnright()
 *
 * Arguments:
 *      unsigned long cardirection: the direction from which the car
 *              approaches the intersection.
 *      unsigned long carnumber: the car id number for printing purposes.
 *
 * Returns:
 *      nothing.
 *
 * Notes:
 *      This function should implement making a right turn through the 
 *      intersection from any direction.
 *      Write and comment this function.
 */

static
void
turnright(unsigned long cardirection,
          unsigned long carnumber,
          unsigned long destdirection)
{
    if( cardirection == 0 ) {   //North
        P(intersectionSem);
        lock_acquire(NW);
        message( APPROACHING, carnumber, cardirection, destdirection);
        message( REGION1, carnumber, cardirection, destdirection );
        message( LEAVING, carnumber, cardirection, destdirection );
        lock_release(NW); 
        V(intersectionSem);
    }
    if( cardirection == 1 ) {   //East
        P(intersectionSem);
        lock_acquire(NE);
        message( APPROACHING, carnumber, cardirection, destdirection);
        message( REGION1, carnumber, cardirection, destdirection );
        message( LEAVING, carnumber, cardirection, destdirection );
        lock_release(NE);
        V(intersectionSem);
    }
    if( cardirection == 2 ) {   //South
        P(intersectionSem);
        lock_acquire(SE);
        message( APPROACHING, carnumber, cardirection, destdirection);
        message( REGION1, carnumber, cardirection, destdirection );
        message( LEAVING, carnumber, cardirection, destdirection );
        lock_release(SE);
        V(intersectionSem);
    }
    if( cardirection == 3 ) {   //West
        P(intersectionSem);
        lock_acquire(SW);
        message( APPROACHING, carnumber, cardirection, destdirection);
        message( REGION1, carnumber, cardirection, destdirection );
        message( LEAVING, carnumber, cardirection, destdirection );
        lock_release(SW);
        V(intersectionSem);
    }
}


/*
 * approachintersection()
 *
 * Arguments: 
 *      void * unusedpointer: currently unused.
 *      unsigned long carnumber: holds car id number.
 *
 * Returns:
 *      nothing.
 *
 * Notes:
 *      Change this function as necessary to implement your solution. These
 *      threads are created by createcars().  Each one must choose a direction
 *      randomly, approach the intersection, choose a turn randomly, and then
 *      complete that turn.  The code to choose a direction randomly is
 *      provided, the rest is left to you to implement.  Making a turn
 *      or going straight should be done by calling one of the functions
 *      above.
 */
 
static
void
approachintersection(void * unusedpointer,
                     unsigned long carnumber)
{
    int cardirection;
    int destdirection;
    int turnType;
    /*
     * Avoid unused variable and function warnings.
     */

    (void) unusedpointer;
    (void) carnumber;
	(void) gostraight;
	(void) turnleft;
	(void) turnright;

    /*
     * cardirection is set randomly.
     */

    /* 0 = turn right
     * 1 = go straight
     * 2 = turn left
     */
    cardirection = random() % 4;
    turnType = random() % 3;
    
    if(turnType==0)
        destdirection=(cardirection+3)%4;
    else if(turnType==1)
        destdirection=(cardirection+2)%4;
    else if(turnType == 2)
        destdirection=(cardirection+1)%4;
    
    if(turnType == 0) {
        turnright(cardirection, carnumber, destdirection);       
    }
    else if(turnType == 1) {
        gostraight(cardirection, carnumber, destdirection);       
    }
    else if(turnType == 2) {
        turnleft(cardirection, carnumber, destdirection);       
    }
    else {
        assert(0);
    }
}


/*
 * createcars()
 *
 * Arguments:
 *      int nargs: unused.
 *      char ** args: unused.
 *
 * Returns:
 *      0 on success.
 *
 * Notes:
 *      Driver code to start up the approachintersection() threads.  You are
 *      free to modiy this code as necessary for your solution.
 */

int
createcars(int nargs,
           char ** args)
{
    int index, error;

    /*
     * Avoid unused variable warnings.
     */

    (void) nargs;
    (void) args;
     
    NW = lock_create("NW"); 
    NE = lock_create("NE"); 
    SW = lock_create("SW"); 
    SE = lock_create("SE"); 
    
    intersectionSem = sem_create("intersectionSem", 3);
    /*
     * Start NCARS approachintersection() threads.
     */
    for (index = 0; index < NCARS; index++) {

            error = thread_fork("approachintersection thread",
                                NULL,
                                index,
                                approachintersection,
                                NULL
                                );

            /*
             * panic() on error.
             */

            if (error) {
                    
                    panic("approachintersection: thread_fork failed: %s\n",
                          strerror(error)
                          );
            }
    }

    return 0;
}


