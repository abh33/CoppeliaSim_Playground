from datetime import datetime
import platform
import uuid
import gspread
def send_to_sheets(data):

    headers=[
    'Date and Time',
    'Platform',
    'Mac',
    'Task No.',
    'Task Output',
    'Score'
    ]

    copsim = {
    "type": "service_account",
    "project_id": "coppeliasim-playground",
    "private_key_id": "2334b85e78cddfdf9254a39ca90f9c1e8661e38a",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCiMDdbCyS90tU5\nXBOO8cBD3Ic9p266o298jiXhYlW2QiSBh/YCjA6aRQdNF1J3oZfWXSIc6eYh03ki\nZ1fg5ZWEMn3pExMSGHs3HMCqE2O7fJzXhrUQoAH9r9DvptulYK4mzkFw6jaD9RJM\nVYUNVnGA70d1nT1mFsmPxAgVM075JuuK9m6DxUKiiTuIZIfSpoGsGLus3fV/J5v+\nPWMuZC6ps/PAtkWUtUzzTcKMi/sMcM9fBpW0t0dhsc04u6FbW6ag3BQ+Xl15ef3K\nXJob6CqHLMMdBNvVnQe0VNZmIXMF78qWrTqKnxLCtjpNFyQImOeuTxI4BZ1UKKcG\nZ9xRRuUtAgMBAAECggEAJ51eT/sTUNg344hFcLNE0m6BjAIi7ixwVTyFLR1vMRLL\nxuW2JZ4fDPhSVbaeGoFaTG44IFbTMqzsGAak9NYu5HjOv0i87j0Tj30S5BfTUt6X\nkp8hB7wFcHjqsDaRzL2mG+1iF5nlkeqguwticcUM+UC4tBYhgpeLSPXJQaBkKD/B\nULjIIYJ86kQl2bvMiUff1IokriqZ6ryIm3PxcdwYqFYBt6vqVf/KwIdOTD1+FTtG\nms+rBrBCF3/Uv1MLlOCMVdQXtroKKUHE1Pk7KiEkPwURHCb/DwIvtPUGiKP5mLNh\nstENkjnKlIE4qlYhQWQoZxckEFMtXj0MN2DKKieLMQKBgQDRokDKnUUW1vyl7I6K\nBVq/987MGFQO11z0dLg/SBdY75Y64MJAhVTgAgxrPvPnRRdMQS4n9SctbQIOlmS4\njOcWfzXuyISPJfEvy76sNCzj2yLDglUtANYnlnWnfA/fRxAvR6kaUyStVyT94h/z\npHrYXm/yGjuEoPlv0SQ5fFCUZQKBgQDGD4mr0/ixGLhQZSOfabQ74V9CIvah+GDu\nNVGZGIgsvkma0GX7cy8PiHajieOe5NeTYStkdX0zptH7DSQH34Z2ldwUkz2wXhtH\nUV5+KvWJ6v0RAjIvtvR1aZOcX1NXrtVVRjlmDzw0VZ7sQSYBb88wJgzs7tLXXzWK\nmice6R4NKQKBgQCdM1f02HSryPHSlw7Yj2VbGUA5KnE2Y+dv5WsZAT2I0rlMU6k3\nawSXqtGXRrDuF5B9/U7YZe1IEjt9pufGwNq1sxVFh5ZoJiK0HcxRJBsZjwWFqOGo\nir0NGLYHr2/Tll2bptg3Rmv1lKjHvd8J/KimQkMeQO+q6G/EmwfYF9HxRQKBgQCs\nW4krBuQ8+Y4sKFe/unUmRxJms5Z9jXCM28mOuVKH3XCgUQrur2Yc1lyoJK7475zK\nnJzuZ2/1Kw9AskbQsyyIthE3torQmJSUk7LviOL0ipJ/4rFZ5JUIOEBErJASlgsA\nkoQQ1OFHidsrLeatCWf8NqC473x8AFbPryasN6H3QQKBgFvkzmP/y1iXG6SB22As\n4Qi0Setgp1ltu11hdyU6OjmvLX+hLVQCXLnGzafsNqukSDcpmy3DplOl3laQqQjB\nWRbyZyS6syJzc3IN4j8D8rV+st8aSCLqeQuIBfv+sV8KJfMHVRrpQHOaYcSWAJWP\n3lUJsK6F2jqv6VNlL+n4j/R9\n-----END PRIVATE KEY-----\n",
    "client_email": "copsim@coppeliasim-playground.iam.gserviceaccount.com",
    "client_id": "110686459353082313226",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/copsim%40coppeliasim-playground.iam.gserviceaccount.com"
    }
    curr_date_time      = str(datetime.now())
    platform_uname = platform.uname().system

    submission_attempts=0

    flag_data_sent_successfully=0 # 0- Failed sending data, 1- Successfully sent data OR Master Flag in the sheet is 0 (Can be done manually ONLY). 

    while submission_attempts<5:
        # print('\n#################################################################')
        # print('\nAttempting to send data to e-Yantra Servers.')
        # print('\nMake sure you have an active internet connection.')

        try:
            gc = gspread.service_account_from_dict(copsim)
            sh = gc.open_by_key("1LK9K4a3y2-j2HZOXZPtMqCQG224zlBk-TCQE5RZgeyg") # or by sheet name: gc.open("TestList")
            wksheet = sh.sheet1		
            wksheet.update('A1:F1',[headers])
            row_num_to_write=len(wksheet.get_all_values())+1 # This will give number of rows which are filled.
            #print(row_num_to_write)
            data_to_push = [curr_date_time, platform_uname, str(hex(uuid.getnode())),data[0],data[1],data[2]]

            wksheet.update('A'+str(row_num_to_write)+':F'+str(row_num_to_write),[data_to_push])

            if(len(wksheet.get_all_values())+1==row_num_to_write+1): # Verifying if the row is filled or not.
                # print("\nSuccessfully sent data to e-Yantra Servers.")
                # print('\n#################################################################')
                submission_attempts=5
                flag_data_sent_successfully=1

        
        except:
            submission_attempts+=1
            flag_data_sent_successfully=0
            # traceback.print_exc(file=sys.stdout)
            # print()
            # print('\nFAILED sending the data.')
            # print('\nNumber of times remaining: ',5-submission_attempts)

    return flag_data_sent_successfully

