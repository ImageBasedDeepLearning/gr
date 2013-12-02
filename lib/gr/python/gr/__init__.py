# -*- coding: utf-8 -*-
"""
This is a procedural interface to the GR plotting library,
which may be imported directly, e.g.:

  import gr
"""
# standard library
import os
from ctypes import c_int, c_double, c_char_p, c_void_p
from ctypes import byref, POINTER, addressof, CDLL, CFUNCTYPE
from ctypes import create_string_buffer, create_unicode_buffer, cast
from sys import version_info, platform

def floatarray(n, a):
  _a = (c_double * n)()
  for i in range(n):
    _a[i] = a[i]
  return _a

def intarray(n, a):
  _a = (c_int * n)()
  for i in range(n):
    _a[i] = a[i]
  return _a

def char(string):
  if version_info[0] == 3:
    s = create_string_buffer(string.encode('iso8859-15'))
  else:
    s = create_string_buffer(string)
  return cast(s, c_char_p)
  
def chararray(n, a):
    _a = (c_char_p * n)()
    for i in range(n):
      _a[i] = char(a[i])
    return _a

def opengks():
  __gr.gr_opengks()

def closegks():
  __gr.gr_closegks(void)

def inqdspsize():
  mwidth = c_double()
  mheight = c_double()
  width = c_int()
  height = c_int()
  __gr.gr_inqdspsize(byref(mwidth), byref(mheight), byref(width), byref(height))
  return [mwidth.value, mheight.value, width.value, height.value]

def openws(workstation_id, connection, type):
  __gr.gr_openws(c_int(workstation_id), char(connection), c_int(type))

def closews(workstation_id):
  __gr.gr_closews(c_int(workstation_id))

def activatews(workstation_id):
  __gr.gr_activatews(c_int(workstation_id))

def deactivatews(workstation_id):
  __gr.gr_deactivatews(c_int(workstation_id))

def clearws():
  __gr.gr_clearws()

def updatews():
  __gr.gr_updatews()

def polyline(n, x, y):
  """
Draws a polyline using the current line attributes,
starting from the first data point and ending at the
last data point.

N - The number of points in the line to be drawn (N > 1)
X - A list of length N containing the X coordinates
Y - A list of length N containing the Y coordinates

The values for X and Y are in world coordinates.
The attributes that control the appearance of a polyline are
linetype, linewidth and color index.
"""
  _x = floatarray(n, x)
  _y = floatarray(n, y)
  __gr.gr_polyline(c_int(n), _x, _y)

def polymarker(n, x, y):
  """
Draws marker symbols centered at the given data points.

N - The number of markers to be drawn (N > 1)
X - A list of length N containing the X coordinates
Y - A list of length N containing the Y coordinates

The values for X and Y are in world coordinates.
The attributes that control the appearance of a polyline are
marker type, marker size scale factor and color index.
"""
  _x = floatarray(n, x)
  _y = floatarray(n, y)
  __gr.gr_polymarker(c_int(n), _x, _y)

def text(x, y, string):
  """
Draws a text at position X, Y using the current text attributes.

X - The X coordinate of starting position of the text string
Y - The Y coordinate of starting position of the text string
STRING - The text to be drawn

The values for X and Y are in normalized device coordinates.
The attributes that control the appearance of text are text font and precision,
character expansion factor, character spacing, text color index, character
height, character up vector, text path and text alignment.
  """
  __gr.gr_text(c_double(x), c_double(y), char(string))

def fillarea(n, x, y):
  """
Allows you to specify a polygonal shape of an area to be filled.

N - The number of points of the polygon to be drawn (N > 1)
X - A list of length N containing the X coordinates
Y - A list of length N containing the Y coordinates

The attributes that control the appearance of fill areas are fill area interior
style, fill area style index and fill area color index.
  """
  _x = floatarray(n, x)
  _y = floatarray(n, y)
  __gr.gr_fillarea(c_int(n), _x, _y)

