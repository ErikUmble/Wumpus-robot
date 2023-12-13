<template>
    <PageTitle>
        <template v-slot:title>Discussion</template>
        <template v-slot:subtitle>Comparing NanoBot with its competition and AI in general</template>
    </PageTitle>
    <main class="container mx-auto py-8 px-4">
	  <section class="mb-8">
            <h2 class="text-3xl font-semibold mb-4 text-white">How'd We Do?</h2>
	    <p>
	      With the passing of the LEGO Mindstorms kits, we didn't have any competitors this year. But viewing footage from past challenges, it seems like we did pretty well overall!
	    </p>
	    <br />
		<div class="flex flex-col md:flex-row">
			<div class="container px-4 py-2">
				<span class="text-center text-white text-lg">Accomplishments</span>
				<ul class="list-disc">
					<li>Sufficient error correction to avoid serious accumulated error on most boards.</li>
					<li>Successfully completed an easy board, a medium, and two hard ones (before the battery died).</li>
					<li>Passed all test cases (including the hardest level) in the algorithm tests.</li>
				</ul>
			</div>
			<div class="container px-4 py-2">
				<span class="text-center text-white text-lg">Future Improvements</span>
				<ul class="list-disc">
					<li>It should be possible to maintain that level of error correction and do so without as many pauses and readjustments.</li>
					<li>When pathfinding, prefer to continue in the same direction.</li>
					<li>Complete all boards.</li>
				</ul>
			</div>
		</div>
	    
	  </section>
	  <section class="mb-8">
            <h2 class="text-3xl font-semibold mb-4 text-white">Related to Class</h2>
	    <p>
			Intelligence is multifaceted. We think NanoBot displays spacial intelligence as it is able to keep track of its position
			and orientation and perceive its environment to make corrections to its understanding. This enabled it to generally move only into squares
			that were chosen by its pathfinding algorithm. We also think NanoBot displays logical intelligence as it is able to make deductions about the board,
			and navigate it in nontrivial ways. For example, NanoBot is able to able to determine where particular scents come from 
			by comparing scents received at all nearby squares. Although it does not display other kinds of intelligences,
			we still consider it an intelligent agent. It takes in informational input (scents via Bluetooth and black/white detection via IR sensors)
			and processes that information to interact safely with its environment and achieve its goal of retrieving the gold.
	    </p>
	  </section>
	</main>

    

</template>
