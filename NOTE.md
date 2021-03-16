## Main Differences

**Modelbench (.mimodel)**

>   use part pivot rotation for object pivot rotation
> 
>   restricted UV


**Blockbench (.json - Minecraft Java)**

>   use self object pivot rotation
>   
>   flexible UV
<br/>

### TODOs:

|          Blockbench           |           Modelbench              |     Status     |
| ----------------------------- | --------------------------------- | -------------- |
| Self object name Blockbench| Modelbench part name; if None cube + number list, the same goes for shape name| **Done**|
| element position NONE         | part position = element origin for pivoting              | **Done**       | 
| element (position) "from" "to"| shapes "from" "to" *"size"*       | **Done**       |
| element rotation              | part rotation as pivot for shape   | **Done** |
| flexible scale UV                            | restricted UV                                | ***Not Done*** |
<br/>
##
### Ideas for implementations:
- **UV**
> ~~1. OpenGL to generate new texture for Modelbench UV layout or OpenCV move texture based on UV Layout.~~
>> - **Possibly** dealing with weird texture ratio scale? stretch UV (cause of different user adjusted UV scale in Blockbench).
>> - Add extra library.
>
> 2. Adjust override Blockbench json UV layout based on Modelbench and let the *users* make texture using that layout.
>> - Nicer, Simple option; less annoying to implement.
>> - ...

- **Pivot Rotation**
> *You already knew the best way to do this. but still wrote this down* **HUH??** ***MA~~X~~MIAN*** 



*Blockbench have generic model convert might look into that.*