def clickStreamData(csdata):
    header=['Date and Time','Click Stream Data']
    copsim = {
    "type": "service_account",
    "project_id": "coppeliasim-playground",
    "private_key_id": "2334b85e78cddfdf9254a39ca90f9c1e8661e38a",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCiMDdbCyS90tU5\nXBOO8cBD3Ic9p266o298jiXhYlW2QiSBh/YCjA6aRQdNF1J3oZfWXSIc6eYh03ki\nZ1fg5ZWEMn3pExMSGHs3HMCqE2O7fJzXhrUQoAH9r9DvptulYK4mzkFw6jaD9RJM\nVYUNVnGA70d1nT1mFsmPxAgVM075JuuK9m6DxUKiiTuIZIfSpoGsGLus3fV/J5v+\nPWMuZC6ps/PAtkWUtUzzTcKMi/sMcM9fBpW0t0dhsc04u6FbW6ag3BQ+Xl15ef3K\nXJob6CqHLMMdBNvVnQe0VNZmIXMF78qWrTqKnxLCtjpNFyQImOeuTxI4BZ1UKKcG\nZ9xRRuUtAgMBAAECggEAJ51eT/sTUNg344hFcLNE0m6BjAIi7ixwVTyFLR1vMRLL\nxuW2JZ4fDPhSVbaeGoFaTG44IFbTMqzsGAak9NYu5HjOv0i87j0Tj30S5BfTUt6X\nkp8hB7wFcHjqsDaRzL2mG+1iF5nlkeqguwticcUM+UC4tBYhgpeLSPXJQaBkKD/B\nULjIIYJ86kQl2bvMiUff1IokriqZ6ryIm3PxcdwYqFYBt6vqVf/KwIdOTD1+FTtG\nms+rBrBCF3/Uv1MLlOCMVdQXtroKKUHE1Pk7KiEkPwURHCb/DwIvtPUGiKP5mLNh\nstENkjnKlIE4qlYhQWQoZxckEFMtXj0MN2DKKieLMQKBgQDRokDKnUUW1vyl7I6K\nBVq/987MGFQO11z0dLg/SBdY75Y64MJAhVTgAgxrPvPnRRdMQS4n9SctbQIOlmS4\njOcWfzXuyISPJfEvy76sNCzj2yLDglUtANYnlnWnfA/fRxAvR6kaUyStVyT94h/z\npHrYXm/yGjuEoPlv0SQ5fFCUZQKBgQDGD4mr0/ixGLhQZSOfabQ74V9CIvah+GDu\nNVGZGIgsvkma0GX7cy8PiHajieOe5NeTYStkdX0zptH7DSQH34Z2ldwUkz2wXhtH\nUV5+KvWJ6v0RAjIvtvR1aZOcX1NXrtVVRjlmDzw0VZ7sQSYBb88wJgzs7tLXXzWK\nmice6R4NKQKBgQCdM1f02HSryPHSlw7Yj2VbGUA5KnE2Y+dv5WsZAT2I0rlMU6k3\nawSXqtGXRrDuF5B9/U7YZe1IEjt9pufGwNq1sxVFh5ZoJiK0HcxRJBsZjwWFqOGo\nir0NGLYHr2/Tll2bptg3Rmv1lKjHvd8J/KimQkMeQO+q6G/EmwfYF9HxRQKBgQCs\nW4krBuQ8+Y4sKFe/unUmRxJms5Z9jXCM28mOuVKH3XCgUQrur2Yc1lyoJK7475zK\nnJzuZ2/1Kw9AskbQsyyIthE3torQmJSUk7LviOL0ipJ/4rFZ5JUIOEBErJASlgsA\nkoQQ1OFHidsrLeatCWf8NqC473x8AFbPryasN6H3QQKBgFvkzmP/y1iXG6SB22As\n4Qi0Setgp1ltu11hdyU6OjmvLX+hLVQCXLnGzafsNqukSDcpmy3DplOl3laQqQjB\nWRbyZyS6syJzc3IN4j8D8rV+st8aSCLqeQuIBfv+sV8KJfMHVRrpQHOaYcSWAJWP\n3lUJsK6F2jqv6VNlL+n4j/R9\n-----END PRIVATE KEY-----\n",
    "client_email": "copsim@coppeliasim-playground.iam.gserviceaccount.com",
    "client_id": "110686459353082313226",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/copsim%40coppeliasim-playground.iam.gserviceaccount.com"
    }
    flag_data_sent_successfully=0 # 0- Failed sending data, 1- Successfully sent data OR Master Flag in the sheet is 0 (Can be done manually ONLY). 
    try:
        gc = gspread.service_account_from_dict(copsim)
        sh = gc.open_by_key("1LK9K4a3y2-j2HZOXZPtMqCQG224zlBk-TCQE5RZgeyg") # or by sheet name: gc.open("TestList")
        wksheet = sh.get_worksheet(1)		
        wksheet.update('A1:B1',[header])
        #print(row_num_to_write,wksheet.get_values('H:I'))
        for data in csdata:
            row_num_to_write=len(wksheet.get_all_values())+1 # This will give number of rows which are filled.
            data_to_push = [data[0],data[1]]
            wksheet.update('A'+str(row_num_to_write)+':B'+str(row_num_to_write),[data_to_push])
        flag_data_sent_successfully=1

    
    except:
        flag_data_sent_successfully=0

    print(flag_data_sent_successfully)

