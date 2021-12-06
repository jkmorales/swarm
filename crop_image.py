R=[i for i in range(135,146)]
G=[i for i in range(169,180)]
B=[i for i in range(0,5)]

def crop_image(image):
  print(image.shape)
  coordenadas = {
    'menor':(1024,1024),
    'mayor':(0,0),
    'last':(image.shape[1],image.shape[0])
    }
  cv2_imshow(image)
  x=0
  y=0
  for img in image:
    for i in img:
      if i[0] in B and i[1] in G and i[2] in R:
        if 'first' not in coordenadas:
          coordenadas['first'] = (y,x)
        if x < coordenadas['menor'][1]:
          coordenadas['menor'] = (y,x)
        if x > coordenadas['mayor'][1]:
          coordenadas['mayor'] = (y,x)        
        coordenadas['last'] = (y,x)
      x=x+1
    x=0
    y=y+1

  x_ = coordenadas['menor'][1]
  y_ = coordenadas['first'][0]
  h_ = coordenadas['last'][0]-coordenadas['first'][0]
  w_ = coordenadas['mayor'][1]-coordenadas['menor'][1]

  # print(x_,y_,h_,w_)
  # print(coordenadas)

  crop_ = image[y_:y_+h_, x_:x_+w_]
  cv2_imshow(crop_)

  return x_,y_,h_,w_