def cellarray(xmin, xmax, ymin, ymax, dimx, dimy, color):
  """
Displays rasterlike images in a device-independent manner. The cell array
function partitions a rectangle given by two corner points into DIMX x DIMY
cells (divided from upper left point to lower right point),
each of them colored individually by the corresponding color index
of the given cell array.

XMIN, YMIN - Lower left point of the rectangle
XMAX, YMAX - Upper right point of the rectangle
DIMX, DIMY - X and Y dimension of the color index array
COLOR - Color index array

The values for XMIN, XMAX, YMIN and YMAX are in world coordinates.
  """
  _color = intarray(dimx*dimy, color)
  __gr.gr_cellarray(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax),
                    c_int(dimx), c_int(dimy), c_int(1), c_int(1),
                    c_int(dimx), c_int(dimy), _color)

def spline(n, px, py, m, method):
  _px = floatarray(n, px)
  _py = floatarray(n, py)
  __gr.gr_spline(c_int(n), _px, _py, c_int(m), c_int(method))

def gridit(nd, xd, yd, zd, nx, ny):
  _xd = floatarray(nd, xd)
  _yd = floatarray(nd, yd)
  _zd = floatarray(nd, zd)
  x = (c_double * nx)()
  y = (c_double * ny)()
  z = (c_double * (nx * ny))()
  __gr.gr_gridit(c_int(nd), _xd, _yd, _zd, c_int(nx), c_int(ny), x, y, z)
  return [x[:], y[:], z[:]]

def setlinetype(type):
  __gr.gr_setlinetype(c_int(type))
  
def inqlinetype():
  ltype = c_int()
  __gr.gr_inqlinetype(byref(ltype))
  return ltype.value

def setlinewidth(width):
  __gr.gr_setlinewidth(c_double(width))

def setlinecolorind(color):
  __gr.gr_setlinecolorind(c_int(color))
  
def inqlinecolorind():
  coli = c_int()
  __gr.gr_inqlinecolorind(byref(coli))
  return coli.value

def setmarkertype(type):
  __gr.gr_setmarkertype(c_int(type))
  
def inqmarkertype():
  mtype = c_int()
  __gr.gr_inqmarkertype(byref(mtype))
  return mtype.value

def setmarkersize(size):
  __gr.gr_setmarkersize(c_double(size))

def setmarkercolorind(color):
  __gr.gr_setmarkercolorind(c_int(color))
  
def inqmarkercolorind():
  coli = c_int()
  __gr.gr_inqmarkercolorind(byref(coli))
  return coli.value
  
def settextfontprec(font, precision):
  __gr.gr_settextfontprec(c_int(font), c_int(precision))

def setcharexpan(factor):
  __gr.gr_setcharexpan(c_double(factor))

def setcharspace(spacing):
  __gr.gr_setcharspace(c_double(spacing))

def settextcolorind(color):
  __gr.gr_settextcolorind(c_int(color))

def setcharheight(height):
  __gr.gr_setcharheight(c_double(height))

def setcharup(ux, uy):
  __gr.gr_setcharup(c_double(ux), c_double(uy))

def settextpath(path):
  __gr.gr_settextpath(c_int(path))

def settextalign(horizontal, vertical):
  __gr.gr_settextalign(c_int(horizontal), c_int(vertical))

def setfillintstyle(style):
  __gr.gr_setfillintstyle(c_int(style))

def setfillstyle(index):
  __gr.gr_setfillstyle(c_int(index))

def setfillcolorind(color):
  __gr.gr_setfillcolorind(c_int(color))

def setcolorrep(index, red, green, blue):
  __gr.gr_setcolorrep(c_int(index), c_double(red), c_double(green), c_double(blue))

def setscale(options):
  return __gr.gr_setscale(c_int(options))

def inqscale():
  options = c_int()
  __gr.gr_inqscale(byref(options))
  return options.value

def setwindow(xmin, xmax, ymin, ymax):
  __gr.gr_setwindow(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax))

def inqwindow():
  xmin = c_double()
  xmax = c_double()
  ymin = c_double()
  ymax = c_double()
  __gr.gr_inqwindow(byref(xmin), byref(xmax), byref(ymin), byref(ymax))
  return [xmin.value, xmax.value, ymin.value, ymax.value]

def setviewport(xmin, xmax, ymin, ymax):
  __gr.gr_setviewport(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax))

