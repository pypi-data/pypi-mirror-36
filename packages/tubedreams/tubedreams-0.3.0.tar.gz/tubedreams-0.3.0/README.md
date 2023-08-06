# tubedreams

tubedreams is part of [material browsing history](https://hudsonbailey.org/projects/material-history/), an experiment in self-quantification and imagining different ways of engaging with computation, privacy, consumption and personal data.

tubedreams is a command line program that concatenates random pieces of local or online videos with the intention of making collages of videos you have viewed. In its default settings, tubedreams turns your YouTube viewing history into new video content. Unrelated sequences of images and sound are recombined in playful or nightmarish ways that could only be produced via your own uniquely-curated media consumption. It can also be adapted for other purposes of making quick video collages (see [examples](#examples)).

## Dependencies

- [python 3](https://www.python.org/downloads/)

- [ffmpeg](https://ffmpeg.org/)

- [SoX](https://sox.sourceforge.net/)

As well as a few python packages, which should automatically get installed when this package is installed:

- [youtube-dl](https://github.com/rg3/youtube-dl) -- for grabbing videos from YouTube or another site.

- [moviepy](https://github.com/Zulko/moviepy) -- for cutting video (uses ffmpeg as a backend).

- [pysox](https://github.com/rabitt/pysox), a python wrapper for SoX -- for audio effects

## Installation

```
pip install tubedreams
```

## Setup

By default, tubedreams attempts to access your YouTube history as a playlist via youtube-dl. In order for youtube-dl to access your history like your browser does, you need to configure your login information in one of three ways:

- Setup the `.tubedreams.conf` file in the package directory (tubedreams looks for this by default).

- Add your login information to a .netrc file (and pass the `--netrc` argument):

  ```
  touch ~/.netrc
  chmod 600 ~/.netrc
  echo "machine youtube login LOGIN password PASSWORD" >> ~/.netrc

  # verify that the login information is correct
  tubedreams --netrc --number 1 --length 5 --minmax 5 --fresh --output test.mp4
  ```

- Or pass your login information manually via the `--login USERNAME PASSWORD` argument.

_note: If you have two-factor authentication set-up with your YouTube/Google account, you will be required to manually authenticate since youtube-dl does not support interfacing with the YouTube developer API._

For public playlists, searches or individual videos, you can pass the argument `--nologin` to avoid having to setup authentication.

## Options

```

usage: tubedreams [-h] [-v] [-dd] [-s [[...]]] [-p ] [-f] [-o ] [-k] [-u ]
                  [-n ] [-da] [-N] [-L [[...]]] [-nl] [-l ] [-m [[...]]]
                  [-fc ] [-g] [-x] [-r [[...]]] [-c ] [-a ] [-oa] [-dp] [-vf ]

create dream-sequences from your video browsing history

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -dd, --dontdownload   don't download any videos or connect to youtube-dl.
                        will only use local videos from source directories.
  -s [ [ ...]], --source [ [ ...]]
                        specify directories to draw raw footage from. the
                        first directory listed also specifies the location for
                        new videos to download
  -p [], --pattern []   only use videos from input directories which contain a
                        given string. note: will still download raw videos
                        that do not match pattern.
  -f, --fresh           only include videos downloaded this run
  -o [], --output []    specify file name and directory for final video output
  -k, --keep            keep raw downloaded videos after processing is
                        completed

youtube-dl options:
  -u [], --url []       the url of the playlist, search page, or video to
                        download from. default is to grab history from
                        https://www.youtube.com/feed/history
  -n [], --number []    number of videos to download
  -da, --downloadall    download all videos in playlist. overrides -n
  -N, --netrc           use .netrc file for login instead of .tubedreams.conf
  -L [ [ ...]], --login [ [ ...]]
                        username and password for accessing YouTube or other
                        site via youtube-dl.
  -nl, --nologin        do not log into an account to access site

video output options:
  -l [], --length []    total length of video to output
  -m [ [ ...]], --minmax [ [ ...]]
                        minimum and maximum length of each clip. one input
                        fixes a static clip length. two inputs sets range.
  -fc [], --finalclip []
                        specify length of final clip
  -g, --grow            scale length of clips so that they gradually get
                        longer or shorter to match finalclip. must use with
                        finalclip.
  -x, --exponential     makes length scaling exponential. must use with grow.
  -r [ [ ...]], --resolution [ [ ...]]
                        select dimensions to output to. one input specifies y
                        dimension for 12:9 ratio. for two inputs, the smaller
                        specifies y and the larger specifies x. default is
                        480p.
  -c [], --codec []     choose codec for uncommon video format or override
                        default codec. defaults are included for mp4
                        (libx264), mkv (libx264), webm (libvpx), ogv
                        (libvorbis) and avi (png).
  -a [], --setaudio []  add path to audio track to use
  -oa, --onlyaudio      only export to mp3 audio, no video.
  -dp, --dontprocessaudio
                        keep raw audio and do not apply sox filters.
  -vf [], --videofilters []
                        add ffmpeg video filters to output video.

```

## Filters

See the [ffmpeg documentation](https://ffmpeg.org/ffmpeg-filters.html) for a list of native ffmpeg filters and usage syntax. You can invoke ffmpeg video filters in tubedreams with `-vf` just as you would with ffmpeg:

```
-vf eq=brightness=.3:contrast=2:gamma=.6:saturation=0,fade=in:0:60
```

Complex filters and audio filters are not currently supported.

## Downloading Videos

See [this list](https://rg3.github.io/youtube-dl/supportedsites.html) for sites currently supported by youtube-dl. Note that not all of these supported sites will necessarily have playlist features fully implemented. For non-YouTube sites, it could be necessary to create a work-around to capture videos in history or playlists even if they appear in this list.

## Examples

Download five random videos from your YouTube history, keep them, and chop and recombine into a 20 second clip:

```
tubedreams --number 5 --fresh --keep --length 20 --minmax 1 3 --output test.mp4
```

A random 10 second clip from your YouTube history:

```
tubedreams --number 1 --fresh --length 10 --minmax 10 --dontprocessaudio --output 10sec.avi
```

Download your entire YouTube history and turn it into a 5-hour-long sound collage for an art exhibition:

```
tubedreams --downloadall --onlyaudio --length 18000 --minmax .2 10 --output experimental.mp3
```

Cut clips from local video files and make into black-and-white:

```
tubedreams --dontdownload --source ~/Videos/movies/ ~/Videos/shows/ --videofilters "eq=saturation=0:gamma=.5:contrast=2:brightness=.2" --length 120 --minmax 10 --output bw.mkv
```

The news in 30 seconds:

```
tubedreams --url "https://www.youtube.com/results?search_query=news" --nologin --downloadall --fresh --length 30 --minmax .1 .5 --videofilters eq=saturation=5:contrast=2,random --dontprocessaudio --output news.ogv
```
