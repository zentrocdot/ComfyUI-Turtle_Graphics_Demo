# ComfyUI Turtle Graphics Demo

> [!IMPORTANT]  
> <p align="justify">🚧 This documentation is still under construction.
> Parts of the node are still under development. There may therefore be
> minor differences between the node itself and the documentation for
> the node. The documentation is also not yet complete.</p>

## Get Started

<p align="justify">Turtle Graphics has some interesting features. This 
node makes use of these capabilities. The aim is to show how beautiful
graphics can be created with Turtle Graphics.</p>

<p align="justify">It will explained later how Turtle Graphics works.
It has to be noted that Turtle Graphics makes use of the Python package
Tkinter. In variations of this nodes one can think about different cases
where Turtle Graphics or/and Tkinter can be used.</p>

<p align="justify">As part of the development I could show that it is not
necessary to save and load a Turtle Graphics for the later use. A canvas
created by Turtle Graphics can be streamed so it can be used as Pil image.</p> 

<p align="justify">The background of a Turtle Graphics image is by default
white. This is completely independent from the background of the screen where 
the graphics is drawn. By use of Numpy this white background can be removed
with a background of personal choice.</p> 

<p align="justify">If the background is exchanged by a black background it
is also possible to remove this background and make the background transparent.
</p> 

<p align="justify">Step by step some more demos to the existing ones 
will be added. The settings will result in a broader range of graphics
creations.</p> 

<p align="justify">This node is intended for demonstration purposes,
but you can use this node for some interesting things. One example is
the creation of colourful QR codes.</p>  

## Introduction

to do ...

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

## Node Settings

The node settings are largely self-explanatory. Accordingly, I am currently only providing a few comments.

## Turtle Graphics Squares Demo

### Node Preview

