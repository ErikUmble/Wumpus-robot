
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
              <nuxt-link to="/design" class="text-white hover:text-gray-300">Design</nuxt-link>
            </li>
            <li>
              <nuxt-link to="/discussion" class="text-white hover:text-gray-300">Discussion</nuxt-link>
            </li>
            <li>
              <nuxt-link to="/logs" class="text-white hover:text-gray-300">Logs</nuxt-link>
            </li>
            <li>
              <nuxt-link to="/demo" class="text-white hover:text-gray-300">Demo</nuxt-link>
            </li>
          </ul>
        </nav>
      </div>
    </header>

    <body>
      <div>
        <!--Each page template automatically goes here-->
        <NuxtPage />
      </div>
    </body>

    <footer class="py-4 px-8 bg-gray-800 text-center">
        <p>Minds & Machines 2023 - Joel M. & Erik U.</p>
    </footer>
  </div>
</template>

<script>

</script>

