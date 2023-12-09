import cv2
import numpy as np

imgOG=cv2.imread('pavNero.png')

cv2.imshow('1',imgOG)
cv2.waitKey(0)

imgBN=cv2.cvtColor(imgOG,cv2.COLOR_BGR2GRAY)


cv2.imshow('1',imgBN)
cv2.waitKey(0)

imgBN=cv2.medianBlur(imgBN,5)

cv2.imshow('1',imgBN)
cv2.waitKey(0)

imgBN=255-imgBN

cv2.imshow('1',imgBN)
cv2.waitKey(0)

maxN=np.max(imgBN)
imgBN=imgBN-maxN+255

cv2.imshow('1',imgBN)
cv2.waitKey(0)

cv2.imwrite('risulatatoImgOffset.png',imgBN)
