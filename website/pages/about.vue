<template>
<body class="">

<header class="py-8 px-8 bg-base">
    <!-- Your header content goes here -->
    <h1 class="text-4xl font-bold text-center text-white">Wumpus World Problem</h1>
    <p class="mt-2 text-lg text-center">An AI challenge in robotic perception and logical decision-making</p>
</header>

<main class="container mx-auto py-8 px-4">
    <!-- Your main content goes here -->
    <section class="mb-8">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
                <h2 class="text-3xl font-semibold mb-4 text-white">The Situation</h2>
                    <p>
		    NanoBot wakes up in the entrance of dark cave with 16 chambers (arranged in a 4x4 grid). It seeks to retrieve the gold located in one of these chambers and return to its starting point unharmed. But a Wumpus, hidden in one of the chambers, threatens to destroy NanoBot should they meet. Adding to the threat of the Wumpus, the cave is infested with inescapable pits that can trap NanoBot forever. Each chamber has doorways to its 4 adjacent chambers, which allow NanoBot to move between chambers and transmit sensory details between pits. If NanoBot is in a chamber adjacent to a pit, it feels a breeze, if next to the Wumpus, it smells a stench, and if adjacent to the gold, it sees a glitter. It can receive multiple senses at once, but cannot tell which direction the senses are coming from. Equipped with a single arrow, NanoBot can shoot its arrow into an adjacent chamber to kill the Wumpus if it is there.
                </p>
            </div>
            <div>
                <img src="" alt="Wumpus World" class="w-full">
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

</body>
</template>