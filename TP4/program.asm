main:
    mov @100 #72
    mov @101 #101
    mov @102 #108
    mov @103 #108
    mov @104 #111
    mov @105 #32
    mov @106 #87
    mov @107 #111
    mov @108 #114
    mov @109 #108
    mov @110 #100
    mov @111 #33
    mov @112 #12351

    mov r1 #100
    mov r2 #0

loop:
    prc !r1,r2 
    add r2 r2 #1
    bne loop r2 #12
    prc #10

;;la consommation est lié directement au nombre de bit à 1

