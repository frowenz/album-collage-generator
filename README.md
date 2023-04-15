## Description

This is the product of a MAAD 26210 assignement where we were instructed to create art from data about ourselves. Using the Spotify API, ``album_cover_fetch.py`` retrieves unique album covers from every track in a csv file. The album covers are then sorted based on brightness and placed accordingly in ``image_maker.py``.

<p align="center">
  <img src="default.jpg" alt="collage" width="500">
</p>

## Spotify API Keys

To use this ``album_cover_fetch.py``, you'll need to have your own Spotify API keys (client ID and secret key). Follow these steps to obtain your keys and set up the environment variables:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and log in or create an account if you don't have one.

2. Click on "Create an App" and fill in the required information to create a new Spotify API application.

3. After creating the app, you'll find the "Client ID" and "Client Secret" on the application's dashboard.

4. Create a `.env` file in the project directory and add your client ID and secret key:

        CLIENT_ID=your_client_id_here
        CLIENT_SECRET=your_client_secret_here

    The script will automatically load the client ID and secret key from the `.env` file.


## Usage

1. Download your last.fm data from [benjaminbenben.com/lastfm-to-csv](https://benjaminbenben.com/lastfm-to-csv/). This will generate a CSV file with the following columns:

        Artist, Album, Song, Time Scrobbled

2. Run the following command to download album covers:

        python3 album_cover_fetch.py YOUR_CSV.CSV NUM_THREADS

    Replace `YOUR_CSV.CSV` with the path to your downloaded CSV file, and `NUM_THREADS` with the number of worker threads you'd like to use (6-8 threads is a recommended value). This will download all the album covers into a folder named `album_covers`.

3. Once all your images are downloaded, it's a good idea to back them up, as the next script is destructive.

4. Run the following command to create the collage:

        python3 image_maker.py

    Here are the possible arguements that can be passed:

        python3 image_maker.py COMPRESSED_DIMENSIONS SORT_CRITERIA --reverse

    If unspecified, `COMPRESSED_DIMENSIONS` will be 64 meaning each album cover will be cropped to 64 x 64.

    If unspecified, `SORT_CRITERIA` will be "brightness". The other options are "hue" and "saturation".

    If `--reverse` is specified, the images will be sorted in descending order.

5. Your final output will be saved as `collage.jpg`.


## Future Plans and Notes

I plan on adding support for different outputs dimensions so wallpapers can be produced.
-
I might add support for placing smaller pictures so they create a mosiac of an input larger picture.

Occasionally, there might be duplicate albums, especially when it comes to deluxe versions of albums.
