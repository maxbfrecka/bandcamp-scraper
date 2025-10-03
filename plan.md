**thoughts**
there are a sequence of things I need to do to make this work.

1.  I need to get a list of every single release and store as a json. an indexed ordered array.
    it needs to have the links to each release, that is the main thing. just title and link. i think bandcamp exposes a json through the console on either the main page or the individual page, or both. or it is possible to easily grab the titles and links of each release through the html on the home page of your profile.

2.  it needs to then separately, in a separate script, use the json file to then visit each link and capture information off the page. title, release date, about release, artist name, tracks and names etc.

3.  in the same script that is visiting each page, i then need to download zips of each release as well as the date it was released

-needs to have logic to deal with the download function: it will have to access the "download" link on the page, then it will have to decide how to deal with what pops up using some sort of automated logic because there will be one of 3 scenarios. if it is a paid release, it will just add the URL to a separate json file called "PAID_DOWNLOADS.json" that lists links of releases I need to manually download myself. if it is pay what you want, it will enter zero then click download. if it is free, it will just click download.
-it will always choose the wav file option for the zip download

this is purely to get all the information and files into a single place so i can add them to my own personal S3 so they're not all stored on bandcamp. it was a mistake for me to use bandcamp as archival because it is not guaranteed to still be there forever and i don't want to lose my life work.

DOWNLOAD LOGIC:
there is a popup every time you visit asking about cookies, you need to get past that.

must select the format you want (Wav)

<select class="bc-select select-margins" id="format-type" data-bind="
                    options: downloadFormatInfos,
                    optionsText: (item) =>  item.sizeMb? item.description + ' - ' + item.sizeMb : item.description,
                    optionsValue:(item) => item.encodingName,
                    value: $parent.formatVM.format().name,
                    event: {change: changeFormat.bind($data, $parent.formatVM)},
                    visible: hasDownload &amp;&amp; !downloadError()
                    "><option value="mp3-v0">MP3 V0 - 15.6MB</option><option value="mp3-320">MP3 320 - 21.9MB</option><option value="flac">FLAC - 44.4MB</option><option value="aac-hi">AAC - 14.3MB</option><option value="vorbis">Ogg Vorbis - 12.4MB</option><option value="alac">ALAC - 49MB</option><option value="wav">WAV - 60.2MB</option><option value="aiff-lossless">AIFF - 84.1MB</option>
</select>

<option value="wav">WAV - 60.2MB</option>

then wait around 20 seconds because it may need to prepare the download link.
<a style="" data-bind="attr: { href: downloadUrl }, visible: downloadReady() &amp;&amp; !downloadError()" href="https://p4.bcbits.com/download/album/1f6a79c5d474ed998298e12c6d484b4d2/wav/3731078398?fsig=7d3a2d5c7468bda6e1e117c84438e6f9&amp;id=3731078398&amp;ts=1759502674.3799466412&amp;token=1760107474_0a0758aaa310a996b019f4c17aea5f7a5632e106">Download</a>

then somehow execute that download, visiting the link should automatically start download but i'm not sure.
you cant just visit that link directly outside of this moment from this page. it has to be from the page.
i think.

we need to do these in batches and track failures. if there is some kind of failure, add the release and url data into "downloadFailures.json"
