# PySlideShow

<i>Configurable image slideshows.</i>

[![Documentation](https://readthedocs.org/projects/pyslideshow/badge/?version=latest)](https://pyslideshow.readthedocs.io/en/latest/?badge=latest)

PySlideShow takes images and a JSON file which 
specifies transition, zoom and pan effects 
and renders them on the screen via OpenGL.

## Installation / Dependencies
PySlideShow depends on the following pip packages:
<pre>
pip install PyGame
pip install PyOpenGl
pip install enum34
pip install jsonschma
pip install numpy
</pre>

## Usage

PySlide image slideshows are configured via a JSON file. An example 
would be the following.
<pre>
{
  "SlideList":
  [    
    {
      "file": "Example/B.GIF"
    },
    {
      "file": "Example/A.GIF",
      "begin":
      {
          "zoom": 1.0,
          "position": "top_right",
          "offset_x": 0.0,
          "offset_y": 0.0
      },
      "end":
      {
          "zoom": 1.2,
          "position": "top_right",
          "offset_x": 0.0,
          "offset_y": 0.0
      }
    }
  ]
}
</pre>
To try it out simply run it with its prepared example slideshow.
<pre>
python bin/SlideShow.py --fullscreen Example/slideshow.json
</pre>

### Command line arguments
The available command line syntax is the following:
<pre>
python bin/SlideShow.py [--fullscreen] [--minimal] SLIDESHOW.json
</pre>

### Hotkeys
While the slideshow is running the following keyboard controls
are available:
<pre>
ESC           Stop slideshow
F5            Reload slideshow and continue from the current image
Right         Got to next image
Left          Got to next image
Ctrl + Right  Jump 10 images forward
Ctrl + Left   Jump 10 images back
Space         Pause/resume slideshow on current slide
</pre>

## Future Work
- Implement reloading of configuration during runtime
- Implement loading/unloading of images while presentation is running
- Offset in relative image sizes (e.g. 0.5 is half image width instead of display px)
- Slide ID and framerate overlay
