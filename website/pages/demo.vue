<template>
<PageTitle>
    <template v-slot:title>Demo</template>
    <template v-slot:subtitle>Watch NanoBot in action (2x speed recommended)</template>
</PageTitle>

<section class="text-center items-center contnet-center py-12">
    <div class="flex justify-center">
        <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/73Ivw8i-liU?si=bQ5bOVg7fe61ApQl" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
    </div>
    <p class="py-2 px-4">This board provided an easy success. When all else is equal, NanoBot prefers vertical movement, which led it to the gold quickly.</p>

</section>

<section class="text-center items-center contnet-center py-12">
    <div class="flex justify-center">
        <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/fC_Bzc6HNs8?si=OKiAzcyONmuCIUad" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
    </div>
    <p class="py-2 px-4">This board required logical deduction to determine where the gold/pit was after sensing both.</p>


</section>

<section class="text-center items-center contnet-center py-12">
    <div class="flex justify-center">
        <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/16AjJ_mv9dA?si=dybMF_2jr4fyWoJV" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
    </div>
    <p class="py-2 px-4">NanoBot solved this one in a fairly straighforward way.</p>


</section>

<section class="text-center items-center contnet-center py-12">
    <div class="flex justify-center">
        <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/l8ya6bs_mnE?si=DAiyfpzZEj2PyuU-" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
    </div>
    <p class="py-2 px-4">This board was not too difficult to solve logically, but NanoBot stumbled by approaching a corner in such a way that the left
        and right sensors were triggered at the same time, thus causing it to believe it had crossed a line correctly. It continued to straddle the line perfectly 
        and would have more obviously failed if it had veered slightly off the line which would have massively disrupted its spacial understanding 
        of how it was oriented. NanoBot did retrieve the gold without entering a dangerous square, but its execution was not perfect, so we 
        only consider this to be a semi-success.
    </p>


</section>
<section class="text-center items-center contnet-center py-12">
    <div class="flex justify-center">
        <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/b1rY62tjVvY?si=52g0-tu7h1GnlUls" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
    </div>
    <p class="py-2 px-4">And of course, we had to include the bloopers.
    </p>


</section>
    
</template>