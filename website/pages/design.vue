<template>
  <PageTitle>
    <template v-slot:title>Design</template>
    <template v-slot:subtitle>Decisions in hardware and software</template>
  </PageTitle>

  <article class="columns-2">
    <div class="break-after-column">
      <section class="mb-8 mx-auto px-6 container">
	<h2 class="text-3xl font-semibold mb-4 text-white">Hardware</h2>
	<p>
	  NanoBot's "brains" come from the Arduino Nano 33 IoT. It uses 2 motors, 2 infrared sensors, and Bluetooth Low Energy (BLE) to move, sense lines, and receive sensory information, respectively.
	</p>
	<p>
	  The Arduino is plugged into the Rensselaer MinSeg Kit, which serves as a motor controller to control the motors safely. This kit enabled us to control the motors, but it also caused many problems for us. We studied <a src="https://cdn.shopify.com/s/files/1/0299/1013/files/MinSegNanoStick_Pinout_R3.pdf?v=1636244432">this schematic</a> carefully, but still made several mistakes using the wrong pins. For example, in our first time installing the infrared sensors, we accidentally connected them to the same pins as the motors, which caused the sensors to change based on whether or not the motors were turning, regardless of what color was beneath the sensors.
	</p>
	<p>
	  We also struggled to get the sensors reporting the white lines properly. At first, we thought we had bought faulty sensors, so we used our electronic measurement kits, which students use in Electrical, Computer Systems Engineering (ECSE) classes, to reliably test the sensors. Using our trusted kits, we found that the sensors worked, but it still took some time for us to get the sensors working with the Arduino. After finding the right pins, we finally discovered that we had the sensors mounted at a suboptimal angle, as they prefer to point slightly forward rather than directly downward.
	</p>
	<p>
	  Additionally, we spent a long time trying to improve the accuracy of NanoBot's movement. NanoBot will inevitably have inaccuracies because motors are not perfect and they don't simply turn a set number of rotations (and even if they did, wheels are not perfectly round, surfaces are not flawlessly flat, etc.). The reality is that any robot which interacts with its enviroment has to have a way to handle error. Part of handling error is trying to minimize it as much as possible. For minimizing the error in NanoBot's motion, we first used math to calculate the scale constant to increase power to the weaker motor in order to roughly equalize the two motors. After that, we examined other sources of inconsistencies, such as the ball pivot in the front of our robot. Our original metal ball pivot was heavy and caused unpredictable friction. So, we replaced the metal ball pivot with a plastic one. TODO: FINISH THIS SECTION!
	</p>
      </section>
    </div>

    <div>
      <section class="mb-8 mx-auto px-6 container">
	<h2 class="text-3xl font-semibold mb-4 text-white">Software</h2>
	<p>
	  At a high level, NanoBot keeps track of three things: its current state, the scents it has recieved, and the best understanding of
	  the board possible from what it has learned. 
	</p>
	<p>
	  NanoBot needs to keep track of its current position and orientation on the board, to be able to rotate and move along particular paths. 
	  It does this by updating its internal state every time it takes an action such as moving or rotating. 
	</p>
	<p>
	  Similarly, it needs to keep track of the scents it has recieved, so that it can use them to make deductions about the board.
	</p>
	<p>
	  The main "intelligence" of NanoBot is in its ability to update its understanding of the board efficiently, so as to determine 
	  what might be in each tile, and plan a fast and safe route to each subsequent location. There are three key deductions that NanoBot makes 
	  when it recieves a new scent:
	  <ul class="list-inside list-decimal mt-2 ps-5 py-2">
            <li>Eliminate the possibility of any tile type not contained in the scent from adjacent positions.</li>
            <li>If glitter or stench scented, eliminate the possibility of gold or Wumpus in all non adjacent squares (since there are just one of each on the map).</li>
            <li>If NanoBot sensed something at a position and eliminated that option from 3 adjacent locations, then the 4th adjacent position must be the tile producing the scent</li>
	  </ul>
	  In games that are solvable, but only under the assumption that they are solvable, NanoBot uses several more complex heuristics to determine which risky location is the one that 
	  must be safe, based on the remaining positions where gold is possible and the elimination of paths that pass through 100% confirmed pits.
	</p>
	<p>
	  A routine opperation NanoBot needs to perform is to choose a tile to visit next and form a path to take to get there. Currently, NanoBot's metric for ranking next locations to visit is based
	  on the maximizing the expected information gained by sensing at that tile (for instance, a tile with three unknown adjacent tiles stands to provide more information than a tile with only one unknown adjacent tile),
	  and it prefers high ranked locations that are nearby, thus forming a hybrid approach between breadth first and depth first search. 
	  To compute the optimal path, NanoBot runs Djikstra's algorithm, breadth first searching outward from the target location until finding the current location, and then follows the reverse path. 
	</p>
      </section>
    </div>
  </article>

</template>
