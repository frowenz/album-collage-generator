## Description

This is the product of a MAAD 26210 assignement where we were instructed to create art from data about ourselves. Using the Spotify API, ``album_cover_fetch.py`` retrieves unique album covers from every track in a csv file. The album covers are then sorted based on brightness, saturation, hue (or some combination) and placed accordingly in ``image_maker.py``. Here is the final image that I submitted for class:

<p align="center">
  <img src="default.jpg" alt="collage" width="500">
</p>

There are a few more examples below and even more examples [here](/more_examples/ALL_EXAMPLES.md).
<p align="center">
  <img src="more_examples/hue_then_brightness.jpg" alt="collage" width="175">&nbsp;&nbsp; 
  <img src="more_examples/hue_reversed.jpg" alt="collage" width="175">&nbsp;&nbsp; 
  <img src="more_examples/brightness_then_saturation.jpg" alt="collage" width="175">&nbsp;&nbsp; 
  <img src="more_examples/saturation_then_hue.jpg" alt="collage" width="175">&nbsp;&nbsp; 
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

1. Download dependencies:

        pip3 install pillow requests python-dotenv

2. Download your last.fm data from [benjaminbenben.com/lastfm-to-csv](https://benjaminbenben.com/lastfm-to-csv/). This will generate a CSV file with the following columns:

        Artist, Album, Song, Time Scrobbled

3. Run the following command to download album covers:

        python3 album_cover_fetch.py YOUR_CSV.CSV NUM_THREADS

    Replace `YOUR_CSV.CSV` with the path to your downloaded CSV file, and `NUM_THREADS` with the number of worker threads you'd like to use (6 is the default if unspecified). This will download all the album covers into a folder named `album_covers`.

4. Once all your images are downloaded, it's a good idea to back them up, as the next script is destructive.

5. Run the following command to create the collage:

        python3 image_maker.py

    Here are the possible arguements that can be passed:

        python3 image_maker.py COMPRESSED_DIMENSIONS SORT_CRITERIA --reverse

    If unspecified, `COMPRESSED_DIMENSIONS` will be 64 meaning each album cover will be cropped to 64 x 64.

    If unspecified, `SORT_CRITERIA` will be "brightness". The other options are "hue" and "saturation".

    If `--reverse` is specified, the images will be sorted in descending order.

    By default, the images are arranged in a circular formation. If you want to arrange them from side to side or to double sort them (e.g., sort top to bottom by brightness and then left to right by hue), you will have to poke around in the code. The relevant lights all begin with:

        # Change Me:

6. Your final output will be saved as `collage.jpg`.

## Notes

Occasionally, there might be duplicate albums covers. This mainly occurs when there exists both a regular and deluxe version of album.

In order to get left and right sorting, you will have to poke around in the code. It is mostly a matter of uncommenting and commenting lines.

## Future Plans

I plan on adding support for different outputs dimensions so wallpapers can be produced.

I might add support for placing smaller pictures so they create a mosiac of an input larger picture.

