from skimage.metrics import structural_similarity as compare_ssim
import cv2
import pyautogui
import time
import smtplib, ssl

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

        cv2.imwrite(root_dir+"\p_img_a.png", imageB)
        time.sleep(5)
except KeyboardInterrupt:
    print("Process Interrupt")
    pass
    


