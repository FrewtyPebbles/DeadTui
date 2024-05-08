import os
from container import Container, ContainerStyle
from row import Row
from style import BorderStyle, FitType
import time

print("\033c")
counter = 0
frames = ['-','~','\\','|','/','~']
while True:
    if counter == len(frames):
        counter = 0    
    print(
        Row([
            Container([
                "This is in its own container!  This container also has word wrapping!",
                Container(
                    ["This is an inner container."],
                    style=ContainerStyle(
                        border=True
                    )
                )
            ], width=20,
            style=ContainerStyle(
                border=True,
                border_style=BorderStyle.SOLID,
                split_words = True,
                border_connect=(False,False,True,False)
            )),
            Container([
                Container([f"This plays a cool animation!"]),
                f"loading animation: {frames[counter]} loading..."
            ], width=20,
            style=ContainerStyle(
                border=True,
                split_words = False,
                border_connect=(True,False,False,False)
            )),
            Container(["third item."])
        ])
    )
    counter += 1
    time.sleep(0.1)