def selntran(transform):
  __gr.gr_selntran(c_int(transform))

def setclip(indicator):
  __gr.gr_setclip(c_int(indicator))

def setwswindow(xmin, xmax, ymin, ymax):
  __gr.gr_setwswindow(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax))

def setwsviewport(xmin, xmax, ymin, ymax):
  __gr.gr_setwsviewport(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax))

def createseg(segment):
  __gr.gr_createseg(c_int(segment))

def copysegws(segment):
  __gr.gr_copysegws(c_int(segment))

def redrawsegws():
  __gr.gr_redrawsegws()

def setsegtran(segment, fx, fy, transx, transy, phi, scalex, scaley):
  __gr.gr_setsegtran(c_int(segment), c_double(fx), c_double(fy),
                     c_double(transx), c_double(transy), c_double(phi),
                     c_double(scalex), c_double(scaley))

def closeseg():
  __gr.gr_closegks()

def emergencyclosegks():
  __gr.gr_emergencyclosegks()

def updategks():
  __gr.gr_updategks()

def setspace(zmin, zmax, rotation, tilt):
  return __gr.gr_setspace(c_double(zmin), c_double(zmax),
                          c_int(rotation), c_int(tilt))

def inqspace():
  zmin = c_double()
  zmax = c_double()
  rotation = c_int()
  tilt = c_int()
  __gr.gr_inqspace(byref(zmin), byref(zmax), byref(rotation), byref(tilt))
  return [zmin.value, zmax.value, rotation.value, tilt.value]
        
def textext(x, y, string):
  return __gr.gr_textext(c_double(x), c_double(y), char(string))
  
def inqtextext(x, y, string):
  tbx = (c_double * 4)()
  tby = (c_double * 4)() 
  __gr.gr_inqtextext(c_double(x), c_double(y), char(string), tbx, tby)
  return [[tbx[0], tbx[1], tbx[2], tbx[3]],
          [tby[0], tby[1], tby[2], tby[3]]]

_axeslbl_callback = CFUNCTYPE(c_void_p, c_double, c_double, c_char_p)
def axeslbl(x_tick, y_tick, x_org, y_org, major_x, major_y, tick_size,
            fpx=0, fpy=0):
  if fpx is None:
    fpx = 0
  if fpy is None:
    fpy = 0

  cfpx = _axeslbl_callback(fpx)
  cfpy = _axeslbl_callback(fpy)
  __gr.gr_axeslbl(c_double(x_tick), c_double(y_tick),
                  c_double(x_org), c_double(y_org),
                  c_int(major_x), c_int(major_y), c_double(tick_size),
                  cfpx, cfpy)

def axes(x_tick, y_tick, x_org, y_org, major_x, major_y, tick_size):
  __gr.gr_axes(c_double(x_tick), c_double(y_tick),
               c_double(x_org), c_double(y_org),
               c_int(major_x), c_int(major_y), c_double(tick_size))
  
def grid(x_tick, y_tick, x_org, y_org, major_x, major_y):
  __gr.gr_grid(c_double(x_tick), c_double(y_tick),
               c_double(x_org), c_double(y_org),
               c_int(major_x), c_int(major_y))

def verrorbars(n, px, py, e1, e2):
  _px = floatarray(n, px)
  _py = floatarray(n, py)
  _e1 = floatarray(n, e1)
  _e2 = floatarray(n, e2)
  __gr.gr_verrorbars(c_int(n), _px, _py, _e1, _e2)
  
def herrorbars(n, px, py, e1, e2):
  _px = floatarray(n, px)
  _py = floatarray(n, py)
  _e1 = floatarray(n, e1)
  _e2 = floatarray(n, e2)
  __gr.gr_herrorbars(c_int(n), _px, _py, _e1, _e2)

def polyline3d(n, px, py, pz):
  _px = floatarray(n, px)
  _py = floatarray(n, py)
  _pz = floatarray(n, pz)
  __gr.gr_polyline3d(c_int(n), _px, _py, _pz)
  
def axes3d(x_tick, y_tick, z_tick, x_org, y_org, z_org,
           major_x, major_y, major_z, tick_size):
  __gr.gr_axes3d(c_double(x_tick), c_double(y_tick), c_double(z_tick),
                 c_double(x_org), c_double(y_org), c_double(z_org),
                 c_int(major_x), c_int(major_y), c_int(major_z),
                 c_double(tick_size))

