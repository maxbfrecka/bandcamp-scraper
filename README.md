# bandcamp-scraper

I have 262 Album pages on Bandcamp and foolishly did not store them elsewhere.

I developed these scraping tools to assist in helping me get all my releases and automate downloading the files.

STEPS:

1. activate venv
2. pip install

Running the scripts (do in sequence):
getAllAlbums: add your bandcamp URL to that. it will create a json file in this directory with all of them.

getAllAlbumsData: visits each page from releases.json (script above made that) and then grabs all metadata. run in batches. has delay to avoid throttling. it creates separate metadata files.

mergeMetadata: merges all the metadata json files into a single file

getPaidReleases: determines which releases are paid releases and adds to json file.

checkEmailRequired: checks if email is required for free download and adds those to a list.

updateMetadata: looks into paid releases and scans those urls, updates metadata if you altered those releases to free (for automated downloading in last step)
