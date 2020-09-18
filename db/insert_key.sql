/* Inserts one-time password */
INSERT INTO keys (strServicio, strOTP)
                values(UPPER(?), UPPER(?)) 
