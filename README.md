# ImageStitcher
### Stitching 3 images into planar panoramic view

- Used openCV findHomography() to find H matrix
- Matrix multiplication used H13 = H12@H23
- Used image blending technique(feathering mask) to avoid black borderline
- Alpha mask is calculated with the distance of two images

| Image 1 (Left) | Image 2 (Center) | Image 3 (Right) |
| :---: | :---: | :---: |
| <img src="https://github.com/user-attachments/assets/32c6135c-d278-4720-8f9b-af305c902c58" width="100%"> | <img src="https://github.com/user-attachments/assets/260a4f0f-7216-4261-87ba-1d8e5eb145f8" width="100%"> | <img src="https://github.com/user-attachments/assets/bc42c823-fd61-4735-a471-6d86f808d434" width="100%"> |

result
<img width="1909" height="1077" alt="result" src="https://github.com/user-attachments/assets/10afeb8c-8d85-4eaf-b338-da3a0a420e0c" />


