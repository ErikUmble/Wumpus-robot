<template>
<PageTitle>
    <template v-slot:title>Wumpus World Problem</template>
    <template v-slot:subtitle>An AI challenge in robotic perception and logical decision-making</template>
</PageTitle>


<main class="container mx-auto py-8 px-4">
    <!-- Your main content goes here -->
    <section class="mb-8">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
                <h2 class="text-3xl font-semibold mb-4 text-white">The Situation</h2>
                    <p>
		    NanoBot wakes up in the entrance of a dark cave with 16 chambers (arranged in a 4x4 grid). It seeks to retrieve the gold in one of the chambers and return to its starting point unharmed. NanoBot has two threats: one Wumpus, hidden in one of the chambers, and any number of inescapable pits. If NanoBot runs into either the Wumpus or one of the pits, it will never escape. Each chamber has doorways to its 4 adjacent chambers, which transmit sensory details between pits. If NanoBot is in a chamber adjacent to a pit, it feels a breeze; if next to the Wumpus, it smells a stench; if adjacent to the gold, it sees a glitter. It can receive multiple senses at once, but cannot tell which direction the senses are coming from. Equipped with a single arrow, NanoBot can shoot its arrow into an adjacent chamber to kill the Wumpus if it is there.
                </p>
            </div>
            <div>
                <img src="@/assets/images/wumpus.png" alt="Wumpus World" class="w-full">
            </div>
        </div>
    </section>

    <section class="mb-8">
        <h2 class="text-3xl font-semibold mb-4 text-white">The Challenge:</h2>
        <p>
            NanoBot must navigate the cave, aoviding the pits and the Wumpus (or shooting it with its single arrow), find the gold, and return to the start using
            its memory of the cave and its senses.
        </p>
        <p>
            The actual physical challenge uses a 4x4 grid of black squares, separated by white lines, as the cave. NanoBot uses IR sensors to detect
            the boundaries. It keeps track of scents recieved by Bluetooth and logically deduces the squares that are safe to enter. 
            It adjusts for variation and discrepencies in its direction and position which are caused by its real (and therefore imperfect) hardware. Can NanoBot find a follow a logical path to retrieve the gold and get out safely?
        </p>
    </section>

</main>

</template>
