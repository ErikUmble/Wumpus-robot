<template>
    <PageTitle>
        <template v-slot:title>Discussion</template>
        <template v-slot:subtitle>Comparing NanoBot with its competition and AI in general</template>
    </PageTitle>
    <main class="container mx-auto py-8 px-4">
	  <section class="mb-8">
            <h2 class="text-3xl font-semibold mb-4 text-white">How'd We Do?</h2>
	    <p>
	      With the passing of the LEGO Mindstorms kits, we didn't have any competitors this year. But viewing footage from past challenges, here's how we compare:
	    </p>
	    <br />
		<div class="flex flex-col md:flex-row">
			<div class="container px-4 py-2">
				<span class="text-center text-white text-lg">Accomplishments</span>
				<ul class="list-disc">
				  <li>Our line-based error correction was accurate enough to usually avoid serious accumulated error.</li>
				  <li>Successfully completed an easy board, a medium, and two hard ones (before the battery died).</li>
				  <li>Passed all test cases (including the hardest level) in the algorithm tests. Also demonstrated more sophisticated reasoning such as considering distance and the new information NanoBot could learn when selecting the next square to move to.</li>
				  <li>We only shoot the Wumpus when we have to (Peace First&#x2122;)</li>
				  <li>Our algorithm was lightweight and quick. It executed with no delay and used small storage to fit on the Arduino Nano's drives.</li>
				  
				</ul>
			</div>
			<div class="container px-4 py-2">
			  <span class="text-center text-white text-lg">Future Improvements</span>
			  <ul class="list-disc">
				  <li>It should be possible to maintain that level of error correction and do so without as many pauses and readjustments.</li>
				  <li>Turning should be able to happen faster rather than correcting for so long. <span class="italic">Note: in the past, Mindstorms' software handled all of the behind-the-scenes work with encoder feedback loops to get the motors to their proper positions. We attempted to recreate this in our limited timeline, which is why our feedback loops are not as advanced.</span></li>
				  <li>When pathfinding, prefer to continue in the same direction. This will minimize error caused by turning.</li>
				  <li>Complete all of the boards in fewer attempts.</li>
			  </ul>
			</div>
		</div>
		
	  </section>
	  <section class="mb-8">
            <h2 class="text-3xl font-semibold mb-4 text-white">Related to Class</h2>
	    <span class="text-white text-lg">Intelligence</span>
	    <p>
	      Intelligence is multifaceted. NanoBot displays spacial intelligence as it is able to keep track of its position and orientation and perceive its environment to make corrections to its understanding. This enabled it to generally move to its intended destination. We also think NanoBot displays logical intelligence as it is able to make deductions about the board, and navigate it in nontrivial ways. For example, NanoBot is able to able to determine where particular scents come from by comparing scents received at all nearby squares. It does not display other kinds of intelligences, so we consider NanoBot to be a weak intelligent agent. It takes in informational input (scents via Bluetooth and black/white detection via IR sensors) and processes that information to interact safely with its environment and achieve its goal of retrieving the gold.
	    </p>
	    <span class="text-white text-lg">Consciousness</span>
	    <p>
	      We do not believe NanoBot is conscious, though it's impossible to be absolutely certain of this. Although it has pretty high computational speed, NanoBot is merely executing a series of instructions. Following from this, NanoBot is completely deterministic, because given the same board, it will always make identical moves. Its lack of emotional intelligence also suggests a lack of consciousness because conscious experience implies thought and desires, which typically coincide with emotions (when your desires are not satisfied, you experience negative emotion).
	      <br />
	      Note that we can never be completely certain of NanoBot's lack of consciousness, because consciousness is entirely internal. NanoBot could be conscious, even if it has no emotional intelligence (a purely logical being). But the evidence suggests that NanoBot is not conscious.
	    </p>
	    <span class="text-white text-lg">Mind-Body</span>
	    <p>
	      NanoBot does not seem to think, so it also does not seem to have a mind. But if it did have a mind, the mind would be the Arduino Nano's CPU and storage drives, which together store information, make logical deductions and transformations, and give instructions to the body (NanoBot's motors). This mind would be entirely materialistic, because its computation is completely credited to its physical arrangement of molecules. Following the materialist mind-body model, signals from NanoBot's infrared sensors, which are a part of its body, are sent to the mind (via wires). Analyzing NanoBot in this way, one can see how the materialist mind-body position is based on computers.
	    </p>
	    <span class="text-white text-lg">Artificial Intelligence</span>
	    <p>
	      This project doesn't change our view on Artifical Intelligence (AI) that much. Every AI we've seen thus far is an algorithm that maps inputs to the same outputs. AI seems intelligent because it will give similar outputs to humans, but none of the AI is actually thinking. This project is a great example of how an algorithm can seem intelligent, because our algorithm can make all of the deductions a human can about a board, and much faster than a human can.
	    </p>
	    <p>
	      A shortcoming of AI that shows how it's not actually intelligent is how it operates only on the set of data or conditions for which it is trained. A human can learn and complete a variety of tasks in a variety of environments, but our algorithm will not work when it's applied to anything other than the Wumpus World Challenge. Even modifying the world so that there can be more than one Wumpus would cause our algorithm to fail. Historically, we've seen the same trend. We've made AIs that play chess or Go, but they can't play any other games. Even the more "sophisticated" AIs that learn language have the same problem, such as when IBM launched project Watson, attempting to repurpose the Jeopardy AI to be a digital assistant but failing miserably.
	    </p>
	  </section>
	</main>

    

</template>
