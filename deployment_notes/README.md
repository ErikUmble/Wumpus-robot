Since it took a few hours to figure out how to host this statically, I figured I should
take note of what ended up working.

Use AWS Amplify (free hosting for static site)
Create static site
Provide GitHub permission and connect to the repo
Change the amplify.yml in build settings
    make sure appRoot is set to the directory that is the root for the webapp
    make sure the build command is using generate instead of build (generate will convert the SSR into static files)
    also, add the ```npm i``` command to prebuild step
    change the baseDirectory to the subdirectory of the app root which holds the generated files (.output/public in the case of Nuxt)

Setup DNS
    Goto Domain management within the Amplify App settings
    add domain and enter the root as it directs
    click exclude root (if you only want subdomain pointing there)
    replace www with the subdomain you actually want to use in the other line
    to add the provided CNAME Record in Namecheap:
        goto Advanced DNS
        + CNAME Record
        then put the first item excluding the root (so wumpus.erikumble.com means just put wumpus in the host field)
        put the full second item in the host field (ie. randomDigits.aws.com )
        save changes
        repeat as needed
        