def getSaveData():
    copsim = {
    "type": "service_account",
    "project_id": "coppeliasim-playground",
    "private_key_id": "2334b85e78cddfdf9254a39ca90f9c1e8661e38a",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCiMDdbCyS90tU5\nXBOO8cBD3Ic9p266o298jiXhYlW2QiSBh/YCjA6aRQdNF1J3oZfWXSIc6eYh03ki\nZ1fg5ZWEMn3pExMSGHs3HMCqE2O7fJzXhrUQoAH9r9DvptulYK4mzkFw6jaD9RJM\nVYUNVnGA70d1nT1mFsmPxAgVM075JuuK9m6DxUKiiTuIZIfSpoGsGLus3fV/J5v+\nPWMuZC6ps/PAtkWUtUzzTcKMi/sMcM9fBpW0t0dhsc04u6FbW6ag3BQ+Xl15ef3K\nXJob6CqHLMMdBNvVnQe0VNZmIXMF78qWrTqKnxLCtjpNFyQImOeuTxI4BZ1UKKcG\nZ9xRRuUtAgMBAAECggEAJ51eT/sTUNg344hFcLNE0m6BjAIi7ixwVTyFLR1vMRLL\nxuW2JZ4fDPhSVbaeGoFaTG44IFbTMqzsGAak9NYu5HjOv0i87j0Tj30S5BfTUt6X\nkp8hB7wFcHjqsDaRzL2mG+1iF5nlkeqguwticcUM+UC4tBYhgpeLSPXJQaBkKD/B\nULjIIYJ86kQl2bvMiUff1IokriqZ6ryIm3PxcdwYqFYBt6vqVf/KwIdOTD1+FTtG\nms+rBrBCF3/Uv1MLlOCMVdQXtroKKUHE1Pk7KiEkPwURHCb/DwIvtPUGiKP5mLNh\nstENkjnKlIE4qlYhQWQoZxckEFMtXj0MN2DKKieLMQKBgQDRokDKnUUW1vyl7I6K\nBVq/987MGFQO11z0dLg/SBdY75Y64MJAhVTgAgxrPvPnRRdMQS4n9SctbQIOlmS4\njOcWfzXuyISPJfEvy76sNCzj2yLDglUtANYnlnWnfA/fRxAvR6kaUyStVyT94h/z\npHrYXm/yGjuEoPlv0SQ5fFCUZQKBgQDGD4mr0/ixGLhQZSOfabQ74V9CIvah+GDu\nNVGZGIgsvkma0GX7cy8PiHajieOe5NeTYStkdX0zptH7DSQH34Z2ldwUkz2wXhtH\nUV5+KvWJ6v0RAjIvtvR1aZOcX1NXrtVVRjlmDzw0VZ7sQSYBb88wJgzs7tLXXzWK\nmice6R4NKQKBgQCdM1f02HSryPHSlw7Yj2VbGUA5KnE2Y+dv5WsZAT2I0rlMU6k3\nawSXqtGXRrDuF5B9/U7YZe1IEjt9pufGwNq1sxVFh5ZoJiK0HcxRJBsZjwWFqOGo\nir0NGLYHr2/Tll2bptg3Rmv1lKjHvd8J/KimQkMeQO+q6G/EmwfYF9HxRQKBgQCs\nW4krBuQ8+Y4sKFe/unUmRxJms5Z9jXCM28mOuVKH3XCgUQrur2Yc1lyoJK7475zK\nnJzuZ2/1Kw9AskbQsyyIthE3torQmJSUk7LviOL0ipJ/4rFZ5JUIOEBErJASlgsA\nkoQQ1OFHidsrLeatCWf8NqC473x8AFbPryasN6H3QQKBgFvkzmP/y1iXG6SB22As\n4Qi0Setgp1ltu11hdyU6OjmvLX+hLVQCXLnGzafsNqukSDcpmy3DplOl3laQqQjB\nWRbyZyS6syJzc3IN4j8D8rV+st8aSCLqeQuIBfv+sV8KJfMHVRrpQHOaYcSWAJWP\n3lUJsK6F2jqv6VNlL+n4j/R9\n-----END PRIVATE KEY-----\n",
    "client_email": "copsim@coppeliasim-playground.iam.gserviceaccount.com",
    "client_id": "110686459353082313226",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/copsim%40coppeliasim-playground.iam.gserviceaccount.com"
    }
    try:
        gc = gspread.service_account_from_dict(copsim)
        sh = gc.open_by_key("1LK9K4a3y2-j2HZOXZPtMqCQG224zlBk-TCQE5RZgeyg") # or by sheet name: gc.open("TestList")
        wksheet = sh.sheet1		
        saveData=wksheet.get_values('K2')
        print(saveData[0][0])
    
    except:
        print(0)

