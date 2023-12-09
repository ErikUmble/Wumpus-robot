<template>
    <PageTitle>
        <template v-slot:title>Design</template>
        <template v-slot:subtitle>Decisions in hardware and software</template>
    </PageTitle>

    <section class="mb-8 mx-auto container">
        <h2 class="text-3xl font-semibold mb-4 text-white">NanoBot: Hardware</h2>
        <p>
            TODO: add details of how the robot works physically, and design decisions made along the way
        </p>
        
    </section>

    <section class="mb-8 mx-auto container py-2">
        <h2 class="text-3xl font-semibold mb-4 text-white">NanoBot: Algorithm</h2>
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
            <ul class="list-inside list-disc mt-2 ps-5 py-2">
                <li>1. Eliminate the possibility of any tile type not contained in the scent from adjacent positions.</li>
                <li>2. If glitter or stench scented, eliminate the possibility of gold or Wumpus in all non adjacent squares (since there are just one of each on the map).</li>
                <li>3. If NanoBot sensed something at a position and eliminated that option from 3 adjacent locations, then the 4th adjacent position must be the tile producing the scent</li>
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

</template>