def titles3d(x_title, y_title, z_title):
  __gr.gr_titles3d(char(x_title), char(y_title), char(z_title))
  
def surface(nx, ny, px, py, pz, option):
  _px = floatarray(nx, px)
  _py = floatarray(ny, py)
  _pz = floatarray(nx*ny, pz)
  __gr.gr_surface(c_int(nx), c_int(ny), _px, _py, _pz, c_int(option))
  
def contour(nx, ny, nh, px, py, h, pz, major_h):
  _px = floatarray(nx, px)
  _py = floatarray(ny, py)
  _h = floatarray(nh, h)
  _pz = floatarray(nx*ny, pz)
  __gr.gr_contour(c_int(nx), c_int(ny), c_int(nh), _px, _py, _h, _pz,
                  c_int(major_h))
  
def setcolormap(index):
  __gr.gr_setcolormap(c_int(index))

def colormap():
  __gr.gr_colormap()
  
def inqcolor(color):
  rgb = c_int()
  __gr.gr_inqcolor(c_int(color), byref(rgb))
  return rgb.value
 
def tick(amin, amax):
  __gr.gr_tick.restype = c_double
  return __gr.gr_tick(c_double(amin), c_double(amax))

def adjustrange(amin, amax):
  _amin = c_double(amin)
  _amax = c_double(amax)
  __gr.gr_adjustrange(byref(_amin), byref(_amax))
  return [_amin.value, _amax.value]

def beginprint(pathname):
  __gr.gr_beginprint(char(pathname))

def beginprintext(pathname, mode, format, orientation):
  __gr.gr_beginprintext(char(pathname), char(mode), char(format), char(orientation))
  
def endprint():
  __gr.gr_endprint()

def ndctowc(x, y):
  _x = c_double(x)
  _y = c_double(y)
  __gr.gr_ndctowc(byref(_x), byref(_y))
  return [_x.value, _y.value]

def wctondc(x, y):
  _x = c_double(x)
  _y = c_double(y)
  __gr.gr_wctondc(byref(_x), byref(_y))
  return [_x.value, _y.value]

def drawrect(xmin, xmax, ymin, ymax):
  __gr.gr_drawrect(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax))

def fillrect(xmin, xmax, ymin, ymax):
  __gr.gr_fillrect(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax))

def drawarc(xmin, xmax, ymin, ymax, a1, a2):
  __gr.gr_drawarc(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax),
                  c_int(a1), c_int(a2))

def fillarc(xmin, xmax, ymin, ymax, a1, a2):
  __gr.gr_fillarc(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax),
                  c_int(a1), c_int(a2))

def setarrowstyle(style):
  __gr.gr_setarrowstyle(c_int(style))

def drawarrow(x1, y1, x2, y2):
  __gr.gr_drawarrow(c_double(x1), c_double(y1), c_double(x2), c_double(y2))

def readimage(path):
  width = c_int()
  height = c_int()
  _data = POINTER(c_int)()
  __gr.gr_readimage(char(path), byref(width), byref(height), byref(_data))
  _type = (c_int * (width.value * height.value))
  data = _type.from_address(addressof(_data.contents))
  return [width.value, height.value, data]

def drawimage(xmin, xmax, ymin, ymax, width, height, data):
  _data = intarray(width*height, data)
  __gr.gr_drawimage(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax),
                    c_int(width), c_int(height), _data)

def importgraphics(path):
  __gr.gr_importgraphics(char(path))

def setshadow(offsetx, offsety, blur):
  __gr.gr_setshadow(c_double(offsetx), c_double(offsety), c_double(blur))

def settransparency(alpha):
  __gr.gr_settransparency(c_double(alpha))

def setcoordxform(mat):
  _mat = floatarray(6, mat)
  __gr.gr_setcoordxform(_mat)
  
def begingraphics(path):
  __gr.gr_begingraphics(char(path))

def endgraphics():
  __gr.gr_endgraphics()

