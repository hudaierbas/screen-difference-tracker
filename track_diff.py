from skimage.metrics import structural_similarity as compare_ssim
import cv2
import pyautogui
import time
import smtplib, ssl
import numpy as np

#cofig
root_dir= r"C:\Users\herbas\Desktop\hudai\python\screen_tracking_v2"
smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "my@gmail.com"
receiver_email = "my@gmail.com"
password = "password"
message = "message"

#smtp
context = ssl.create_default_context()

def send_email():   
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        print(e)
    finally:
        server.quit() 

#detect difference
im = pyautogui.screenshot()
im.save(root_dir+"\p_img_a.png")

try:
    while True:
        imageA = cv2.imread("p_img_a.png")

        im = pyautogui.screenshot()
        im.save(root_dir+"\p_img_b.png")
        imageB = cv2.imread("p_img_b.png")

        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        (score, diff) = compare_ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")
        print("SSIM: {}".format(score))

        if score < 1:
            send_email()

        #display difference
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        mask = np.zeros(imageB.shape, dtype='uint8')
        filled_after = imageA.copy()

        for c in contours:
            area = cv2.contourArea(c)
            if area > 40:
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(imageA, (x, y), (x + w, y + h), (36,255,12), 2)
                cv2.rectangle(imageB, (x, y), (x + w, y + h), (36,255,12), 2)
                cv2.drawContours(mask, [c], 0, (0,255,0), -1)
                cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)

        cv2.imshow('before', imageA)
        cv2.imshow('after', imageB)
        cv2.imshow('diff',diff)
        cv2.imshow('mask',mask)
        cv2.imshow('filled after',filled_after)



        cv2.imwrite(root_dir+"\p_img_a.png", imageB)
        time.sleep(5)
except KeyboardInterrupt:
    print("Process Interrupt")
    pass
    


