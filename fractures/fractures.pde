float waveHeight = 15; // wave amplitude
float timeStep = 0.01;
float t = 0;
color gapColor, borderColor;
int minGapSize = 5;
int maxGapSize = 40;

void setup() {
  size(600, 600);
  background(0);
  frameRate(1);
  gapColor = color(0);
  borderColor = color(255);
}

void draw() {
  stroke(0);
  strokeWeight(2);
  
  splitByCurveyLine();
}

void splitByCurveyLine() {
  PVector start, end;
  ArrayList<PVector> line = new ArrayList<PVector>();
  // left to right case
  if (random(2.0) < 1.0) {
    start = new PVector(0, int(random(height)));
    if (start.y <= height / 2) {
      end = new PVector(width, int(random(height/2) + height/2));
    } else {
      end = new PVector(width, int(random(height/2)));
    }
    
    for (int i = 0; i < width; i++) {
      float approxHeight = ((end.y - start.y) * i / width) + start.y;
      float lineY = approxHeight + int(map(noise(t), 0, 1, -waveHeight, waveHeight));
      t += timeStep;
      point(i, lineY);
      line.add(new PVector(i, lineY));
    }
    updateByHorizontalLine(line);
  } else {
    start = new PVector(int(random(width)), 0);
    if (start.x <= width / 2) {
      end = new PVector(int(random(width/2) + width/2), height);
    } else {
      end = new PVector(int(random(width/2)), height);
    }
    
    for (int i = 0; i >= 0 && i < height; i++) {
      float approxwidth = ((end.x - start.x) * i / height) + start.x;
      float lineX = approxwidth + int(map(noise(t), 0, 1, -waveHeight, waveHeight));
      t += timeStep;
      point(lineX, i);
      line.add(new PVector(lineX, i));
    }
    updateByVerticalLine(line);
  }
}

void updateByHorizontalLine(ArrayList<PVector> line) {
  int gapSize = int(random(maxGapSize - minGapSize)) + minGapSize;
  for (PVector p : line) {
    int x = int(p.x), y = int(p.y);
    loadPixels();
     
    ArrayList<Integer> lastPixels = halfPixelBuffer(gapSize);
    for (int i = (width * y) + x; i >= 0 && i < height * width; i -= width) {
      lastPixels.add(pixels[i]);
      pixels[i] = lastPixels.get(0);
      lastPixels.remove(0);
    }
     
    lastPixels = halfPixelBuffer(gapSize);
    for (int i = (width * y - 1) + x; i >= 0 && i < height * width; i += width) {
      lastPixels.add(pixels[i]);
      pixels[i] = lastPixels.get(0);
      lastPixels.remove(0);
    }
    updatePixels();
  }
}

void updateByVerticalLine(ArrayList<PVector> line) {
  int gapSize = int(random(maxGapSize - minGapSize)) + minGapSize;
  for (PVector p : line) {
    int x = int(p.x), y = int(p.y);
    loadPixels();
     
    ArrayList<Integer> lastPixels = halfPixelBuffer(gapSize);
    for (int i = (width * y) + x; i >= width * y && i < width * (y + 1); i += 1) {
      lastPixels.add(pixels[i]);
      pixels[i] = lastPixels.get(0);
      lastPixels.remove(0);
    }
     
    lastPixels = halfPixelBuffer(gapSize);
    for (int i = (width * y) + x + 1; i >= width * y && i < width * (y + 1); i -= 1) {
      lastPixels.add(pixels[i]);
      pixels[i] = lastPixels.get(0);
      lastPixels.remove(0);
    }
    updatePixels();
  }
}

ArrayList<Integer> halfPixelBuffer(int gapSize) {
  ArrayList<Integer> result = new ArrayList<Integer>();
  for (int i = 0; i < gapSize / 2 - 1; i++) {
    result.add(gapColor);
  }
  result.add(borderColor);
  return result;
}

