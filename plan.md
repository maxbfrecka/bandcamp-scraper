**thoughts**
there are a sequence of things I need to do to make this work.

1.  I need to get a list of every single release and store as a json. an indexed ordered array.
    it needs to have the links to each release, that is the main thing. just title and link. i think bandcamp exposes a json through the console on either the main page or the individual page, or both. or it is possible to easily grab the titles and links of each release through the html on the home page of your profile.

2.  it needs to then separately, in a separate script, use the json file to then visit each link and capture information off the page. title, release date, about release, artist name, tracks and names etc.

3.  in the same script that is visiting each page, i then need to download zips of each release as well as the date it was released

-needs to have logic to deal with the download function: it will have to access the "download" link on the page, then it will have to decide how to deal with what pops up using some sort of automated logic because there will be one of 3 scenarios. if it is a paid release, it will just add the URL to a separate json file called "PAID_DOWNLOADS.json" that lists links of releases I need to manually download myself. if it is pay what you want, it will enter zero then click download. if it is free, it will just click download.
-it will always choose the wav file option for the zip download

this is purely to get all the information and files into a single place so i can add them to my own personal S3 so they're not all stored on bandcamp. it was a mistake for me to use bandcamp as archival because it is not guaranteed to still be there forever and i don't want to lose my life work.
