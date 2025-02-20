# ComfyUI Turtle Graphics Demo

## Get Started

Turtle Graphics has some interesting features. This nodes makes use of these features. The goal is to show
how Turtle Graphics can be used to create beautiful square graphics.

This node is for demonstration purposes but one can use this node for some interesting things. One example
is the creation of colorful QR codes. 

It will explained later how Turtle Graphics works. It has to be noted that Turtle Graphics makes use of Tkinter.
In variations of this nodes one can think about different cases where Turtle Graphics or/and Tkinter can be used.

Step by step some more demos to the existing ones will be added. The settings will result in a broader range of
graphics. 

As part of the development I could show that it us not necessary to save and load a Turtle Graphics for later
use. The canvas can be streamt so it can be used as Pil image.

The background of a Turtle Graphics image is by default white. This is right independent from the background 
of the screen where the graphics is drawn. By use of Jumpy this white background can be removed with a 
background of personal choice.

If the background is exchanged by a black background it us also possible to remove the background.

To be cont'd

## Main Goals

One goal is to use the node as Turtle Graphics demonstrator and to play with settings of a special demo.

Another goal is it to provide graphics to other applications. One exaample will be given later. The turtle 
Graphics can be used for colorising QR codes. 

## Turtle Graphics

In this node I made use of the special character of the Python module Turtle Graphics. As long one waits
untill the image is drawn everything is fine. If not it could be that the code will  have a short confusion 
in form of a catched error in the background. 

Turtle Graphics is using Tkinter for the windows management. Starting a draw command Turtle Graphics is 
opening a window for drawing. Within the node one can decide to show this window or not.

One can decide to let a turtle or another shape drawing the image. This can also be set in the node.

## Turtle Graphics Spiral Demo

### Square Node

