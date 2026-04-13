 Interactive Edge Detection Application using OpenCV and PyQt5

📌 Overview

This project is a graphical user interface (GUI) application developed in Python for detecting edges in images using classical computer vision techniques.
It was built as part of a Computer Vision lab to explore first-order and second-order derivative methods for edge detection.

The application allows users to load an image, apply different edge detection filters, and visualize the results interactively.


 🎯 Objectives

* Understand edge detection based on image gradients
* Implement convolution manually (Prewitt & Sobel)
* Explore second-order derivatives (Laplacian & LoG)
* Apply advanced edge detection using the Canny algorithm
* Build an interactive GUI for visualization


🛠️ Technologies Used

* Python
* OpenCV
* NumPy
* PyQt5



## ⚙️ Features

🔹 Image Processing

* Load and display an image
* Convert image to grayscale

🔹 First Derivative Methods

* Prewitt filter (manual implementation)
* Sobel filter (manual + OpenCV)
* Gradient magnitude computation

🔹 Thresholding

* Adjustable threshold values
* Binary edge segmentation

🔹 Second Derivative Methods

* Laplacian edge detection
* Laplacian of Gaussian (LoG)

🔹 Advanced Detection

* Canny edge detector (thin and connected edges)

🔹 Graphical Interface

* Interactive buttons and controls
* Real-time visualization of results


 🖥️ Application Interface

The GUI includes:

* Image selection (Browse button)
* Grayscale image display
* Filter selection (Prewitt / Sobel)
* Threshold input fields
* Output displays for:

  * Gradient edges
  * Segmented image
  * Laplacian
  * LoG
  * Canny
