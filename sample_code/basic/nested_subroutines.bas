10 FOR I = 1 TO 3
20 GOSUB 100
30 NEXT I
40 END
100 PRINT I,
110 GOSUB 200
120 RETURN
200 PRINT I*I
210 RETURN
