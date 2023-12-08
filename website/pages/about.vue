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
                <h2 class="text-3xl font-semibold mb-4 text-white">The Situation...</h2>
                    <p>NanoBot wakes up in the entrance of dark cave with 16 chambers (arranged in a 4x4 grid). Its one goal in life is to retrieve the gold that resides in one 
                    of these chambers and return to its starting point without harm. But a Wupus, in one of the chambers, threatens to destroy NanoBot should it step 
                    in the Wumpus' chamber. Not only that, but the cave is infested with pits that do not allow anyone who enters to leave.
                    Each chamber has a doorway to the 4 adjacent chambers through which NanoBot can pass through, and also through which NanoBot can smell
                    sense whatever is on the other side. If NanoBot is in a chamber adjacent to a pit, it feels a breeze, if next to the Wumpus, it smells a stench,
                    and if adjacent to the gold, it sees a glitter. Note that it cannot tell which direction the scent is coming from, and it can receive 
                    multiple senses at once (if adjacent to multiple non-empty chambers). NanoBot can shoot its single arrow
                    and if it is into the chamber with the Wumpus, the Wumpus will die and the chamber becomes safe. 
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
            In a more practical sense. NanoBot must navigate a 4x4 grid of black squares, separated by white lines, using IR sensors to detect
            the boundaries. It must keep track of scents recieved by Bluetooth and logically deduce the squares that are safe to enter. 
            It must be able to rotate, adjust for variation and discrepencies in its direction, and follow its logical path without entering a 
            dangerous square. 
        </p>
    </section>

</main>

</body>
</template>