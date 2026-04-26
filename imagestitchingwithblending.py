import numpy as np
import cv2 as cv

img1_raw = cv.imread('./apt01.jpg')
img2_raw = cv.imread('./apt02.jpg')
img3_raw = cv.imread('./apt03.jpg')
assert (img1_raw is not None) and (img2_raw is not None) and (img3_raw is not None), 'Cannot read the given images'

def resize_img(image, width=800):
    h, w = image.shape[:2]
    ratio = width / float(w)
    return cv.resize(image, (width, int(h * ratio)), interpolation=cv.INTER_AREA)

img1 = resize_img(img1_raw)
img2 = resize_img(img2_raw)
img3 = resize_img(img3_raw)

def blend_images(src_w, dst_w):
    mask_src = (cv.cvtColor(src_w, cv.COLOR_BGR2GRAY) > 0).astype(np.float32)
    mask_dst = (cv.cvtColor(dst_w, cv.COLOR_BGR2GRAY) > 0).astype(np.float32)
    
    dist_src = cv.distanceTransform(mask_src.astype(np.uint8), cv.DIST_L2, 3)
    dist_dst = cv.distanceTransform(mask_dst.astype(np.uint8), cv.DIST_L2, 3)
    
    sum_dist = dist_src + dist_dst
    alpha = np.where(sum_dist > 0, dist_src / sum_dist, 0)
    
    alpha = cv.merge([alpha, alpha, alpha])
    
    out = (src_w * alpha + dst_w * (1 - alpha)).astype(np.uint8)
    
    return out

fdetector = cv.BRISK_create()
fmatcher = cv.DescriptorMatcher_create('BruteForce-Hamming')

def get_H(src, dst):
    kp1, des1 = fdetector.detectAndCompute(dst, None)
    kp2, des2 = fdetector.detectAndCompute(src, None)
    match = fmatcher.match(des1, des2)
    pts1 = np.array([kp1[m.queryIdx].pt for m in match], dtype=np.float32)
    pts2 = np.array([kp2[m.trainIdx].pt for m in match], dtype=np.float32)
    H, _ = cv.findHomography(pts2, pts1, cv.RANSAC)
    return H

canvas_size = (img1.shape[1] * 3, img1.shape[0])

H12 = get_H(img2, img1)
img2_warped = cv.warpPerspective(img2, H12, canvas_size)

img1_canvas = np.zeros((canvas_size[1], canvas_size[0], 3), dtype=np.uint8)
img1_canvas[0:img1.shape[0], 0:img1.shape[1]] = img1

merged_12 = blend_images(img2_warped, img1_canvas)

H23 = get_H(img3, img2)
H13 = H12 @ H23 # img3를 img1 좌표계로 누적 변환
img3_warped = cv.warpPerspective(img3, H13, canvas_size)

img_final = blend_images(img3_warped, merged_12)

cv.imshow('3-Image Blending', img_final)
cv.waitKey(0)
cv.destroyAllWindows()