/* Create table structure */
CREATE TABLE "keys" (
                        "idServicio"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                        "strServicio"	TEXT NOT NULL,
                        "strOTP"	TEXT NOT NULL
                    )