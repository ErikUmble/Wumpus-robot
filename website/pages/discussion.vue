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
				  <li>Successfully completed an easy, medium, and two hard boards (before the battery died).</li>
				  <li>Passed all test cases (including the hardest level) in the algorithm tests. Also demonstrated more sophisticated reasoning such as considering distance and the new information NanoBot could learn when selecting the next square to move to.</li>
				  <li>We only shoot the Wumpus when we have to (Peace First&#x2122;)</li>
				  <li>Our algorithm was lightweight and quick. It executed with no delay and used small storage to fit on the Arduino Nano's drives.</li>
				  
				</ul>
			</div>
			<div class="container px-4 py-2">
			  <span class="text-center text-white text-lg">Future Improvements</span>
			  <ul class="list-disc">
				  <li>It should be possible to maintain that level of error correction and do so without as many pauses and readjustments.</li>
				  <li>Turning should be able to happen faster rather than correcting for so long. <span class="italic">Note: in the past, Mindstorms' software handled all of the behind-the-scenes work with encoder feedback loops to get the motors to their proper positions. We attempted to recreate this in our limited time, which is why our feedback loops are not as advanced.</span></li>
				  <li>When pathfinding, prefer to continue in the same direction. This will minimize error caused by turning.</li>
				  <li>Complete all of the boards in fewer attempts.</li>
			  </ul>
			</div>
		</div>
		
	  </section>
	  <section class="mb-8">
            <h2 class="text-3xl font-semibold mb-4 text-white">Related to Class</h2>
	    <h3 class="text-white text-lg mt-5">Intelligence</h3>
	    <p>
	      As we learned in our group presentations, intelligence is multifaceted. 
		  NanoBot displays spacial intelligence as it is able to keep track of its position and orientation and use features of its environment to 
		  correct its understanding. Demonstrating spacial intelligence, it can usually move to its intended destination. 
		  NanoBot also displays logical intelligence as it is able to make deductions about the board, and navigate it in nontrivial ways. 
		  For example, NanoBot is able to able to determine where particular scents come from by comparing scents received at all nearby squares. 
		  It does not display other kinds of intelligences, so we consider NanoBot to be a weak intelligent agent. 
		  It takes in informational input (scents via Bluetooth and black/white detection via IR sensors) and processes that information to interact safely with its environment and achieve its goal of retrieving the gold.
	    </p>
	    <h3 class="text-white text-lg mt-5">Consciousness</h3>
	    <p>
	      We do not believe NanoBot is conscious; it does not demonstrate self-awareness, have emotions, or express thoughts and desires. 
		  Although it has pretty high computational speed,
		   NanoBot is merely executing a series of instructions and its logic is deterministic. That is, given the same board, 
		   it will always make identical moves. We have no reason to think that it has conscious experiences. 
	    </p>
	    <h3 class="text-white text-lg mt-5">Minds</h3>
	    <p>
			Similarly, we do not think that NanoBot has a mind. It demonstrates some kinds of intelligence, but lacks memory, learning, 
			motives, and awareness. And it does not seem to think or make choices of its own.
	    </p>
		<h3 class="text-white text-lg mt-5">Embedded Cognition</h3>
	    <p>
			Humans use their environment to help them think. For instance, we use calculators to enable us to tackle more complex math problems and
			writing to aid our memory. NanoBot uses the Arduino Nano's RAM to offload the scents that it receives, to aid its logical ability, and it 
			uses the board markings to improve its understanding of its position and orientation on the map. 
		</p>
	    <h3 class="text-white text-lg mt-5">Artificial Intelligence</h3>
	    <p>
	      This project doesn't change our view on Artificial Intelligence (AI). Every AI we've seen thus far is an algorithm that maps inputs to outputs. AI seems intelligent because it will give similar outputs as humans do, but the AI is not actually thinking. This project is a great example of how an algorithm can seem intelligent, because our algorithm can make all of the deductions a human can about a board, and even much faster than a human can, but has no general intelligence.
	    </p>
	    <p>
	      A common shortcoming of AI is that it is often limited to particular task or environment which is was trained for. 
		  A human can learn and complete a variety of tasks in a variety of environments, 
		  but our algorithm will not work when it's applied to anything other than the Wumpus World Challenge. 
		  Even modifying the world so that there can be more than one Wumpus would cause our algorithm to fail. 
		  Historically, we've seen the same trend. We've made AIs that play chess or Go, but they can't play any other games. 
		  Even the more "sophisticated" AIs that learn language have the same problem, such as when IBM launched project Watson, 
		  attempting to repurpose the Jeopardy AI to be a digital assistant but falling short of having general human level intelligence.
	    </p>
		<p>
			This project did help us appreciate the value of adaptability in robotics. By using iterative line crossing corrections, NanoBot was able 
			to orient itself in the correct direction more reliably than if we tried to make the rotations precisely perfect. We think that robots 
			in the future will also benefit from adaptability to their environments. 
		</p>
	  </section>
    </main>
</template>