def saveData(data):
    copsim = {
    "type": "service_account",
    "project_id": "coppeliasim-playground",
    "private_key_id": "2334b85e78cddfdf9254a39ca90f9c1e8661e38a",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCiMDdbCyS90tU5\nXBOO8cBD3Ic9p266o298jiXhYlW2QiSBh/YCjA6aRQdNF1J3oZfWXSIc6eYh03ki\nZ1fg5ZWEMn3pExMSGHs3HMCqE2O7fJzXhrUQoAH9r9DvptulYK4mzkFw6jaD9RJM\nVYUNVnGA70d1nT1mFsmPxAgVM075JuuK9m6DxUKiiTuIZIfSpoGsGLus3fV/J5v+\nPWMuZC6ps/PAtkWUtUzzTcKMi/sMcM9fBpW0t0dhsc04u6FbW6ag3BQ+Xl15ef3K\nXJob6CqHLMMdBNvVnQe0VNZmIXMF78qWrTqKnxLCtjpNFyQImOeuTxI4BZ1UKKcG\nZ9xRRuUtAgMBAAECggEAJ51eT/sTUNg344hFcLNE0m6BjAIi7ixwVTyFLR1vMRLL\nxuW2JZ4fDPhSVbaeGoFaTG44IFbTMqzsGAak9NYu5HjOv0i87j0Tj30S5BfTUt6X\nkp8hB7wFcHjqsDaRzL2mG+1iF5nlkeqguwticcUM+UC4tBYhgpeLSPXJQaBkKD/B\nULjIIYJ86kQl2bvMiUff1IokriqZ6ryIm3PxcdwYqFYBt6vqVf/KwIdOTD1+FTtG\nms+rBrBCF3/Uv1MLlOCMVdQXtroKKUHE1Pk7KiEkPwURHCb/DwIvtPUGiKP5mLNh\nstENkjnKlIE4qlYhQWQoZxckEFMtXj0MN2DKKieLMQKBgQDRokDKnUUW1vyl7I6K\nBVq/987MGFQO11z0dLg/SBdY75Y64MJAhVTgAgxrPvPnRRdMQS4n9SctbQIOlmS4\njOcWfzXuyISPJfEvy76sNCzj2yLDglUtANYnlnWnfA/fRxAvR6kaUyStVyT94h/z\npHrYXm/yGjuEoPlv0SQ5fFCUZQKBgQDGD4mr0/ixGLhQZSOfabQ74V9CIvah+GDu\nNVGZGIgsvkma0GX7cy8PiHajieOe5NeTYStkdX0zptH7DSQH34Z2ldwUkz2wXhtH\nUV5+KvWJ6v0RAjIvtvR1aZOcX1NXrtVVRjlmDzw0VZ7sQSYBb88wJgzs7tLXXzWK\nmice6R4NKQKBgQCdM1f02HSryPHSlw7Yj2VbGUA5KnE2Y+dv5WsZAT2I0rlMU6k3\nawSXqtGXRrDuF5B9/U7YZe1IEjt9pufGwNq1sxVFh5ZoJiK0HcxRJBsZjwWFqOGo\nir0NGLYHr2/Tll2bptg3Rmv1lKjHvd8J/KimQkMeQO+q6G/EmwfYF9HxRQKBgQCs\nW4krBuQ8+Y4sKFe/unUmRxJms5Z9jXCM28mOuVKH3XCgUQrur2Yc1lyoJK7475zK\nnJzuZ2/1Kw9AskbQsyyIthE3torQmJSUk7LviOL0ipJ/4rFZ5JUIOEBErJASlgsA\nkoQQ1OFHidsrLeatCWf8NqC473x8AFbPryasN6H3QQKBgFvkzmP/y1iXG6SB22As\n4Qi0Setgp1ltu11hdyU6OjmvLX+hLVQCXLnGzafsNqukSDcpmy3DplOl3laQqQjB\nWRbyZyS6syJzc3IN4j8D8rV+st8aSCLqeQuIBfv+sV8KJfMHVRrpQHOaYcSWAJWP\n3lUJsK6F2jqv6VNlL+n4j/R9\n-----END PRIVATE KEY-----\n",
    "client_email": "copsim@coppeliasim-playground.iam.gserviceaccount.com",
    "client_id": "110686459353082313226",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/copsim%40coppeliasim-playground.iam.gserviceaccount.com"
    }
    try:
        gc = gspread.service_account_from_dict(copsim)
        sh = gc.open_by_key("1LK9K4a3y2-j2HZOXZPtMqCQG224zlBk-TCQE5RZgeyg") # or by sheet name: gc.open("TestList")
        wksheet = sh.sheet1		
        data = str(data).replace('{','{"').replace(':','":').replace(',',',"')
        data_to_push = [str(data)]
        wksheet.update('K2',[data_to_push])
        print(data)
    
    except:
        print(0)
