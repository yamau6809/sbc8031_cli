5  STRING 100,10
10 $(1)="SECRET" : REM SECRET IS THE PASSWORD
20 INPUT "WHAT'S THE PASSWORD - ",$(2)
30 FOR T=1 TO 6
40 IF ASC($(1),T)=ASC($(2),T) THEN NEXT T ELSE 70
50 PRINT "YOU GUESSED IT"
60 END
70 PRINT "WRONG, TRY AGAIN" : GOTO 20