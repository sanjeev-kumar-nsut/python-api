from flask import Flask,jsonify,render_template
from flask import request    
from urllib.request import urlopen
import urllib.request
from colormap import rgb2hex
import io
from PIL import Image
from colorthief import ColorThief
from numpy import asarray
import numpy as np
import cv2

app = Flask(__name__)


@app.route('/')
def index():
    src = request.query_string
    if(src):
      img = src[4:]
      imglink = img.decode("utf-8")
      fd = urlopen(imglink)
      f = io.BytesIO(fd.read())
      color_thief = ColorThief(f)
      rgb1 = color_thief.get_color(quality=1)
      urllib.request.urlretrieve(imglink,"sample.png")
      sampleImg = Image.open("sample.png")
      sampleData = asarray(sampleImg)
      row = sampleData.shape[0]
      col = sampleData.shape[1]
      r=0
      g=0
      b=0
      for i in range(10):
          for j in range(col):
                r = r+sampleData[i][j][0]
                g = g+sampleData[i][j][1]
                b = b+sampleData[i][j][2]
      for i in range(col-10,col):
          for j in range(row):
                r = r+sampleData[j][i][0]
                g = g+sampleData[j][i][1]
                b = b+sampleData[j][i][2]
      for i in range(row-10,row):
          for j in range(col):
                r = r+sampleData[i][j][0]
                g = g+sampleData[i][j][1]
                b = b+sampleData[i][j][2]
      for i in range(10):
          for j in range(row):
                r = r+sampleData[i][j][0]
                g = g+sampleData[i][j][1]
                b = b+sampleData[i][j][2]
      r = int(r/(20*(row+col)))
      g = int(g/(20*(row+col)))
      b = int(b/(20*(row+col)))
      result = {
          "logo_border": rgb2hex(r,g,b),
          "dominant_color": rgb2hex(rgb1[0],rgb1[1],rgb1[2])
      }
      return jsonify(result)
    else:
        return render_template("home.html")
 
if __name__ == "__main__":
    app.run(debug=True)