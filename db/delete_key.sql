/* Delete one-time password */ DELETE
    FROM
        keys
    WHERE
        strServicio = UPPER(?)
        AND strOTP = UPPER(?)