![image](https://github.com/user-attachments/assets/c45793e2-bb84-481c-a7b8-d3c155236783)

*Figure 1: Turtle Graphics Squares Demo*

### Graphics Examples

  📎     | Column 1            | Column 2         |   Column 3  
:----: | :-------------------------: | :-------------------------: | :----------------------------------:
Row 1 | ![ComfyUI_temp_otckr_00021_](https://github.com/user-attachments/assets/5a59d225-7401-4864-8334-992170004991) | ![ComfyUI_temp_otckr_00004_ (4)](https://github.com/user-attachments/assets/0037b51f-3923-4183-b34e-de4f3d9b848b) | ![ComfyUI_temp_otckr_00005_ (8)](https://github.com/user-attachments/assets/794afeba-5f9d-401a-8af6-cbab965823a5)
Row 2 | ![ComfyUI_temp_otckr_00009_ (2)](https://github.com/user-attachments/assets/8ea38ed5-aaad-421a-86cb-cfc1cebe9a80) | ![ComfyUI_temp_otckr_00029_](https://github.com/user-attachments/assets/05e5340f-3653-40cc-bc53-9a14e44d366d) | ![ComfyUI_temp_otckr_00040_](https://github.com/user-attachments/assets/22fc1d80-6b72-4464-ae84-8e44dc7ad81f)
Row 3 | ![ComfyUI_temp_otckr_00011_ (4)](https://github.com/user-attachments/assets/6b7bdd90-3fae-4354-b16c-a728386028c7) | ![ComfyUI_temp_otckr_00022_](https://github.com/user-attachments/assets/aa7b63e4-08cb-4e01-845a-baf333d887c0) | ![ComfyUI_temp_otckr_00026_](https://github.com/user-attachments/assets/d62e2ff7-d561-42d6-b79a-f625ff5b0b67)

### Turtle Graphics Spiral Demo Node

![image](https://github.com/user-attachments/assets/63fbd8ad-b69e-4745-a13e-b1ffb24ecb07)

*Figure 2: Turtle Graphics Spiral Demo*

 📎     | Column 1            | Column 2         |   Column 3  
:----: | :-------------------------: | :-------------------------: | :----------------------------------:
Row 1 | ![ComfyUI_temp_otckr_00002_ (4)](https://github.com/user-attachments/assets/12ae4099-5ac6-43c8-9670-068cb63f3b98) | ![ComfyUI_temp_otckr_00008_ (2)](https://github.com/user-attachments/assets/c5c5a48b-01a3-4d50-8cc2-23baa3c01afe) | ![ComfyUI_temp_otckr_00021_ (1)](https://github.com/user-attachments/assets/c86751f2-4488-4f71-a61b-9b02b888a1a2)
Row 2 | ![ComfyUI_temp_otckr_00027_](https://github.com/user-attachments/assets/dfe7fedd-6cea-4725-9e0b-fe443b24db16) | ![ComfyUI_temp_otckr_00005_ (10)](https://github.com/user-attachments/assets/12786dce-22bb-419b-b766-5fa0126ab304) | ![ComfyUI_temp_otckr_00028_](https://github.com/user-attachments/assets/b5ef6459-3dcb-4f8e-a133-16fbbdfbcef7)

### Circle Demo

![image](https://github.com/user-attachments/assets/faeb7fbd-e715-4a50-8116-1e39b7846d8d)

*Figure 3: Turtle Graphics Circle Demo*

  📎     | Column 1            | Column 2         |   Column 3  
:----: | :-------------------------: | :-------------------------: | :----------------------------------:
Row 1 | ![ComfyUI_temp_otckr_00030_](https://github.com/user-attachments/assets/d78b51bf-0efb-4c8b-a885-e4fc4e6fbc90) | ![ComfyUI_temp_otckr_00032_](https://github.com/user-attachments/assets/412b17e0-63e2-42c2-b522-e27eff587049) | ![ComfyUI_temp_otckr_00034_](https://github.com/user-attachments/assets/5701d9a3-ce5f-4e99-acad-ef6af2ba044a)

### Turtle Graphics Circle Lobes Demo Node 

#### Node Preview

<p align="justify">Figure 1 shows the Turtle Graphics Circle Lobes Demo  
node. The settings for the graphics are fully parameterised.</p> 

![image](https://github.com/user-attachments/assets/d39e57b6-1b57-4032-bd29-d5b354c8255b)

*Figure 4: Turtle Graphics Circle Lobes Demo*

#### Graphics Examples

  📎     | Column 1            | Column 2         |   Column 3  
:----: | :-------------------------: | :-------------------------: | :----------------------------------:
Row 1 | ![ComfyUI_temp_otckr_00005_ (7)](https://github.com/user-attachments/assets/5d3bcd8a-24ab-43d7-99e3-d29c0f38cef9) | ![ComfyUI_temp_otckr_00006_ (2)](https://github.com/user-attachments/assets/2db35f0b-4219-4007-afc3-856d729900d1) | ![ComfyUI_temp_otckr_00010_ (4)](https://github.com/user-attachments/assets/ef0e5a23-2228-4a34-863d-d2b0b47188cb)
Row 2 | ![ComfyUI_temp_otckr_00013_](https://github.com/user-attachments/assets/b03ca5e8-6a57-4665-b1fe-baa39944432a) | ![ComfyUI_temp_otckr_00015_ (1)](https://github.com/user-attachments/assets/62d14758-3954-4ed7-b204-0958ef0e0d41) | ![ComfyUI_temp_otckr_00016_](https://github.com/user-attachments/assets/b29f3a54-c7ec-477b-8d7f-f4aba416c81f)
Row 3 | ![ComfyUI_temp_tvbxm_00010_ (1)](https://github.com/user-attachments/assets/673a92f0-5dce-4e6f-a101-339f44379435) | ![ComfyUI_temp_tvbxm_00013_](https://github.com/user-attachments/assets/e495cab7-a1dd-4bfb-8061-d4a8b9d8f8ba) | ![ComfyUI_temp_tvbxm_00016_](https://github.com/user-attachments/assets/b7435ed4-1b19-47ca-9232-bb3e63946da9)


### Turtle Graphics Concate Lines Demo Node 

#### Node Preview

![image](https://github.com/user-attachments/assets/cf429848-f707-4e31-91be-6c5375c9cfc9)

*Figure 4: Turtle Graphics Concate Lines Demo*

#### Graphics Examples 

 📎     | Column 1            | Column 2         |   Column 3  
:----: | :-------------------------: | :-------------------------: | :----------------------------------:
Row 1 | ![ComfyUI_00532_](https://github.com/user-attachments/assets/b92000cc-ad23-42f7-8f84-dd010fc80465) | ![ComfyUI_00533_](https://github.com/user-attachments/assets/c6506e49-a2f4-45b9-a8b0-42bacc099c4f) | ![ComfyUI_00535_](https://github.com/user-attachments/assets/83e88c59-4ec6-4cf3-adc5-a6b16686b68b)
Row 2 | ![ComfyUI_00536_](https://github.com/user-attachments/assets/250ef0d0-fd64-4c17-93b5-0b154b86e88b) | ![ComfyUI_00540_](https://github.com/user-attachments/assets/ab326ec6-f8a4-47ff-8fff-caf9d3ffe20e) | ![ComfyUI_00545_](https://github.com/user-attachments/assets/ada442e1-2579-45b3-adbc-df5bb84eb22a)
Row 3 | ![ComfyUI_00556_](https://github.com/user-attachments/assets/3247fa60-a514-495c-b599-688cad35aec3) | ![ComfyUI_00557_](https://github.com/user-attachments/assets/5e277ed6-4b3f-4555-ad19-7a3f99de3017) | ![ComfyUI_00561_](https://github.com/user-attachments/assets/713bafee-595a-4756-b1d2-702e40964d65)

## Real Life Example

### Workflow Preview

![image](https://github.com/user-attachments/assets/047ef65d-6c86-4002-9b81-1e70e1b4ef8e)

### Example Images

  📎     | Turtle Graphics           | QR Code                     |   AI Image  
:----: | :-------------------------: | :-------------------------: | :-------------------------:
Images | ![ComfyUI_temp_voxnf_00024_ (1)](https://github.com/user-attachments/assets/6af4e8ba-3c52-4180-87a3-63b99bf749e7) | ![ComfyUI_temp_mzxdj_00009_](https://github.com/user-attachments/assets/1193ebc7-988f-4541-bbd9-3a790bad1e9b) | ![image](https://github.com/user-attachments/assets/663965d3-965d-4cd2-a1f5-66fed257abcb)

 

## Known Problems

### Tkinter Crash

<p align="justify">Tkinker crashes under unknown circumstances.
In general this can be resolved by restarting ComfyUI.</p>

### ComfyUI Crash

<p align="justify">Sometimes following error occures, when
closing to often a Turtle Graphics windows while Turtle
Graphics is still drawing.</p>

<pre>
RuntimeError: main thread is not in main loop
Tcl_AsyncDelete: async handler deleted by the wrong thread
</pre>  

<p align="justify">In general this can be resolved by restarting
ComfyUI.</p>

## Open Questions

<p align="justify">In real-life use of the node, a few questions
have arisen that require clarification. As long as I am using a
square format the resulting image is with or without upscaling in
his quality good. I used a landscape format and the image became 
blurry. It became even more blurred by changing the background.</p>

## Open Issues

<p align="justify">Opening and closing of a Turtle Graphics 
window or start and stop of a Turtle Graphics object is not
working as expected.</p>

## To-Do

<p align="justify">I need nodes where I can move the 
starting point of the Turtle Graphics from the center 
of the drawing area by offset values for x and y.</p>

# References

[1] https://docs.python.org/3/library/turtle.html
