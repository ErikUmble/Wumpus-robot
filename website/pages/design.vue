<template>
  <PageTitle>
    <template v-slot:title>Design</template>
    <template v-slot:subtitle>Decisions in hardware and software</template>
  </PageTitle>

  <article class="columns-1">
    <div>
      <section class="mb-8 mx-auto px-6 container">
	<h2 class="text-3xl font-semibold mb-4 text-white">Hardware</h2>
	<p>
	  NanoBot's "brains" come from the Arduino Nano 33 IoT. It uses 2 motors, 2 infrared sensors, and Bluetooth Low Energy (BLE) to move, sense lines, and receive sensory information, respectively.
	</p>
	<img src="@/assets/images/nanobot.png" alt="NanoBot" class="w-auto bg-base" style="max-height: 80vh;">
	<p>
	  The Arduino is inserted into the Rensselaer MinSeg Kit, which serves as a motor controller. This kit enabled us to safely control the motors, but it also caused many problems for us. We studied <a src="https://cdn.shopify.com/s/files/1/0299/1013/files/MinSegNanoStick_Pinout_R3.pdf?v=1636244432">this schematic</a> carefully, but still made several mistakes using the wrong pins. For example, in our first time installing the infrared sensors, we accidentally connected them to the same pins as the motors, which caused the sensors to change based on whether or not the motors were turning, rather than what color was beneath the sensors.
	</p>
	<p>
	  We also struggled to get the sensors reporting the white lines properly. At first, we thought we had bought faulty sensors, so we used our electronic measurement kits from our Electrical, Computer Systems Engineering (ECSE) classes to reliably test the sensors, and found that they worked! However, it took some time for us to get them working with the Arduino. After finding the right pins, we finally discovered that the sensors were very particular about their angle being downward and slightly forward.
	</p>
	<p>
	  Additionally, we spent a long time trying to improve the accuracy of NanoBot's movement. As with any robot, NanoBot will inevitably have to correct for error because motors and other electronics are not perfect (and even if they were, wheels are not perfectly round, surfaces are not flawlessly flat, etc.). To minimize our error, we first calculated the scale constant to increase power to the weaker motor in order to roughly equalize the two. After that, we examined other sources of inconsistencies, such as the ball pivot in the front of our robot. The original metal ball pivot was heavy and caused unpredictable friction. So, we replaced the metal ball pivot with a plastic one. The plastic pivot works with much lower friction, leading to smaller random error! A final change we made to improve NanoBot's movement was to add weight to the back of the robot where the wheels are, thereby increasing their friction (grip) on the floor. This prevented them from slipping even as they made small or quick adjustments.
	</p>
	<img src="@/assets/images/nano_pinout.webp" alt="Robot" class="w-auto m-2 py-2" style="max-height: 80vh;">
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
	  NanoBot needs to keep track of its current position and orientation on the board to be able to rotate and move along paths. 
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
            <li>Eliminate from adjacent positions the possibility of any tile type not contained in the scent.</li>
            <li>If the sense is glitter or stench, eliminate the possibility of gold or Wumpus in all non adjacent squares (since there are just one of each on the map).</li>
            <li>If NanoBot sensed something at a position and eliminated that option from 3 adjacent locations, then the 4th adjacent position must be the tile producing the scent</li>
	  </ul>
	  <div class="items-center justify-center">	    
		<img src="@/assets/images/knowledge_animation.gif" alt="Knowledge Progression" class="w-auto" style="max-height: 80vh;">
	  </div>
	  In games that are solvable only with the assumption that they are solvable, NanoBot uses several more complex heuristics to determine which unknown location is the one that 
	  must be safe, based on the remaining positions where gold is possible and the elimination of paths that pass through confirmed pits.
	</p>
	<p>
	  A routine operation NanoBot needs to perform is to choose a tile to visit next and form a path to take to get there. Currently, NanoBot's metric for ranking next locations to visit is based
	  on the maximizing the expected information gained by sensing at that tile (for instance, a tile with three unknown adjacent tiles stands to provide more information than a tile with only one unknown adjacent tile),
	  and it prefers high ranked locations that are nearby, thus forming a hybrid approach between breadth first and depth first search. 
	  To compute the optimal path, NanoBot runs Djikstra's algorithm: a breadth first searching outward from the target location until finding the current location. It then follows the reverse path. 
	</p>
      </section>
    </div>
  </article>

</template>