def mathtex(x, y, string):
  return __gr.gr_mathtex(c_double(x), c_double(y), char(string))

def beginselection(index, type):
  __gr.gr_beginselection(c_int(index), c_int(type))

def endselection():
  __gr.gr_endselection()

def moveselection(x, y):
  __gr.gr_moveselection(c_double(x), c_double(y))

def resizeselection(type, x, y):
  __gr.gr_resizeselection(c_int(type), c_double(x), c_double(y))

def inqbbox():
  xmin = c_double()
  xmax = c_double()
  ymin = c_double()
  ymax = c_double()
  __gr.gr_inqbbox(byref(xmin), byref(xmax), byref(ymin), byref(ymax))
  return [xmin.value, xmax.value, ymin.value, ymax.value]


_grPkgDir = os.path.realpath(os.path.dirname(__file__))
_grLibDir = os.getenv("GRLIB", _grPkgDir)
_gksFontPath = os.path.join(_grPkgDir, "fonts")
if os.access(_gksFontPath, os.R_OK):
  os.environ["GKS_FONTPATH"] = os.getenv("GKS_FONTPATH", _grPkgDir)
  
if platform == "win32":
  libext = ".dll"
else:
  libext = ".so"

_grLib = os.path.join(_grLibDir, "libGR" + libext)
if not os.getenv("GRLIB") and not os.access(_grLib, os.R_OK):          
    _grLibDir = os.path.join(_grPkgDir, "..", "..")
    _grLib = os.path.join(_grLibDir, "libGR" + libext)
if platform == "win32":
    os.environ["PATH"] = os.getenv("PATH", "") + ";" + _grLibDir
__gr = CDLL(_grLib)

__gr.gr_opengks.argtypes = [];
__gr.gr_closegks.argtypes = [];
__gr.gr_inqdspsize.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_int), POINTER(c_int)];
__gr.gr_openws.argtypes = [c_int, c_char_p, c_int];
__gr.gr_closews.argtypes = [c_int];
__gr.gr_activatews.argtypes = [c_int];
__gr.gr_deactivatews.argtypes = [c_int];
__gr.gr_clearws.argtypes = [];
__gr.gr_updatews.argtypes = [];
__gr.gr_polyline.argtypes = [c_int, POINTER(c_double), POINTER(c_double)];
__gr.gr_polymarker.argtypes = [c_int, POINTER(c_double), POINTER(c_double)];
__gr.gr_text.argtypes = [c_double, c_double, c_char_p];
__gr.gr_fillarea.argtypes = [c_int, POINTER(c_double), POINTER(c_double)];
__gr.gr_cellarray.argtypes = [
  c_double, c_double, c_double, c_double, c_int, c_int, c_int, c_int, c_int, c_int, POINTER(c_int)];
__gr.gr_spline.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_int, c_int];
__gr.gr_gridit.argtypes = [c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)];
__gr.gr_setlinetype.argtypes = [c_int];
__gr.gr_inqlinetype.argtypes = [POINTER(c_int)];
__gr.gr_setlinewidth.argtypes = [c_double];
__gr.gr_setlinecolorind.argtypes = [c_int];
__gr.gr_inqlinecolorind.argtypes = [POINTER(c_int)];
__gr.gr_setmarkertype.argtypes = [c_int];
__gr.gr_inqmarkertype.argtypes = [POINTER(c_int)];
__gr.gr_setmarkersize.argtypes = [c_double];
__gr.gr_setmarkercolorind.argtypes = [c_int];
__gr.gr_inqmarkercolorind.argtypes = [POINTER(c_int)];
__gr.gr_settextfontprec.argtypes = [c_int, c_int];
__gr.gr_setcharexpan.argtypes = [c_double];
__gr.gr_setcharspace.argtypes = [c_double];
__gr.gr_settextcolorind.argtypes = [c_int];
__gr.gr_setcharheight.argtypes = [c_double];
__gr.gr_setcharup.argtypes = [c_double, c_double];
__gr.gr_settextpath.argtypes = [c_int];
__gr.gr_settextalign.argtypes = [c_int, c_int];
__gr.gr_setfillintstyle.argtypes = [c_int];
__gr.gr_setfillstyle.argtypes = [c_int];
__gr.gr_setfillcolorind.argtypes = [c_int];
__gr.gr_setcolorrep.argtypes = [c_int, c_double, c_double, c_double];
__gr.gr_setwindow.argtypes = [c_double, c_double, c_double, c_double];
__gr.gr_inqwindow.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)];
__gr.gr_setviewport.argtypes = [c_double, c_double, c_double, c_double];
__gr.gr_selntran.argtypes = [c_int];
__gr.gr_setclip.argtypes = [c_int];
__gr.gr_setwswindow.argtypes = [c_double, c_double, c_double, c_double];
__gr.gr_setwsviewport.argtypes = [c_double, c_double, c_double, c_double];
__gr.gr_createseg.argtypes = [c_int];
__gr.gr_copysegws.argtypes = [c_int];
__gr.gr_redrawsegws.argtypes = [];
__gr.gr_setsegtran.argtypes = [
  c_int, c_double, c_double, c_double, c_double, c_double, c_double, c_double];
