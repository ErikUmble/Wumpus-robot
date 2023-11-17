
<template>
  <!--This specifies global layout for each page-->
  <div>
    <!-- Header -->
    <header class="text-white py-4 shadow-lg">
      <div class="container mx-auto px-3">
        <!-- Navigation Links -->
        <nav class="flex items-center">
          <ul class="flex space-x-4">
            <li>
              <nuxt-link to="/" class="text-white hover:text-gray-300">Home</nuxt-link>
            </li>
            <li>
              <nuxt-link to="/about" class="text-white hover:text-gray-300">About</nuxt-link>
            </li>
            <li>
              <nuxt-link to="/blog" class="text-white hover:text-gray-300">Blog</nuxt-link>
            </li>
            <li>
              <nuxt-link to="/demo" class="text-white hover:text-gray-300">Demo</nuxt-link>
            </li>
          </ul>
        </nav>
      </div>
    </header>

    <div>
      <!--Each page template automatically goes here-->
      <NuxtPage />
    </div>
  </div>
</template>

<script>

</script>

