10 PRINT "MULTIPLICATION TEST, YOU HAVE 5 SECONDS"
20 FOR I = 2 TO 9
30 N = INT(RND*10) : A = N*I
40 PRINT "WHAT IS ",N,"*",I, "?": CLOCK1
50 TIME = 0 : ONTIME 5,200 : INPUT R : IF R<>A THEN 100
60 PRINT "THAT'S RIGHT":TIME=0 : NEXT I
70 PRINT "YOU DID IT, GOOD JOB" : END
100 PRINT "WRONG TRY AGAIN" : GOTO 50
200 REM WASTE CONTROL STACK, TOO MUCH TIME
210 CLEARS : PRINT "YOU TOOK TOO LONG":GOTO 10