__gr.gr_closeseg.argtypes = [];
__gr.gr_emergencyclosegks.argtypes = [];
__gr.gr_updategks.argtypes = [];
__gr.gr_setspace.argtypes = [c_double, c_double, c_int, c_int];
__gr.gr_inqspace.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_int), POINTER(c_int)];
__gr.gr_setscale.argtypes = [c_int];
__gr.gr_inqscale.argtypes = [POINTER(c_int)];
__gr.gr_textext.argtypes = [c_double, c_double, c_char_p];
__gr.gr_inqtextext.argtypes = [c_double, c_double, c_char_p, POINTER(c_double), POINTER(c_double)];
__gr.gr_axeslbl.argtypes = [c_double, c_double, c_double, c_double, c_int, c_int,
                            c_double, _axeslbl_callback, _axeslbl_callback]
__gr.gr_axes.argtypes = [c_double, c_double, c_double, c_double, c_int, c_int, c_double];
__gr.gr_grid.argtypes = [c_double, c_double, c_double, c_double, c_int, c_int];
__gr.gr_verrorbars.argtypes = [c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)];
__gr.gr_herrorbars.argtypes = [c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)];
__gr.gr_polyline3d.argtypes = [c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)];
__gr.gr_axes3d.argtypes = [
  c_double, c_double, c_double, c_double, c_double, c_double, c_int, c_int, c_int, c_double];
__gr.gr_titles3d.argtypes = [c_char_p, c_char_p, c_char_p];
__gr.gr_surface.argtypes = [c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int];
__gr.gr_contour.argtypes = [
  c_int, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int];
__gr.gr_setcolormap.argtypes = [c_int];
__gr.gr_colormap.argtypes = [];
__gr.gr_inqcolor.argtypes = [c_int, POINTER(c_int)];
__gr.gr_tick.argtypes = [c_double, c_double];
__gr.gr_adjustrange.argtypes = [POINTER(c_double), POINTER(c_double)];
__gr.gr_beginprint.argtypes = [c_char_p];
__gr.gr_beginprintext.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p];
__gr.gr_endprint.argtypes = [];
__gr.gr_ndctowc.argtypes = [POINTER(c_double), POINTER(c_double)];
__gr.gr_wctondc.argtypes = [POINTER(c_double), POINTER(c_double)];
__gr.gr_drawrect.argtypes = [c_double, c_double, c_double, c_double];
__gr.gr_fillrect.argtypes = [c_double, c_double, c_double, c_double];
__gr.gr_drawarc.argtypes = [c_double, c_double, c_double, c_double, c_int, c_int];
__gr.gr_fillarc.argtypes = [c_double, c_double, c_double, c_double, c_int, c_int];
__gr.gr_setarrowstyle.argtypes = [c_int];
__gr.gr_drawarrow.argtypes = [c_double, c_double, c_double, c_double];
__gr.gr_readimage.argtypes = [c_char_p, POINTER(c_int), POINTER(c_int), POINTER(POINTER(c_int))];
__gr.gr_drawimage.argtypes = [c_double, c_double, c_double, c_double, c_int, c_int, POINTER(c_int)];
__gr.gr_importgraphics.argtypes = [c_char_p];
__gr.gr_setshadow.argtypes = [c_double, c_double, c_double];
__gr.gr_settransparency.argtypes = [c_double];
__gr.gr_setcoordxform.argtypes = [POINTER(c_double)];
__gr.gr_begingraphics.argtypes = [c_char_p];
__gr.gr_endgraphics.argtypes = [];
__gr.gr_mathtex.argtypes = [c_double, c_double, c_char_p];
__gr.gr_beginselection.argtypes = [c_int, c_int];
__gr.gr_endselection.argtypes = [];
__gr.gr_moveselection.argtypes = [c_double, c_double];
__gr.gr_resizeselection.argtypes = [c_int, c_double, c_double];
__gr.gr_inqbbox.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)];

