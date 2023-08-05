from mooda.waterframe import WaterFrame
try:
    from mooda.plotmap import PlotMap
except ImportError:
    print("Warning: You do not have the basemap library installed. You cannot",
          "use PlotMap.")

name = "mooda"
__version__ = "0.1.0"