![image](https://github.com/user-attachments/assets/d6a191c8-2e52-4ad1-b571-9847834bc52f)

*Figure 1: Turtle Graphics Square Demo*

### Graphics Examples

  📎     | Column 1            | Column 2         |   Column 3  
:----: | :-------------------------: | :-------------------------: | :----------------------------------:
Row 1 | ![ComfyUI_temp_otckr_00021_](https://github.com/user-attachments/assets/5a59d225-7401-4864-8334-992170004991) | ![ComfyUI_temp_otckr_00004_ (4)](https://github.com/user-attachments/assets/0037b51f-3923-4183-b34e-de4f3d9b848b) | ![ComfyUI_temp_otckr_00005_ (8)](https://github.com/user-attachments/assets/794afeba-5f9d-401a-8af6-cbab965823a5)
Row 2 | ![ComfyUI_temp_otckr_00009_ (2)](https://github.com/user-attachments/assets/8ea38ed5-aaad-421a-86cb-cfc1cebe9a80) | ![ComfyUI_temp_otckr_00029_](https://github.com/user-attachments/assets/05e5340f-3653-40cc-bc53-9a14e44d366d) | ![ComfyUI_temp_otckr_00040_](https://github.com/user-attachments/assets/22fc1d80-6b72-4464-ae84-8e44dc7ad81f)
Row 3 | ![ComfyUI_temp_otckr_00011_ (4)](https://github.com/user-attachments/assets/6b7bdd90-3fae-4354-b16c-a728386028c7) | ![ComfyUI_temp_otckr_00022_](https://github.com/user-attachments/assets/aa7b63e4-08cb-4e01-845a-baf333d887c0) | ![ComfyUI_temp_otckr_00026_](https://github.com/user-attachments/assets/d62e2ff7-d561-42d6-b79a-f625ff5b0b67)


### Helix Node

![image](https://github.com/user-attachments/assets/63fbd8ad-b69e-4745-a13e-b1ffb24ecb07)

*Figure 2: Turtle Graphics Helix Demo*

 📎     | Column 1            | Column 2         |   Column 3  
:----: | :-------------------------: | :-------------------------: | :----------------------------------:
Row 1 | ![ComfyUI_temp_otckr_00002_ (4)](https://github.com/user-attachments/assets/12ae4099-5ac6-43c8-9670-068cb63f3b98) |
![ComfyUI_temp_otckr_00008_ (2)](https://github.com/user-attachments/assets/c5c5a48b-01a3-4d50-8cc2-23baa3c01afe) |
![ComfyUI_temp_otckr_00021_ (1)](https://github.com/user-attachments/assets/c86751f2-4488-4f71-a61b-9b02b888a1a2)
Row 2 | ![ComfyUI_temp_otckr_00027_](https://github.com/user-attachments/assets/dfe7fedd-6cea-4725-9e0b-fe443b24db16) |
![ComfyUI_temp_otckr_00005_ (10)](https://github.com/user-attachments/assets/12786dce-22bb-419b-b766-5fa0126ab304) |
![ComfyUI_temp_otckr_00028_](https://github.com/user-attachments/assets/b5ef6459-3dcb-4f8e-a133-16fbbdfbcef7)

### Circle Demo

![image](https://github.com/user-attachments/assets/faeb7fbd-e715-4a50-8116-1e39b7846d8d)

*Figure 3: Turtle Graphics Circle Demo*

  📎     | Column 1            | Column 2         |   Column 3  
:----: | :-------------------------: | :-------------------------: | :----------------------------------:
Row 1 | ![ComfyUI_temp_otckr_00030_](https://github.com/user-attachments/assets/d78b51bf-0efb-4c8b-a885-e4fc4e6fbc90) | ![ComfyUI_temp_otckr_00032_](https://github.com/user-attachments/assets/412b17e0-63e2-42c2-b522-e27eff587049) | ![ComfyUI_temp_otckr_00034_](https://github.com/user-attachments/assets/5701d9a3-ce5f-4e99-acad-ef6af2ba044a)

### Spiral Node 

<p align="justify">Figure 1 shows the Turtle Graphics Spiral Demo 
node. The settings for the graphics are fully parameterised.</p> 

![image](https://github.com/user-attachments/assets/9d315296-cd2f-439d-afae-aa740b8653b8)

*Figure 4: Turtle Graphics Spiral Demo*

### Graphics Examples

  📎     | Column 1            | Column 2         |   Column 3  
:----: | :-------------------------: | :-------------------------: | :----------------------------------:
Row 1 | ![ComfyUI_temp_otckr_00005_ (7)](https://github.com/user-attachments/assets/5d3bcd8a-24ab-43d7-99e3-d29c0f38cef9) | ![ComfyUI_temp_otckr_00006_ (2)](https://github.com/user-attachments/assets/2db35f0b-4219-4007-afc3-856d729900d1) | ![ComfyUI_temp_otckr_00010_ (4)](https://github.com/user-attachments/assets/ef0e5a23-2228-4a34-863d-d2b0b47188cb)
Row 2 | ![ComfyUI_temp_otckr_00013_](https://github.com/user-attachments/assets/b03ca5e8-6a57-4665-b1fe-baa39944432a) | ![ComfyUI_temp_otckr_00015_ (1)](https://github.com/user-attachments/assets/62d14758-3954-4ed7-b204-0958ef0e0d41) | ![ComfyUI_temp_otckr_00016_](https://github.com/user-attachments/assets/b29f3a54-c7ec-477b-8d7f-f4aba416c81f)
Row 3 | ![ComfyUI_temp_tvbxm_00010_ (1)](https://github.com/user-attachments/assets/673a92f0-5dce-4e6f-a101-339f44379435) | ![ComfyUI_temp_tvbxm_00013_](https://github.com/user-attachments/assets/e495cab7-a1dd-4bfb-8061-d4a8b9d8f8ba) | ![ComfyUI_temp_tvbxm_00016_](https://github.com/user-attachments/assets/b7435ed4-1b19-47ca-9232-bb3e63946da9)

## Known Problems

<p align="justify">Tkinker crashes under unknown circumstances. This can be resolved by restarting ComfyUI.</p>

Unsolved Error:

RuntimeError: main thread is not in main loop

Tcl_AsyncDelete: async handler deleted by the wrong thread

## Open Issues

Opening and closing of a Turtle Graphics window or start and stop of a Turtle Graphics object is not working as expected.

# References

[1] https://docs.python.org/3/library/turtle.html