ASF_BUNDLED = 0
ASF_INDIVIDUAL = 1

NOCLIP = 0
CLIP = 1

COORDINATES_WC = 0
COORDINATES_NDC = 1

INTSTYLE_HOLLOW = 0
INTSTYLE_SOLID = 1
INTSTYLE_PATTERN = 2
INTSTYLE_HATCH = 3

TEXT_HALIGN_NORMAL = 0
TEXT_HALIGN_LEFT = 1
TEXT_HALIGN_CENTER = 2
TEXT_HALIGN_RIGHT = 3
TEXT_VALIGN_NORMAL = 0
TEXT_VALIGN_TOP = 1
TEXT_VALIGN_CAP = 2
TEXT_VALIGN_HALF = 3
TEXT_VALIGN_BASE = 4
TEXT_VALIGN_BOTTOM = 5

TEXT_PATH_RIGHT = 0
TEXT_PATH_LEFT = 1
TEXT_PATH_UP = 2
TEXT_PATH_DOWN = 3

TEXT_PRECISION_STRING = 0
TEXT_PRECISION_CHAR = 1
TEXT_PRECISION_STROKE = 2

LINETYPE_SOLID = 1
LINETYPE_DASHED = 2
LINETYPE_DOTTED = 3
LINETYPE_DASHED_DOTTED = 4
LINETYPE_DASH_2_DOT = -1
LINETYPE_DASH_3_DOT = -2
LINETYPE_LONG_DASH = -3
LINETYPE_LONG_SHORT_DASH = -4
LINETYPE_SPACED_DASH = -5
LINETYPE_SPACED_DOT = -6
LINETYPE_DOUBLE_DOT = -7
LINETYPE_TRIPLE_DOT = -8

MARKERTYPE_DOT = 1
MARKERTYPE_PLUS = 2
MARKERTYPE_ASTERISK = 3
MARKERTYPE_CIRCLE = 4
MARKERTYPE_DIAGONAL_CROSS = 5
MARKERTYPE_SOLID_CIRCLE = -1
MARKERTYPE_TRIANGLE_UP = -2
MARKERTYPE_SOLID_TRI_UP = -3
MARKERTYPE_TRIANGLE_DOWN = -4
MARKERTYPE_SOLID_TRI_DOWN = -5
MARKERTYPE_SQUARE = -6
MARKERTYPE_SOLID_SQUARE = -7
MARKERTYPE_BOWTIE = -8
MARKERTYPE_SOLID_BOWTIE = -9
MARKERTYPE_HOURGLASS = -10
MARKERTYPE_SOLID_HGLASS = -11
MARKERTYPE_DIAMOND = -12
MARKERTYPE_SOLID_DIAMOND = -13
MARKERTYPE_STAR = -14
MARKERTYPE_SOLID_STAR = -15
MARKERTYPE_TRI_UP_DOWN = -16
MARKERTYPE_SOLID_TRI_RIGHT = -17
MARKERTYPE_SOLID_TRI_LEFT = -18
MARKERTYPE_HOLLOW_PLUS = -19
MARKERTYPE_OMARK = -20

OPTION_X_LOG = 1
OPTION_Y_LOG = 2
OPTION_Z_LOG = 4
OPTION_FLIP_X = 8
OPTION_FLIP_Y = 16
OPTION_FLIP_Z = 32

