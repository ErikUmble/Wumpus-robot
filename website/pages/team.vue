<template>
  <PageTitle>
    <template v-slot:title>Our Team</template>
    <template v-slot:subtitle>Here's to the fun we had!</template>
  </PageTitle>
  <main class="container mx-auto py-8 px-4">
    <section class="mb-8">
      <div class="flex justify-center w-full">
	<img src="@/assets/images/team.png" alt="Partner Pic" class="rotate-180" style="max-height: 80vh">
      </div>
      <div id="caption" class="text-center w-full">
	Joel M. (left) and Erik U. (right)
      </div>
      <p class="mt-8">
	We were disappointed to hear that the LEGO Mindstorms kits which were used in this project in the past were no longer working, leading to our professors considering taking the project off the table. Together, we agreed to pursue the project anyways, and when we tried the Mindstorms kits and failed to get them connected in any way, we switched to using an Arduino. In the weeks we worked on it, much of our time was spent trying to rebuild what Mindstorms has built-in already, but that didn't stop us from celebrating when we first got the motors to spin or got our sensors connected. We're super proud of how far NanoBot has come, and are both very glad that we stuck with this project through our hardships.
      </p>
    </section>
  </main>
</template>
