sw r1,0(r11)
movi r1,10
movi r2,5
movi r11,300
addi r11,r11,1
addi r1,r1,3
blt r11,r2,3
movi r11,3
lw r4,1(r11)