OPTION_LINES = 0
OPTION_MESH = 1
OPTION_FILLED_MESH = 2
OPTION_Z_SHADED_MESH = 3
OPTION_COLORED_MESH = 4
OPTION_CELL_ARRAY = 5
OPTION_SHADED_MESH = 6

COLORMAP_UNIFORM = 0
COLORMAP_TEMPERATURE = 1
COLORMAP_GRAYSCALE = 2
COLORMAP_GLOWING = 3
COLORMAP_RAINBOW = 4
COLORMAP_GEOLOGIC = 5
COLORMAP_GREENSCALE = 6
COLORMAP_CYANSCALE = 7
COLORMAP_BLUESCALE = 8
COLORMAP_MAGENTASCALE = 9
COLORMAP_REDSCALE = 10
COLORMAP_FLAME = 11
COLORMAP_BROWNSCALE = 12
COLORMAP_BONE = 13
COLORMAP_USER_DEFINED = 14

FONT_TIMES_ROMAN = 101
FONT_TIMES_ITALIC = 102
FONT_TIMES_BOLD = 103
FONT_TIMES_BOLDITALIC = 104
FONT_HELVETICA = 105
FONT_HELVETICA_OBLIQUE = 106
FONT_HELVETICA_BOLD = 107
FONT_HELVETICA_BOLDOBLIQUE = 108
FONT_COURIER = 109
FONT_COURIER_OBLIQUE = 110
FONT_COURIER_BOLD = 111
FONT_COURIER_BOLDOBLIQUE = 112
FONT_SYMBOL = 113
FONT_BOOKMAN_LIGHT = 114
FONT_BOOKMAN_LIGHTITALIC = 115
FONT_BOOKMAN_DEMI = 116
FONT_BOOKMAN_DEMIITALIC = 117
FONT_NEWCENTURYSCHLBK_ROMAN = 118
FONT_NEWCENTURYSCHLBK_ITALIC = 119
FONT_NEWCENTURYSCHLBK_BOLD = 120
FONT_NEWCENTURYSCHLBK_BOLDITALIC = 121
FONT_AVANTGARDE_BOOK = 122
FONT_AVANTGARDE_BOOKOBLIQUE = 123
FONT_AVANTGARDE_DEMI = 124
FONT_AVANTGARDE_DEMIOBLIQUE = 125
FONT_PALATINO_ROMAN = 126
FONT_PALATINO_ITALIC = 127
FONT_PALATINO_BOLD = 128
FONT_PALATINO_BOLDITALIC = 129
FONT_ZAPFCHANCERY_MEDIUMITALIC = 130
FONT_ZAPFDINGBATS = 131

# gr.beginprint types
PRINT_PS   = "ps"
PRINT_EPS  = "eps"
PRINT_PDF  = "pdf"
PRINT_BMP  = "bmp"
PRINT_JPEG = "jpeg"
PRINT_JPG  = "jpg"
PRINT_PNG  = "png"
PRINT_TIFF = "tiff"
PRINT_TIF  = "tif"
PRINT_FIG  = "fig"
PRINT_SVG  = "svg"
PRINT_WMF  = "wmf"

PRINT_TYPE = { PRINT_PS   : "PostScript (*.ps)",
               PRINT_EPS  : "Encapsulated PostScript (*.eps)",
               PRINT_PDF  : "Portable Document Format (*.pdf)",
               PRINT_BMP  : "Windows Bitmap (*.bmp)",
               PRINT_JPEG : "JPEG image (*.jpg *.jpeg)",
               PRINT_PNG  : "Portable Network Graphics (*.png)",
               PRINT_TIFF : "Tagged Image File Format (*.tif *.tiff)",
               PRINT_FIG  : "Figure (*.fig)",
               PRINT_SVG  : "Scalable Vector Graphics (*.svg)",
               PRINT_WMF  : "Windows Metafile (*.wmf)"
}
# multiple keys
PRINT_TYPE[PRINT_JPG] = PRINT_TYPE[PRINT_JPEG]
PRINT_TYPE[PRINT_TIF] = PRINT_TYPE[PRINT_TIFF]

# gr.begingraphics types
GRAPHIC_GRX = "grx"

GRAPHIC_TYPE = { GRAPHIC_GRX : "Graphics Format (*.grx)" }